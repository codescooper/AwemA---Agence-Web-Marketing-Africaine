#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exécute un agent IA AWEMA sur un client (ou tous) et écrit sa sortie JSON additive.

Lit le manifeste `scripts/agents.json`, rassemble les entrées du client (reseaux.json,
memoire.json, campagne.json), appelle Claude via `awema_ai`, valide la sortie contre
l'enveloppe commune, puis écrit `_donnees/_agents/<agent>.json`. **Additif** : ne modifie
jamais les données réelles existantes. **Skip gracieux** sans clé IA.

Usage :
  python3 scripts/run-agent.py <agent> <slug-client>
  python3 scripts/run-agent.py <agent> --all
  python3 scripts/run-agent.py --list
"""
import glob
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)
import awema_ai  # noqa: E402

MANIFEST = os.path.join(ICI, "agents.json")


def _agents():
    return (json.load(open(MANIFEST, encoding="utf-8")) or {}).get("agents", {})


def _lire(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def _clients():
    motif = os.path.join(RACINE, "departements", "*", "clients", "*", "_donnees", "client.json")
    out = []
    for cj in sorted(glob.glob(motif)):
        out.append((json.load(open(cj, encoding="utf-8")), os.path.dirname(cj)))
    return out


def _entrees(defn, donnees):
    """Rassemble les entrées déclarées par l'agent (fichiers existants seulement)."""
    dispo, ctx = [], {}
    mapping = {"reseaux": "reseaux.json", "memoire": "memoire.json", "campagne": "campagne.json"}
    for e in defn.get("entrees", []):
        d = _lire(os.path.join(donnees, mapping.get(e, e + ".json")))
        if d is not None:
            ctx[e] = d
            dispo.append(mapping.get(e, e + ".json"))
    return ctx, dispo


def _executer(nom, defn, client, donnees):
    ctx, fichiers = _entrees(defn, donnees)
    if not ctx:
        return None, "aucune entrée disponible (rien à analyser)"
    prompt = (f"{defn.get('instruction','')}\n\n"
              f"Client : {client.get('nom')} ({client.get('secteur','')}).\n"
              f"Données disponibles (JSON) :\n{json.dumps(ctx, ensure_ascii=False)[:12000]}")
    schema_hint = ('{"items":[{"type":"...","titre":"...","explication":"...",'
                   '"preuve":{"metrique":"...","valeur":0},"action":"..."}]}')
    try:
        rep = awema_ai.chat(prompt, system=defn.get("systeme"),
                            schema_hint=schema_hint, model=defn.get("modele"))
    except Exception as e:
        return None, f"appel IA échoué : {e}"
    if rep is None:
        return None, "skip (pas de clé IA)"
    items = rep.get("items", []) if isinstance(rep, dict) else (rep if isinstance(rep, list) else [])
    env = awema_ai.enveloppe(
        nom, items, defn.get("modele") or awema_ai.DEFAULT_MODEL,
        {"client": client.get("id"), "fichiers": fichiers, "genere_par": "run-agent.py"})
    ok, err = awema_ai.valider_enveloppe(env, defn.get("item_requis"))
    if not ok:
        return None, "sortie invalide : " + " ; ".join(err[:3])
    return env, None


def _ecrire(donnees, nom, env):
    d = os.path.join(donnees, "_agents")
    os.makedirs(d, exist_ok=True)
    json.dump(env, open(os.path.join(d, nom + ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def main():
    a = sys.argv[1:]
    agents = _agents()
    if not a or a[0] == "--list":
        print("Agents disponibles :")
        for k, v in agents.items():
            print(f"  • {k:12} {v.get('role','')}")
        print("\nClé IA :", "✅ présente" if awema_ai.disponible()
              else "❌ absente → skip gracieux (aucune écriture)")
        return
    nom = a[0]
    if nom not in agents:
        sys.exit(f"❌ agent inconnu : {nom} (voir --list)")
    if not awema_ai.disponible():
        print(f"ℹ️ Pas de clé IA → agent « {nom} » ignoré (skip gracieux). Aucune écriture.")
        return
    cibles = _clients()
    if "--all" not in a:
        slug = a[1] if len(a) > 1 else None
        cibles = [(c, d) for c, d in cibles if c.get("id") == slug]
        if not cibles:
            sys.exit(f"❌ client introuvable : {slug}")
    n = 0
    for client, donnees in cibles:
        env, erreur = _executer(nom, agents[nom], client, donnees)
        if env:
            _ecrire(donnees, nom, env)
            n += 1
            print(f"  ✓ {nom} · {client.get('id')} — {len(env['items'])} item(s)")
        else:
            print(f"  · {nom} · {client.get('id')} — {erreur}")
    print(f"✅ {nom} : {n} client(s). Régénère le registre : python3 outils/_data/build.py")


if __name__ == "__main__":
    main()
