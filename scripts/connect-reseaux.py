#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connecteur « présence digitale » → écrit reseaux.json (données RÉELLES).

Remplit le contrat outils/_data (reseaux.json) d'un client à partir des réseaux
sociaux. Deux voies :

  1) META GRAPH API (Facebook Page + Instagram Business)
     Requiert un token d'accès (Page/IG) avec les permissions de lecture insights.
     export META_TOKEN="EAAB..."   export FB_PAGE_ID="..."   export IG_USER_ID="..."

  2) IMPORT MANUEL (CSV exporté depuis Meta Business Suite / TwoMinuteReports / autre)
     python3 connect-reseaux.py --manuel <client_dir> <export.csv>

Aucune donnée inventée : si une source est absente, les champs restent null.
Le réseau du sandbox peut bloquer les appels externes → lancer ce script depuis
une machine ayant accès à graph.facebook.com.

Usage :
  python3 connect-reseaux.py --meta departements/marketing/clients/la-grande-vision
  python3 connect-reseaux.py --manuel <client_dir> <export.csv>
"""
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

GRAPH = "https://graph.facebook.com/v21.0"


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
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


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


def main():
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "--meta":
        via_meta(a[1])
    elif len(a) >= 3 and a[0] == "--manuel":
        via_manuel(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
