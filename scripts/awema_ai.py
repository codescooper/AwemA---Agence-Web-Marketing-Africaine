#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client IA AWEMA — appel Claude (Anthropic) en *stdlib*, avec skip gracieux sans clé.

ADN respecté : aucune dépendance pip, aucun secret dans le dépôt. La clé vient de
l'environnement `ANTHROPIC_API_KEY` ou du store local `.awema/` (géré par l'opérateur).
Sans clé → tout s'auto-désactive proprement (`disponible()` → False, `chat()` → None),
pour que la CI et l'usage hors-ligne restent verts.

Brique de base des agents IA (cf. docs/PRD-AWEMA.md §3, ADR-001).
"""
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = os.environ.get("AWEMA_AI_MODEL", "claude-sonnet-4-6")
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _key():
    """Clé API : env d'abord, puis store local .awema (plateforme 'claude'/'anthropic')."""
    k = os.environ.get("ANTHROPIC_API_KEY")
    if k:
        return k.strip()
    try:
        store = json.load(open(os.path.join(RACINE, ".awema", "credentials.json"), encoding="utf-8"))
        for p in (store.get("platforms") or {}).values():
            cur = p.get("current") or {}
            for name in ("ANTHROPIC_API_KEY", "CLAUDE_API_KEY"):
                if cur.get(name):
                    return str(cur[name]).strip()
    except Exception:
        pass
    return None


def disponible():
    """Vrai si une clé est configurée (donc si les agents IA peuvent tourner)."""
    return bool(_key())


def _extraire_json(texte):
    """Extrait le premier objet/tableau JSON d'une réponse (robuste aux préambules)."""
    texte = (texte or "").strip()
    # bloc ```json ... ```
    m = re.search(r"```(?:json)?\s*(.+?)```", texte, re.S)
    if m:
        texte = m.group(1).strip()
    try:
        return json.loads(texte)
    except Exception:
        pass
    for ouvre, ferme in (("{", "}"), ("[", "]")):
        i, j = texte.find(ouvre), texte.rfind(ferme)
        if i != -1 and j > i:
            try:
                return json.loads(texte[i:j + 1])
            except Exception:
                continue
    return None


def chat(user, system=None, schema_hint=None, model=None, max_tokens=2000):
    """Appelle Claude. Renvoie le texte, ou (si schema_hint) un objet JSON parsé.
    Renvoie None si pas de clé (skip gracieux). Lève RuntimeError sur erreur API réelle."""
    key = _key()
    if not key:
        return None
    model = model or DEFAULT_MODEL
    contenu = user
    if schema_hint:
        contenu += ("\n\nRéponds UNIQUEMENT avec un JSON valide conforme à ce schéma "
                    f"(pas de texte autour) :\n{schema_hint}")
    payload = {"model": model, "max_tokens": max_tokens,
               "messages": [{"role": "user", "content": contenu}]}
    if system:
        payload["system"] = system
    req = urllib.request.Request(
        API_URL, data=json.dumps(payload).encode("utf-8"),
        headers={"x-api-key": key, "anthropic-version": API_VERSION,
                 "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        msg = body
        try:
            msg = json.loads(body).get("error", {}).get("message", body)
        except Exception:
            pass
        raise RuntimeError(f"HTTP {e.code} — {msg}") from None
    blocs = data.get("content") or []
    texte = "".join(b.get("text", "") for b in blocs if b.get("type") == "text")
    if schema_hint:
        return _extraire_json(texte)
    return texte


# --------------------------------------------------------------------------- #
# Enveloppe commune des sorties d'agents + validation (partagée run-agent / tests)
# --------------------------------------------------------------------------- #
def enveloppe(agent, items, modele, provenance):
    """Construit la sortie standard d'un agent (cf. PLAN-EXECUTION-BETA, schéma commun)."""
    return {
        "agent": agent,
        "genere_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "modele": modele,
        "provenance": provenance or {},
        "items": list(items or []),
    }


def valider_enveloppe(obj, item_requis=None):
    """Valide la forme commune. Renvoie (ok: bool, erreurs: [str])."""
    err = []
    if not isinstance(obj, dict):
        return False, ["la sortie n'est pas un objet"]
    for k in ("agent", "genere_le", "modele", "provenance", "items"):
        if k not in obj:
            err.append(f"clé manquante : {k}")
    if "items" in obj and not isinstance(obj["items"], list):
        err.append("items doit être une liste")
    if "provenance" in obj and not isinstance(obj["provenance"], dict):
        err.append("provenance doit être un objet")
    for n, it in enumerate(obj.get("items", []) if isinstance(obj.get("items"), list) else []):
        if not isinstance(it, dict):
            err.append(f"items[{n}] n'est pas un objet")
            continue
        for k in (item_requis or []):
            if k not in it:
                err.append(f"items[{n}] : clé requise manquante « {k} »")
    return (len(err) == 0), err


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        print("✅ Clé IA détectée — agents activés." if disponible()
              else "ℹ️ Aucune clé IA (ANTHROPIC_API_KEY) — agents désactivés (skip gracieux).")
        print("Modèle par défaut :", DEFAULT_MODEL)
    else:
        print(__doc__)
