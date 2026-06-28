#!/usr/bin/env python3
"""AWEMA · Échange OAuth LinkedIn côté GitHub Actions (flux 100 % Pages-native).

Déclenché par oauth.html (workflow_dispatch) après autorisation LinkedIn. Le client_secret
vit en Secret GitHub, jamais dans le navigateur. Le script :
  1. échange le `code` contre un access_token (même appel que linkedin-onboard.py) ;
  2. enregistre l'access token dans la Variable LINKEDIN_TOKEN (lue par sync-reseaux.yml),
     et, s'il existe, le refresh_token dans LINKEDIN_REFRESH_TOKEN.

Entrées (env) :
  TT_CODE / LI_CODE      code OAuth (entrée workflow)             — requis
  TT_REDIRECT / LI_REDIRECT  redirect_uri EXACTE (oauth.html)     — requis
  LINKEDIN_CLIENT_ID     Secret app LinkedIn                      — requis
  LINKEDIN_CLIENT_SECRET Secret app LinkedIn                      — requis
  GH_PAT                 PAT (Variables: R/W) — AWEMA_PAT ou TIKTOK_PAT — requis pour écrire
  GITHUB_REPOSITORY      owner/repo (fourni par Actions)

ADN : stdlib uniquement, aucun secret écrit dans le dépôt, token jamais imprimé.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError

TOKEN = "https://www.linkedin.com/oauth/v2/accessToken"


def _post_form(url, params):
    body = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def echanger(cid, cs, code, redirect):
    d = _post_form(TOKEN, {"grant_type": "authorization_code", "code": code,
                           "redirect_uri": redirect, "client_id": cid, "client_secret": cs})
    if not d.get("access_token"):
        raise RuntimeError("réponse sans access_token : %s" % d)
    return d


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
        gh("PATCH", "/repos/%s/actions/variables/%s" % (repo, name), pat,
           {"name": name, "value": value})
    except HTTPError as e:
        if e.code == 404:
            gh("POST", "/repos/%s/actions/variables" % repo, pat, {"name": name, "value": value})
        else:
            raise


def fail(msg):
    print("::error::" + msg)
    sys.exit(1)


def main():
    cid = (os.environ.get("LINKEDIN_CLIENT_ID") or "").strip()
    cs = (os.environ.get("LINKEDIN_CLIENT_SECRET") or "").strip()
    code = (os.environ.get("LI_CODE") or os.environ.get("TT_CODE") or "").strip()
    redirect = (os.environ.get("LI_REDIRECT") or os.environ.get("TT_REDIRECT") or "").strip()
    pat = (os.environ.get("GH_PAT") or "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    if not cid or not cs:
        fail("LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET manquants (Secrets du dépôt).")
    if not code or not redirect:
        fail("code ou redirect_uri manquant (entrées du workflow).")
    if not pat:
        fail("PAT manquant (Secret AWEMA_PAT ou TIKTOK_PAT, « Variables: Read and write »).")

    print("🔑 Échange du code LinkedIn…")
    d = echanger(cid, cs, code, redirect)
    access = d["access_token"]
    exp = d.get("expires_in")
    gh_set_var(repo, pat, "LINKEDIN_TOKEN", access)
    msg = "✅ LINKEDIN_TOKEN enregistré (Variable)"
    if exp:
        msg += " · valable ~%d j" % (int(exp) // 86400)
    if d.get("refresh_token"):
        gh_set_var(repo, pat, "LINKEDIN_REFRESH_TOKEN", d["refresh_token"])
        msg += " · refresh_token conservé"
    print(msg + ".")
    print("➡️  Lance « Sync présence digitale (réseaux) » pour récupérer les stats LinkedIn.")


if __name__ == "__main__":
    main()
