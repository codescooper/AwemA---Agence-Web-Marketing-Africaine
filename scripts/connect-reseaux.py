#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connecteur « présence digitale » → écrit reseaux.json (données RÉELLES).

Remplit le contrat outils/_data (reseaux.json) à partir des réseaux sociaux. Voies :

  1) META — TOUTES LES PAGES (recommandé pour l'agence)
     Un seul token : découvre toutes les Pages gérées et crée/maj un client par Page.
     export META_TOKEN="EAAB..."
     python3 connect-reseaux.py --meta-all

  2) META — UNE PAGE précise
     export META_TOKEN="EAAB..." FB_PAGE_ID="..." IG_USER_ID="..."
     python3 connect-reseaux.py --meta departements/marketing/clients/la-grande-vision

  3) IMPORT MANUEL (CSV exporté depuis Meta Business Suite / TwoMinuteReports / autre)
     python3 connect-reseaux.py --manuel <client_dir> <export.csv>

Aucune donnée inventée : si une source est absente, les champs restent null.
Le réseau du sandbox peut bloquer graph.facebook.com → lancer depuis une machine
connectée (ou via le GitHub Action .github/workflows/sync-reseaux.yml).

TEST hors-ligne : définir AWEMA_PAGES_FIXTURE=<fichier.json> pour simuler me/accounts.
"""
import csv
import glob
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

GRAPH = "https://graph.facebook.com/v21.0"
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.environ.get("AWEMA_PAGES_FIXTURE")  # tests hors-ligne


def _pages_ignorees():
    """IDs de Pages à ne JAMAIS synchroniser (anciennes pages, doublons, pages vides).
    Éditer scripts/reseaux-ignore.json : {"pages_ignorees": ["<page_id>", ...]}."""
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reseaux-ignore.json")
    try:
        return {str(x) for x in json.load(open(f, encoding="utf-8")).get("pages_ignorees", [])}
    except Exception:
        return set()


IGNOREES = _pages_ignorees()

# Portée Page : les noms de métriques valides varient selon la version de l'API Graph.
# Le script essaie ces candidats dans l'ordre et garde le premier qui renvoie une valeur.
PORTEE_CANDIDATS = [
    "page_impressions_unique",      # portée (28 j) — historique
    "page_impressions",             # impressions
    "page_views_total",             # vues de la Page
    "page_total_actions",           # actions sur la Page
    "page_post_engagements",        # engagements sur les posts
]
_METRIQUE_PORTEE = None  # mémorise la métrique qui marche (découverte au 1er succès)


def _vide():
    return {
        "connecte": False, "source": None, "maj": None,
        "global": {k: None for k in ["audience", "posts", "likes", "commentaires",
                                      "partages", "portee", "engagement_taux"]},
        "par_reseau": {r: {k: None for k in ["abonnes", "posts", "likes", "commentaires", "portee"]}
                       for r in ["facebook", "instagram", "tiktok", "linkedin"]},
        "top_fans": [], "top_posts": [], "evolution_audience": [],
    }


def _get(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # Remonte le vrai message d'erreur Graph (sinon on n'a que "400 Bad Request")
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        msg = body
        try:
            err = json.loads(body).get("error", {})
            msg = (f"{err.get('message')} "
                   f"(code={err.get('code')}, subcode={err.get('error_subcode')})")
        except Exception:
            pass
        raise RuntimeError(f"HTTP {e.code} — {msg}") from None


def via_meta(client_dir):
    token = os.environ.get("META_TOKEN")
    page = os.environ.get("FB_PAGE_ID")
    ig = os.environ.get("IG_USER_ID")
    if not token:
        sys.exit("❌ META_TOKEN manquant. export META_TOKEN=...  (et FB_PAGE_ID / IG_USER_ID)")
    data = _vide()
    data["source"] = "meta-graph-api"

    def q(path, params):
        params = {**params, "access_token": token}
        return _get(f"{GRAPH}/{path}?{urllib.parse.urlencode(params)}")

    # --- Facebook Page ---
    if page:
        fb = data["par_reseau"]["facebook"]
        try:
            info = q(page, {"fields": "fan_count,followers_count"})
            fb["abonnes"] = info.get("followers_count") or info.get("fan_count")
        except Exception as e:
            print("⚠️ FB page:", e)
        try:
            posts = q(f"{page}/posts", {"fields": "message,likes.summary(true),comments.summary(true),shares",
                                        "limit": 25})["data"]
            fb["posts"] = len(posts)
            likes = sum((p.get("likes", {}).get("summary", {}).get("total_count", 0)) for p in posts)
            comm = sum((p.get("comments", {}).get("summary", {}).get("total_count", 0)) for p in posts)
            fb["likes"], fb["commentaires"] = likes, comm
            for p in posts:
                data["top_posts"].append({
                    "titre": (p.get("message") or "")[:80], "plateforme": "Facebook",
                    "likes": p.get("likes", {}).get("summary", {}).get("total_count", 0),
                    "commentaires": p.get("comments", {}).get("summary", {}).get("total_count", 0),
                    "partages": (p.get("shares") or {}).get("count", 0)})
        except Exception as e:
            print("⚠️ FB posts:", e)

    # --- Instagram Business ---
    if ig:
        ins = data["par_reseau"]["instagram"]
        try:
            info = q(ig, {"fields": "followers_count,media_count"})
            ins["abonnes"] = info.get("followers_count")
            ins["posts"] = info.get("media_count")
        except Exception as e:
            print("⚠️ IG info:", e)
        try:
            media = q(f"{ig}/media", {"fields": "caption,like_count,comments_count", "limit": 25})["data"]
            ins["likes"] = sum(m.get("like_count", 0) for m in media)
            ins["commentaires"] = sum(m.get("comments_count", 0) for m in media)
            for m in media:
                data["top_posts"].append({
                    "titre": (m.get("caption") or "")[:80], "plateforme": "Instagram",
                    "likes": m.get("like_count", 0), "commentaires": m.get("comments_count", 0), "partages": 0})
        except Exception as e:
            print("⚠️ IG media:", e)

    _consolider(data)
    _ecrire(client_dir, data)


def via_manuel(client_dir, csv_path):
    """CSV attendu (souple) : colonnes reseau,abonnes,posts,likes,commentaires,portee."""
    data = _vide(); data["source"] = "manuel"
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r = (row.get("reseau") or "").strip().lower()
            if r in data["par_reseau"]:
                for k in ["abonnes", "posts", "likes", "commentaires", "portee"]:
                    v = row.get(k)
                    data["par_reseau"][r][k] = int(v) if v and v.isdigit() else None
    _consolider(data)
    _ecrire(client_dir, data)


def _consolider(data):
    pr = data["par_reseau"]
    def somme(k):
        vals = [pr[r][k] for r in pr if pr[r][k] is not None]
        return sum(vals) if vals else None
    g = data["global"]
    g["audience"] = somme("abonnes"); g["posts"] = somme("posts")
    g["likes"] = somme("likes"); g["commentaires"] = somme("commentaires")
    g["portee"] = somme("portee")
    if g["portee"] and g["likes"] is not None and g["commentaires"] is not None:
        g["engagement_taux"] = round((g["likes"] + g["commentaires"]) / g["portee"] * 100, 2)
    data["top_posts"] = sorted(data["top_posts"], key=lambda p: p["likes"] + p["commentaires"], reverse=True)[:8]
    data["connecte"] = any(pr[r]["abonnes"] is not None for r in pr)
    data["maj"] = datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ecrire(client_dir, data):
    out = os.path.join(client_dir, "_donnees", "reseaux.json")
    base = {}
    try:
        with open(out, encoding="utf-8") as f:
            base = json.load(f)
    except FileNotFoundError:
        pass
    base.update(data); base["client"] = os.path.basename(client_dir.rstrip("/"))
    base.pop("_doc", None)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(base, f, ensure_ascii=False, indent=2)
    print(f"✅ {out} — connecté={base['connecte']} source={base['source']}")
    print("   Pense à régénérer le registre : python3 outils/_data/build.py")


# --------------------------------------------------------------------------- #
# META — découverte de TOUTES les Pages (un client par Page)
# --------------------------------------------------------------------------- #
def slugify(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "page"


def initiales(nom):
    parts = [p for p in re.split(r"\s+", nom or "") if p]
    if not parts:
        return "AW"
    if len(parts) >= 2:
        return (parts[0][:1] + parts[1][:1]).upper()
    return parts[0][:2].upper()


def _pages():
    """Liste les Pages gérées (me/accounts) avec IG lié. Pagination gérée.
    En mode FIXTURE, lit un JSON {"data":[...]} pour tester hors-ligne."""
    if FIXTURE:
        with open(FIXTURE, encoding="utf-8") as f:
            return json.load(f).get("data", [])
    token = os.environ.get("META_TOKEN")
    if not token:
        sys.exit("❌ META_TOKEN manquant. export META_TOKEN=\"EAAB...\"")
    fields = ("name,id,access_token,fan_count,followers_count,"
              "instagram_business_account{id,username,followers_count,media_count}")
    url = f"{GRAPH}/me/accounts?fields={fields}&limit=50&access_token={token}"
    out = []
    while url:
        d = _get(url)
        out += d.get("data", [])
        url = (d.get("paging") or {}).get("next")
    return out


def _trouver_client_par_pageid(page_id):
    motif = os.path.join(RACINE, "departements", "*", "clients", "*", "_donnees", "client.json")
    for cj in glob.glob(motif):
        try:
            d = json.load(open(cj, encoding="utf-8"))
        except Exception:
            continue
        if str(d.get("fb_page_id")) == str(page_id):
            return os.path.dirname(os.path.dirname(cj))
    return None


def _assurer_client_json(client_dir, pg):
    donnees = os.path.join(client_dir, "_donnees")
    os.makedirs(donnees, exist_ok=True)
    cj = os.path.join(donnees, "client.json")
    nom = pg.get("name") or pg.get("id")
    ig = pg.get("instagram_business_account") or {}
    slug = os.path.basename(client_dir)
    if os.path.exists(cj):
        d = json.load(open(cj, encoding="utf-8"))            # préserve les éditions humaines
    else:
        d = {
            "id": slug, "nom": nom, "secteur": "", "lieu": "",
            "departement": "marketing", "statut": "actif", "initiales": initiales(nom),
            "reseaux": {
                "facebook": f"https://facebook.com/{pg.get('id')}",
                "instagram": (f"https://instagram.com/{ig.get('username')}" if ig.get("username") else ""),
                "tiktok": "", "linkedin": "", "whatsapp": "",
            },
            "chemins": {
                "campagne": "_donnees/campagne.json", "reseaux": "_donnees/reseaux.json",
                "revue": f"../../../../outils/revue-visuels/index.html?client={slug}",
            },
        }
    d["fb_page_id"] = pg.get("id")
    if ig.get("id"):
        d["ig_user_id"] = ig.get("id")
    json.dump(d, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def _engagement_page(data, page_id, ptok):
    """Likes/commentaires + top posts FB (sautés en mode FIXTURE)."""
    if FIXTURE or not ptok:
        return
    fb = data["par_reseau"]["facebook"]
    try:
        posts = _get(f"{GRAPH}/{page_id}/posts?fields=message,likes.summary(true),"
                     f"comments.summary(true),shares&limit=25&access_token={ptok}")["data"]
        fb["posts"] = len(posts)
        fb["likes"] = sum(p.get("likes", {}).get("summary", {}).get("total_count", 0) for p in posts)
        fb["commentaires"] = sum(p.get("comments", {}).get("summary", {}).get("total_count", 0) for p in posts)
        for p in posts:
            data["top_posts"].append({
                "titre": (p.get("message") or "")[:80], "plateforme": "Facebook",
                "likes": p.get("likes", {}).get("summary", {}).get("total_count", 0),
                "commentaires": p.get("comments", {}).get("summary", {}).get("total_count", 0),
                "partages": (p.get("shares") or {}).get("count", 0)})
    except Exception as e:
        print(f"  ⚠️ FB posts {page_id}: {e}")
    _insights_page(data, page_id, ptok)


def _insights_page(data, page_id, ptok):
    """Portée Page (28 j) via read_insights. Essaie plusieurs métriques (les noms
    valides changent selon la version de l'API) ; garde la 1re qui répond.
    Reste null si aucune ne marche (ex. permission read_insights absente)."""
    if FIXTURE or not ptok:
        return
    fb = data["par_reseau"]["facebook"]
    global _METRIQUE_PORTEE
    candidats = ([_METRIQUE_PORTEE] if _METRIQUE_PORTEE else []) + [
        m for m in PORTEE_CANDIDATS if m != _METRIQUE_PORTEE]
    for metric in candidats:
        try:
            rep = _get(f"{GRAPH}/{page_id}/insights?metric={metric}"
                       f"&period=days_28&access_token={ptok}").get("data", [])
            for m in rep:
                vals = m.get("values") or []
                val = vals[-1].get("value") if vals else None
                if val is not None:
                    fb["portee"] = val          # → global.portee + engagement_taux
                    _METRIQUE_PORTEE = metric    # mémorise pour les pages suivantes
                    return
        except Exception as e:
            print(f"  ⚠️ insights {page_id} [{metric}]: {e}")
    # Aucune métrique valide → portée laissée à null (déjà le cas)


def _engagement_ig(data, ig, ptok):
    if not ig:
        return
    ins = data["par_reseau"]["instagram"]
    ins["abonnes"] = ig.get("followers_count")
    ins["posts"] = ig.get("media_count")
    if FIXTURE or not ptok or not ig.get("id"):
        return
    try:
        media = _get(f"{GRAPH}/{ig['id']}/media?fields=caption,like_count,"
                     f"comments_count&limit=25&access_token={ptok}")["data"]
        ins["likes"] = sum(m.get("like_count", 0) for m in media)
        ins["commentaires"] = sum(m.get("comments_count", 0) for m in media)
        for m in media:
            data["top_posts"].append({
                "titre": (m.get("caption") or "")[:80], "plateforme": "Instagram",
                "likes": m.get("like_count", 0), "commentaires": m.get("comments_count", 0),
                "partages": 0})
    except Exception as e:
        print(f"  ⚠️ IG media: {e}")


def _page_info(page_id, ptok):
    """Abonnés + nom à jour via le TOKEN DE PAGE (plus fiable que me/accounts)."""
    if FIXTURE or not ptok:
        return None, None
    try:
        d = _get(f"{GRAPH}/{page_id}?fields=name,followers_count,fan_count&access_token={ptok}")
        ab = d.get("followers_count")
        if ab is None:
            ab = d.get("fan_count")
        return ab, d.get("name")
    except Exception as e:
        print(f"  ⚠️ page info {page_id}: {e}")
        return None, None


def via_meta_all():
    """Un client par Page gérée. Crée les dossiers manquants, met à jour reseaux.json."""
    pages = _pages()
    n = 0
    for pg in pages:
        page_id = pg.get("id")
        if not page_id:
            continue
        if str(page_id) in IGNOREES:
            print(f"  ⏭️  {pg.get('name') or page_id} ignorée (reseaux-ignore.json)")
            continue
        ptok = pg.get("access_token")
        # Abonnés + nom fiables via le token de Page
        ab, nom_maj = _page_info(page_id, ptok)
        if nom_maj:
            pg["name"] = nom_maj
        if ab is None:
            ab = pg.get("followers_count") or pg.get("fan_count")
        client_dir = _trouver_client_par_pageid(page_id) or os.path.join(
            RACINE, "departements", "marketing", "clients", slugify(pg.get("name") or page_id))
        _assurer_client_json(client_dir, pg)
        data = _vide()
        data["source"] = "meta-graph-api"
        data["par_reseau"]["facebook"]["abonnes"] = ab
        _engagement_page(data, page_id, ptok)
        _engagement_ig(data, pg.get("instagram_business_account") or {}, ptok)
        _consolider(data)
        _ecrire(client_dir, data)
        n += 1
        print(f"  ✓ {pg.get('name')} ({ab if ab is not None else '—'} abonnés) → "
              f"{os.path.relpath(client_dir, RACINE)}")
    print(f"✅ {n} page(s) synchronisée(s). Régénère le registre : python3 outils/_data/build.py")


def main():
    a = sys.argv[1:]
    if a and a[0] == "--meta-all":
        via_meta_all()
    elif len(a) >= 2 and a[0] == "--meta":
        via_meta(a[1])
    elif len(a) >= 3 and a[0] == "--manuel":
        via_manuel(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
