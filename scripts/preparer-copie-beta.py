#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare une COPIE D'ACCUEIL propre du dépôt pour les beta testeurs (Programme 20 CM).

Produit un dossier autonome, identique au projet MAIS :
  • sans les données réelles des clients de l'agence (RGPD + confidentialité) ;
  • avec UN client de démo neutre (le dashboard n'est pas vide) ;
  • avec une config d'agence neutre à personnaliser ;
  • registres régénérés (agence.js / config.js).

N'altère JAMAIS le dépôt courant : tout est écrit dans le dossier cible.

Usage :
  python3 scripts/preparer-copie-beta.py ../awema-beta
Puis : pousser ce dossier dans un NOUVEAU dépôt GitHub et le marquer « Template repository »
(Settings → Template repository) pour que chaque CM fasse « Use this template ».
"""
import json
import os
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

IGNORE = shutil.ignore_patterns(
    ".git", ".awema", "__pycache__", "*.pyc", "tiktok_tokens.out", "scratchpad",
    "node_modules", ".DS_Store")

CONFIG_TEMPLATE = {
    "_doc": "Configuration de TON agence. Personnalise via setup.html ou `awema setup`, "
            "puis : python3 outils/_data/build.py.",
    "nom": "Mon Agence", "nom_complet": "Mon Agence — présence en ligne",
    "tagline": "Centre de pilotage",
    "slogan": "La présence en ligne de mes clients, pilotée.",
    "initiales": "MA", "langue": "fr", "contact": "ton-email@exemple.com",
    "github": {"owner": "ton-pseudo", "repo": "mon-agence"},
    "charte": {"nuit": "#0A1F44", "ciel": "#4BA3FF", "gold": "#D4AF37",
               "violet": "#7C5CFF", "mint": "#34E5C4", "pink": "#FF7D9C"},
}

DEMO_CLIENT = {
    "id": "demo-client", "nom": "Client Démo", "secteur": "Exemple",
    "lieu": "—", "departement": "marketing", "statut": "actif", "initiales": "CD",
    "reseaux": {"facebook": "", "instagram": "", "tiktok": "", "linkedin": "",
                "whatsapp": "", "youtube": ""},
    "chemins": {"campagne": "_donnees/campagne.json", "reseaux": "_donnees/reseaux.json",
                "revue": "../../../../outils/revue-visuels/index.html?client=demo-client"},
}


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage : python3 scripts/preparer-copie-beta.py <dossier-cible>")
    cible = os.path.abspath(sys.argv[1])
    if os.path.exists(cible) and os.listdir(cible):
        sys.exit(f"❌ {cible} existe déjà et n'est pas vide. Choisis un dossier neuf.")
    print(f"→ Copie du projet vers {cible} (sans .git, .awema, données réelles)…")
    shutil.copytree(RACINE, cible, ignore=IGNORE)

    # 1) Purge des clients réels → un seul client de DÉMO riche (effet « wow » immédiat,
    #    clairement étiqueté exemple, isolé des vraies données — cf. M6)
    clients_dir = os.path.join(cible, "departements", "marketing", "clients")
    if os.path.isdir(clients_dir):
        for d in os.listdir(clients_dir):
            shutil.rmtree(os.path.join(clients_dir, d), ignore_errors=True)
    demo = os.path.join(clients_dir, "demo-client", "_donnees")
    demo_src = os.path.join(cible, "scripts", "_demo")
    if os.path.isdir(demo_src):
        shutil.copytree(demo_src, demo)            # client.json + memoire + reseaux + _agents/*
    else:                                          # repli minimal si _demo absent
        os.makedirs(demo, exist_ok=True)
        json.dump(DEMO_CLIENT, open(os.path.join(demo, "client.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

    # 2) Config d'agence neutre
    json.dump(CONFIG_TEMPLATE, open(os.path.join(cible, "config", "agence.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=2)

    # 2b) Neutralise le README du département (retire la liste des clients réels)
    rdm = os.path.join(cible, "departements", "marketing", "README.md")
    if os.path.exists(rdm):
        lignes, garde = open(rdm, encoding="utf-8").read().splitlines(), []
        for ln in lignes:
            low = ln.lower()
            if ln.startswith("| [") or (ln.startswith("## ") and "client" in low):
                break  # coupe avant la table/section des clients réels
            garde.append(ln)
        garde += ["", "## Clients", "",
                  "_Aucun client pour l'instant — ajoute le tien via `nouveau-client.html`._", ""]
        open(rdm, "w", encoding="utf-8").write("\n".join(garde))

    # 3) Suivi des places remis à zéro (aucune donnée perso ne fuit dans la copie)
    seats = os.path.join(cible, "config", "beta-seats.json")
    if os.path.exists(seats):
        try:
            s = json.load(open(seats, encoding="utf-8"))
            for p in s.get("places", []):
                p.update({"statut": "libre", "membre": "", "handle": "", "contact": "",
                          "fork": "", "rejoint_le": "", "dernier_retour": "", "notes": ""})
            s["liste_attente"] = []
            json.dump(s, open(seats, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        except Exception:
            pass

    # 4) Régénère les registres dans la copie
    print("→ Régénération des registres (build.py)…")
    subprocess.call([sys.executable, os.path.join(cible, "outils", "_data", "build.py")], cwd=cible)

    print("\n✅ Copie d'accueil prête :", cible)
    print("\nProchaines étapes :")
    print("  1. cd", cible, "&& git init && git add -A && git commit -m \"AWEMA — copie d'accueil beta\"")
    print("  2. Crée un dépôt GitHub vide, puis : git remote add origin <url> && git push -u origin main")
    print("  3. Settings → coche « Template repository » → chaque CM fait « Use this template ».")
    print("  4. Settings → Pages → branche main, dossier / (root).")
    print("  5. Partage le lien + docs/11-programme-beta.md et onboarding.html aux 20 CM.")


if __name__ == "__main__":
    main()
