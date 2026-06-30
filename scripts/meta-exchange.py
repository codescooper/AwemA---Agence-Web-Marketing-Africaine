#!/usr/bin/env python3
"""AWEMA · Échange OAuth Meta (Facebook/Instagram) côté GitHub Actions — flux 100 % Pages-native.

Déclenché par oauth.html après « Se connecter avec Facebook ». Le client_secret de l'app vit en
Secret GitHub, jamais dans le navigateur. Le script :
  1. échange le `code` contre un token court ;
  2. l'allonge en token LONGUE DURÉE (~60 j) ;
  3. l'enregistre dans la Variable META_TOKEN (lue par sync-reseaux.yml).

Entrées (env) :
  FB_CODE                code OAuth (entrée workflow)              — requis
  FB_REDIRECT            redirect_uri EXACTE (oauth.html)          — requis
  FACEBOOK_APP_ID        Secret app Meta                           — requis
  FACEBOOK_APP_SECRET    Secret app Meta                           — requis
  GH_PAT                 PAT (Variables: R/W) — AWEMA_PAT/TIKTOK_PAT — requis
  GITHUB_REPOSITORY      owner/repo (fourni par Actions)

ADN : stdlib uniquement, aucun secret écrit dans le dépôt, token jamais imprimé.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError

GRAPH = "https://graph.facebook.com/v21.0"


def _get(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            return {"error": {"message": "HTTP %s" % e.code}}


def gh(method, path, pat, data=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=(json.dumps(data).encode() if data is not None else None),
                                 headers={"Authorization": "Bearer " + pat,
                                          "Accept": "application/vnd.github+json",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, (r.read().decode() or "")


def gh_set_var(repo, pat, name, value):
    try:
        gh("PATCH", "/repos/%s/actions/variables/%s" % (repo, name), pat, {"name": name, "value": value})
    except HTTPError as e:
        if e.code == 404:
            gh("POST", "/repos/%s/actions/variables" % repo, pat, {"name": name, "value": value})
        else:
            raise


def fail(msg):
    print("::error::" + msg)
    sys.exit(1)


def main():
    app_id = (os.environ.get("FACEBOOK_APP_ID") or "").strip()
    app_secret = (os.environ.get("FACEBOOK_APP_SECRET") or "").strip()
    code = (os.environ.get("FB_CODE") or "").strip()
    redirect = (os.environ.get("FB_REDIRECT") or "").strip()
    pat = (os.environ.get("GH_PAT") or "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    if not app_id or not app_secret:
        fail("FACEBOOK_APP_ID / FACEBOOK_APP_SECRET manquants (Secrets du dépôt).")
    if not code or not redirect:
        fail("code ou redirect_uri manquant (entrées du workflow).")
    if not pat:
        fail("PAT manquant (Secret AWEMA_PAT ou TIKTOK_PAT, « Variables: Read and write »).")

    print("🔑 Échange du code Meta…")
    d = _get(GRAPH + "/oauth/access_token?" + urllib.parse.urlencode({
        "client_id": app_id, "client_secret": app_secret, "redirect_uri": redirect, "code": code}))
    short = d.get("access_token")
    if not short:
        fail("Pas de token : " + json.dumps(d.get("error") or d)[:180])

    print("⏳ Allongement en token longue durée…")
    d2 = _get(GRAPH + "/oauth/access_token?" + urllib.parse.urlencode({
        "grant_type": "fb_exchange_token", "client_id": app_id,
        "client_secret": app_secret, "fb_exchange_token": short}))
    longtok = d2.get("access_token") or short

    gh_set_var(repo, pat, "META_TOKEN", longtok)
    print("✅ META_TOKEN enregistré (Variable, ~60 j).")
    print("➡️  Lance « Sync présence digitale (réseaux) » pour découvrir toutes tes Pages.")


if __name__ == "__main__":
    main()
