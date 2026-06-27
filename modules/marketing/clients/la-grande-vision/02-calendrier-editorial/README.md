# 02 — Calendrier Éditorial (90 jours · 180 contenus)

Le fichier [`calendrier-editorial.csv`](calendrier-editorial.csv) est **généré** par
`_generateur/generer.py`. Il correspond à l'**Onglet 2** du Google Sheet.

## Caractéristiques

- **Durée :** 90 jours (du 2026-07-01 au 2026-09-28).
- **Fréquence :** 2 publications / jour (08:00 et 18:30) = **180 contenus**.
- **Plateformes :** Facebook, Instagram, TikTok, LinkedIn, WhatsApp Business.
- **Équilibre des piliers :** PIL1 30 % · PIL2 20 % · PIL4 20 % · PIL3 15 % · PIL5 10 % · PIL6 5 %.

## Colonnes

`ID · Date · Heure · Plateforme · Objectif · Persona · Pilier · Sujet · Titre · Hook ·
CTA · Format · Prompt Visuel · Prompt Video · Statut`

> La colonne **Prompt Visuel** contient un extrait ; le prompt complet (Canva +
> Midjourney + GPT Image) est dans [`../03-contenus/contenus.md`](../03-contenus/contenus.md).

## Importer dans Google Sheets

1. Google Sheets → *Fichier > Importer > Importer un fichier* → déposer le CSV.
2. Séparateur : virgule. Encodage : UTF-8.
3. Figer la 1ʳᵉ ligne, mettre en forme (Onglet 2 « Calendrier Editorial La Grande Vision »).

## Workflow de statut

`À produire → En revue → Validé → Programmé → Publié` (colonne **Statut**).

## Régénérer

```bash
cd ../_generateur && python3 generer.py
```
