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

# Insights Page (28 j) — les noms de métriques valides varient selon la version de l'API.
# On distingue la VRAIE portée (reach) des simples VUES de page : ce ne sont pas la même chose.
#   • page_impressions_unique / page_impressions = portée/impressions (souvent dépréciées en v21)
#   • page_views_total = nombre de vues de la Page (disponible en v21)
# Pour chaque indicateur, on essaie les candidats dans l'ordre et on garde le 1er qui répond.
PORTEE_CANDIDATS = ["page_impressions_unique", "page_impressions"]   # portée réelle (reach)
VUES_CANDIDATS = ["page_views_total"]                                # vues de la Page
GAGNES_CANDIDATS = ["page_fan_adds_unique", "page_fan_adds"]         # nouveaux abonnés (28 j)
PERDUS_CANDIDATS = ["page_fan_removes_unique", "page_fan_removes"]   # désabonnements (28 j)
_METRIQUE = {"portee": None, "vues": None, "gagnes": None, "perdus": None}

REACTIONS = ["like", "love", "care", "haha", "wow", "sad", "angry"]
JOURS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def _vide():
    return {
        "connecte": False, "source": None, "maj": None,
        "global": {k: None for k in ["audience", "posts", "likes", "commentaires",
                                      "partages", "portee", "vues", "engagement_taux"]},
        "par_reseau": {r: {k: None for k in ["abonnes", "posts", "likes", "commentaires",
                                             "partages", "portee", "vues"]}
                       for r in ["facebook", "instagram", "tiktok", "linkedin"]},
        "reactions": None,            # {like,love,care,haha,wow,sad,angry} (Facebook, posts récents)
        "portee_post": None,          # {moyenne, max} portée par post (reach réel)
        "croissance": None,           # {gagnes_28j, perdus_28j, net_28j}
        "cadence": None,              # {dernier_post, jours_depuis, posts_30j, posts_par_semaine}
        "meilleur_creneau": None,     # {jour, heure, par_jour, recommandation}
        "types_contenu": None,        # {photo:{n,eng_moyen}, video:{...}, ...}
        "a_repondre": None,           # {total, exemples:[...]}  ← inbox community management
        "top_commentateurs": [],      # abonnés les plus actifs (vrais « top fans »)
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
        vals = [pr[r].get(k) for r in pr if pr[r].get(k) is not None]
        return sum(vals) if vals else None
    g = data["global"]
    g["audience"] = somme("abonnes"); g["posts"] = somme("posts")
    g["likes"] = somme("likes"); g["commentaires"] = somme("commentaires")
    g["partages"] = somme("partages")
    g["portee"] = somme("portee")   # vraie portée Page (reach) — null si indisponible (API v21)
    g["vues"] = somme("vues")        # vues de la Page (28 j)
    # Taux d'engagement RÉEL = engagement moyen par post / portée moyenne par post (×100).
    pp = (data.get("portee_post") or {}).get("moyenne")
    nb = pr["facebook"]["posts"]
    if pp and nb:
        eng = (pr["facebook"].get("likes") or 0) + (pr["facebook"].get("commentaires") or 0) \
            + (pr["facebook"].get("partages") or 0)
        g["engagement_taux"] = round((eng / nb) / pp * 100, 1)
    data["top_posts"] = sorted(
        data["top_posts"],
        key=lambda p: p["likes"] + p["commentaires"] + p.get("partages", 0), reverse=True)[:8]
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
    # Conserve l'historique d'audience et ajoute le point du jour (vraie courbe dans le temps).
    ancienne_ev = base.get("evolution_audience") or []
    base.update(data); base["client"] = os.path.basename(client_dir.rstrip("/"))
    base.pop("_doc", None)
    audience = (data.get("global") or {}).get("audience")
    if audience is not None:
        jour = datetime.now(timezone.utc).date().isoformat()
        ev = [p for p in ancienne_ev if p.get("date") != jour]
        ev.append({"date": jour, "valeur": audience})
        base["evolution_audience"] = ev[-90:]   # garde 90 derniers points
    else:
        base["evolution_audience"] = ancienne_ev
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


def _champs_posts():
    """Champs riches récupérés en UN appel /posts (réactions par type, commentaires+réponses)."""
    rea = ",".join(f"reactions.type({t.upper()}).limit(0).summary(total_count).as(r_{t})"
                   for t in REACTIONS)
    return ("message,created_time,permalink_url,shares,"
            "attachments{media_type},"
            "comments.summary(true).limit(60){from,message,created_time,"
            "comments.limit(30){from}}," + rea)


def _engagement_page(data, page_id, ptok):
    """Récupère les posts FB enrichis (réactions, commentaires, réponses) puis dérive
    tous les indicateurs community management. Sauté en mode FIXTURE."""
    if FIXTURE or not ptok:
        return
    fb = data["par_reseau"]["facebook"]
    posts = []
    try:
        posts = _get(f"{GRAPH}/{page_id}/posts?fields={_champs_posts()}"
                     f"&limit=30&access_token={ptok}")["data"]
    except Exception as e:
        print(f"  ⚠️ FB posts {page_id}: {e}")

    if posts:
        rea_tot = {t: 0 for t in REACTIONS}
        partages = 0
        for p in posts:
            n_com = (p.get("comments", {}).get("summary", {}) or {}).get("total_count", 0)
            rea = {t: (p.get(f"r_{t}", {}).get("summary", {}) or {}).get("total_count", 0)
                   for t in REACTIONS}
            for t in REACTIONS:
                rea_tot[t] += rea[t]
            n_rea = sum(rea.values())
            sh = (p.get("shares") or {}).get("count", 0)
            partages += sh
            p["_rea"], p["_ncom"], p["_sh"] = n_rea, n_com, sh
            p["_eng"] = n_rea + n_com + sh
            data["top_posts"].append({
                "titre": (p.get("message") or "")[:80], "plateforme": "Facebook",
                "date": p.get("created_time"), "lien": p.get("permalink_url"),
                "likes": n_rea, "commentaires": n_com, "partages": sh,
                "type": _type_post(p), "reactions": rea, "portee": None})
        fb["posts"] = len(posts)
        fb["likes"] = sum(p["_rea"] for p in posts)
        fb["commentaires"] = sum(p["_ncom"] for p in posts)
        fb["partages"] = partages
        data["reactions"] = rea_tot
        _portee_posts(data, posts, ptok)
        _derive_commentaires(data, page_id, posts)
        _cadence(data, posts)
        _creneau(data, posts)
        _types_contenu(data, posts)

    _insights_page(data, page_id, ptok)
    _croissance(data, page_id, ptok)


def _type_post(p):
    att = ((p.get("attachments") or {}).get("data") or [{}])
    mt = (att[0].get("media_type") or "").lower() if att else ""
    return {"photo": "photo", "video": "vidéo", "share": "lien",
            "album": "album", "link": "lien"}.get(mt, "statut")


def _portee_posts(data, posts, ptok):
    """Portée RÉELLE par post (post_impressions_unique), best-effort sur les posts récents."""
    vals = []
    for p in posts[:12]:
        pid = p.get("id")
        if not pid:
            continue
        try:
            rep = _get(f"{GRAPH}/{pid}/insights/post_impressions_unique"
                       f"?access_token={ptok}").get("data", [])
            v = rep[0]["values"][0]["value"] if rep and rep[0].get("values") else None
            if v is not None:
                p["portee"] = v
                # reporte la portée dans le top_post correspondant
                for tp in data["top_posts"]:
                    if tp.get("lien") == p.get("permalink_url"):
                        tp["portee"] = v
                vals.append(v)
        except Exception as e:
            print(f"  ⚠️ portée post {pid}: {e}")
            break  # métrique probablement indisponible → on arrête de marteler l'API
    if vals:
        data["portee_post"] = {"moyenne": round(sum(vals) / len(vals)), "max": max(vals)}


def _derive_commentaires(data, page_id, posts):
    """Top commentateurs (abonnés les plus actifs) + commentaires SANS réponse de la Page."""
    compte = {}
    a_repondre = []
    for p in posts:
        for c in (p.get("comments", {}).get("data") or []):
            auteur = (c.get("from") or {})
            nom, aid = auteur.get("name"), auteur.get("id")
            if not nom or str(aid) == str(page_id):
                continue
            compte[nom] = compte.get(nom, 0) + 1
            reponses = (c.get("comments", {}).get("data") or [])
            page_a_repondu = any(str((r.get("from") or {}).get("id")) == str(page_id)
                                 for r in reponses)
            if not page_a_repondu:
                a_repondre.append({
                    "auteur": nom, "message": (c.get("message") or "")[:140],
                    "date": c.get("created_time"), "lien": p.get("permalink_url")})
    top = sorted(compte.items(), key=lambda kv: kv[1], reverse=True)[:8]
    data["top_commentateurs"] = [{"nom": n, "commentaires": k} for n, k in top]
    data["top_fans"] = [{"nom": n, "interactions": k} for n, k in top]  # alias dashboard
    a_repondre.sort(key=lambda x: x.get("date") or "", reverse=True)
    data["a_repondre"] = {"total": len(a_repondre), "exemples": a_repondre[:12]}


def _cadence(data, posts):
    dates = sorted([p["created_time"] for p in posts if p.get("created_time")], reverse=True)
    if not dates:
        return
    dernier = _parse_dt(dates[0])
    now = datetime.now(timezone.utc)
    jours_depuis = (now - dernier).days if dernier else None
    p30 = sum(1 for d in dates if (_parse_dt(d) and (now - _parse_dt(d)).days <= 30))
    # rythme = posts / nb de semaines couvertes par l'échantillon
    plus_vieux = _parse_dt(dates[-1])
    semaines = max(((dernier - plus_vieux).days / 7.0), 1) if (dernier and plus_vieux) else 1
    data["cadence"] = {
        "dernier_post": dates[0], "jours_depuis": jours_depuis, "posts_30j": p30,
        "posts_par_semaine": round(len(dates) / semaines, 1)}


def _creneau(data, posts):
    """Engagement moyen par jour de semaine et par heure → meilleur créneau pour publier."""
    par_jour, par_heure = {}, {}
    for p in posts:
        dt = _parse_dt(p.get("created_time"))
        if not dt:
            continue
        eng = p.get("_eng", 0)
        par_jour.setdefault(dt.weekday(), []).append(eng)
        par_heure.setdefault(dt.hour, []).append(eng)
    if not par_jour:
        return
    moy_jour = {j: sum(v) / len(v) for j, v in par_jour.items()}
    moy_heure = {h: sum(v) / len(v) for h, v in par_heure.items()}
    best_j = max(moy_jour, key=moy_jour.get)
    best_h = max(moy_heure, key=moy_heure.get)
    data["meilleur_creneau"] = {
        "jour": JOURS_FR[best_j], "heure": f"{best_h:02d}h",
        "par_jour": {JOURS_FR[j]: round(m, 1) for j, m in sorted(moy_jour.items())},
        "recommandation": f"{JOURS_FR[best_j]} vers {best_h:02d}h"}


def _types_contenu(data, posts):
    grp = {}
    for p in posts:
        t = _type_post(p)
        grp.setdefault(t, []).append(p.get("_eng", 0))
    data["types_contenu"] = {t: {"n": len(v), "engagement_moyen": round(sum(v) / len(v), 1)}
                             for t, v in grp.items()}


def _croissance(data, page_id, ptok):
    g = _insight_28j(page_id, ptok, "gagnes", GAGNES_CANDIDATS)
    p = _insight_28j(page_id, ptok, "perdus", PERDUS_CANDIDATS)
    if g is not None or p is not None:
        data["croissance"] = {"gagnes_28j": g, "perdus_28j": p,
                              "net_28j": (g or 0) - (p or 0)}


def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _insights_page(data, page_id, ptok):
    """Insights Page (28 j) via read_insights : portée réelle (reach) ET vues de page.
    Pour chaque indicateur on essaie plusieurs métriques candidates (les noms valides
    changent selon la version de l'API) et on garde la 1re qui répond. Chaque indicateur
    reste null si aucune candidate ne marche (ex. portée dépréciée en v21)."""
    if FIXTURE or not ptok:
        return
    fb = data["par_reseau"]["facebook"]
    fb["portee"] = _insight_28j(page_id, ptok, "portee", PORTEE_CANDIDATS)
    fb["vues"] = _insight_28j(page_id, ptok, "vues", VUES_CANDIDATS)


def _insight_28j(page_id, ptok, cle, candidats):
    """Retourne la valeur (28 j) du 1er métrique candidat qui répond, sinon None.
    Mémorise la métrique gagnante par indicateur pour accélérer les pages suivantes."""
    ordre = ([_METRIQUE[cle]] if _METRIQUE[cle] else []) + [
        m for m in candidats if m != _METRIQUE[cle]]
    for metric in ordre:
        try:
            rep = _get(f"{GRAPH}/{page_id}/insights?metric={metric}"
                       f"&period=days_28&access_token={ptok}").get("data", [])
            for m in rep:
                vals = m.get("values") or []
                val = vals[-1].get("value") if vals else None
                if val is not None:
                    _METRIQUE[cle] = metric
                    return val
        except Exception as e:
            print(f"  ⚠️ insights {page_id} [{metric}]: {e}")
    return None


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
    try:
        pages = _pages()
    except RuntimeError as e:
        msg = str(e)
        if "code=190" in msg or "access token" in msg.lower():
            sys.exit(
                "❌ Token Meta invalide ou EXPIRÉ.\n"
                "   → Régénère un token **longue durée** (~60 j) : Explorateur API Graph → ⓘ →\n"
                "     « Open in Access Token Tool » → « Extend Access Token », puis mets-le dans\n"
                "     le Secret GitHub META_TOKEN. (Le token de l'Explorateur dure ~1-2 h.)\n"
                f"   Détail Graph : {msg}")
        raise
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
