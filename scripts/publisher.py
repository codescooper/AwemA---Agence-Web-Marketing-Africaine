#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AWEMA · Planificateur de publication (file d'attente Git + cron). ADR-010.

Parcourt les posts en file d'attente (modules/*/clients/*/_donnees/_planning/*.json), publie ceux
qui sont DUS (statut=programme et publier_le <= maintenant) sur chaque réseau, de façon IDEMPOTENTE
(un réseau déjà publié n'est jamais republié), met à jour le statut et réécrit le fichier.

Tokens d'écriture lus dans l'environnement (Secrets/Variables GitHub) :
  META_TOKEN · LINKEDIN_TOKEN · YOUTUBE_API_KEY (lecture) … (voir TOKENS)
Mode :  python3 scripts/publisher.py            → publie réellement
        python3 scripts/publisher.py --dry-run  → simule (aucun appel réseau), pour tester le moteur

ADN : stdlib uniquement ; aucun secret écrit dans le dépôt ; aucune donnée fictive.
Les appels de publication suivent les specs des plateformes mais doivent être validés en conditions réelles.
"""
import glob
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from urllib.error import HTTPError

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MAX_TENTATIVES = 3
GRAPH = "https://graph.facebook.com/v21.0"


# ————————————————————————— utilitaires —————————————————————————
def maintenant():
    # PUBLISH_NOW (ISO) permet de tester ; sinon l'heure réelle UTC.
    s = os.environ.get("PUBLISH_NOW")
    if s:
        return parse_iso(s)
    return datetime.now(timezone.utc)


def parse_iso(s):
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def http(url, data=None, headers=None, method=None):
    h = {"Accept": "application/json"}
    if headers:
        h.update(headers)
    body = None
    if data is not None:
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=h, method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {"error": "HTTP %s" % e.code}
    except Exception as e:
        return 0, {"error": str(e)}


def token(name):
    return (os.environ.get(name) or "").strip() or None


# ————————————————————————— connecteurs d'écriture —————————————————————————
# Chaque connecteur : (item, medias[urls]) -> {"ok":bool, "url"|"error":..., "detail":...}
# Codés selon les specs ; à valider en live (scopes d'écriture + IDs de compte + App Review requis).

def c_facebook(item, medias):
    tok = token("META_TOKEN")
    if not tok:
        return {"ok": False, "error": "META_TOKEN manquant"}
    page_id = (item.get("comptes") or {}).get("facebook")
    # Récupère le page access token (et l'id si absent) via /me/accounts.
    st, acc = http(GRAPH + "/me/accounts?" + urllib.parse.urlencode({"access_token": tok}))
    pages = (acc or {}).get("data") or []
    page = None
    for p in pages:
        if not page_id or str(p.get("id")) == str(page_id):
            page = p
            break
    if not page:
        return {"ok": False, "error": "Page introuvable (admin requis / scope pages_show_list)"}
    pid, ptok = page.get("id"), page.get("access_token")
    texte = (item.get("contenu") or {}).get("texte", "")
    if medias:
        st, r = http(GRAPH + "/%s/photos" % pid, data=urllib.parse.urlencode(
            {"url": medias[0], "caption": texte, "access_token": ptok}).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"})
    else:
        lien = (item.get("contenu") or {}).get("lien", "")
        params = {"message": texte, "access_token": ptok}
        if lien:
            params["link"] = lien
        st, r = http(GRAPH + "/%s/feed" % pid, data=urllib.parse.urlencode(params).encode(),
                     headers={"Content-Type": "application/x-www-form-urlencoded"})
    if st in (200, 201) and (r.get("id") or r.get("post_id")):
        pubid = r.get("post_id") or r.get("id")
        return {"ok": True, "url": "https://www.facebook.com/%s" % pubid, "detail": pubid}
    return {"ok": False, "error": (r.get("error") or {}).get("message") or str(r)[:160]}


def c_linkedin(item, medias):
    tok = token("LINKEDIN_TOKEN")
    if not tok:
        return {"ok": False, "error": "LINKEDIN_TOKEN manquant"}
    org = (item.get("comptes") or {}).get("linkedin")
    if not org:
        return {"ok": False, "error": "URN d'organisation LinkedIn manquant (comptes.linkedin)"}
    author = org if str(org).startswith("urn:") else ("urn:li:organization:%s" % org)
    texte = (item.get("contenu") or {}).get("texte", "")
    payload = {
        "author": author, "lifecycleState": "PUBLISHED",
        "specificContent": {"com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": texte},
            "shareMediaCategory": "IMAGE" if medias else "NONE"}},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}
    # NB : l'image LinkedIn nécessite un upload d'asset préalable (registerUpload) — non couvert ici.
    st, r = http("https://api.linkedin.com/v2/ugcPosts", data=payload,
                 headers={"Authorization": "Bearer " + tok, "X-Restli-Protocol-Version": "2.0.0"})
    if st in (200, 201) and r.get("id"):
        return {"ok": True, "url": "https://www.linkedin.com/feed/update/%s" % r.get("id"), "detail": r.get("id")}
    return {"ok": False, "error": r.get("message") or str(r)[:160]}


def c_instagram(item, medias):
    tok = token("META_TOKEN")
    if not tok:
        return {"ok": False, "error": "META_TOKEN manquant"}
    ig = (item.get("comptes") or {}).get("instagram")
    if not ig:
        return {"ok": False, "error": "ID utilisateur Instagram (Business) manquant (comptes.instagram)"}
    if not medias:
        return {"ok": False, "error": "Instagram exige une image (URL publique)"}
    texte = (item.get("contenu") or {}).get("texte", "")
    st, r = http(GRAPH + "/%s/media" % ig, data=urllib.parse.urlencode(
        {"image_url": medias[0], "caption": texte, "access_token": tok}).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    cid = r.get("id")
    if not cid:
        return {"ok": False, "error": (r.get("error") or {}).get("message") or str(r)[:160]}
    st, r2 = http(GRAPH + "/%s/media_publish" % ig, data=urllib.parse.urlencode(
        {"creation_id": cid, "access_token": tok}).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    if r2.get("id"):
        return {"ok": True, "url": "https://www.instagram.com/", "detail": r2.get("id")}
    return {"ok": False, "error": (r2.get("error") or {}).get("message") or str(r2)[:160]}


def c_video_a_venir(item, medias):
    # YouTube (upload vidéo) & TikTok (Content Posting API auditée / brouillon) : activés en phase ultérieure.
    return {"ok": False, "error": "Connecteur vidéo à activer (validation plateforme requise)", "differe": True}


CONNECTEURS = {
    "facebook": c_facebook,
    "linkedin": c_linkedin,
    "instagram": c_instagram,
    "youtube": c_video_a_venir,
    "tiktok": c_video_a_venir,
}


# ————————————————————————— moteur (testable) —————————————————————————
def est_du(item, ref):
    if (item.get("statut") or "") not in ("programme", "partiel"):
        return False
    d = parse_iso(item.get("publier_le"))
    return d is not None and d <= ref


def medias_urls(item):
    return [m.get("url") for m in (item.get("media") or []) if m.get("url")]


def publier_item(item, ref, publish=None, dry=False):
    """Publie les réseaux DUS et non encore réussis. Renvoie l'item modifié. `publish` injectable pour les tests."""
    publish = publish or (lambda reseau, it, med: CONNECTEURS.get(reseau, c_video_a_venir)(it, med))
    item.setdefault("resultats", {})
    med = medias_urls(item)
    horo = ref.isoformat()
    for reseau in (item.get("reseaux") or []):
        deja = item["resultats"].get(reseau)
        if deja and deja.get("ok"):
            continue  # idempotent : jamais republier
        if dry:
            res = {"ok": True, "url": "(dry-run)", "detail": "simulation"}
        else:
            res = publish(reseau, item, med)
        res = dict(res)
        res["at"] = horo
        item["resultats"][reseau] = res
    # statut global
    reseaux = item.get("reseaux") or []
    oks = [r for r in reseaux if item["resultats"].get(r, {}).get("ok")]
    differes = [r for r in reseaux if item["resultats"].get(r, {}).get("differe")]
    if len(oks) == len(reseaux):
        item["statut"] = "publie"
    elif oks:
        item["statut"] = "partiel"
        item["tentatives"] = item.get("tentatives", 0) + 1
    else:
        item["tentatives"] = item.get("tentatives", 0) + 1
        item["statut"] = "echec" if (item["tentatives"] >= MAX_TENTATIVES and not differes) else "programme"
    item["maj_le"] = horo
    return item


def lister_fichiers():
    motif = os.path.join(RACINE, "modules", "*", "clients", "*", "_donnees", "_planning", "*.json")
    return [f for f in sorted(glob.glob(motif)) if os.path.basename(f) != "index.json"]


def main():
    dry = "--dry-run" in sys.argv
    ref = maintenant()
    traites = 0
    for path in lister_fichiers():
        try:
            with open(path, encoding="utf-8") as f:
                item = json.load(f)
        except Exception as e:
            print("⚠️ illisible: %s (%s)" % (path, e))
            continue
        if not est_du(item, ref):
            continue
        avant = item.get("statut")
        item = publier_item(item, ref, dry=dry)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        traites += 1
        print("• %s : %s → %s" % (os.path.relpath(path, RACINE), avant, item["statut"]))
    print("✅ %d post(s) traité(s)%s." % (traites, " [DRY-RUN]" if dry else ""))


if __name__ == "__main__":
    main()
