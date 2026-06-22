# Outil — Dashboard AWEMA (Command Center)

Tableau de bord SaaS premium pour **piloter l'agence et les campagnes** : KPI, calendrier
éditorial, répartition par pilier/plateforme, production, scoring A→E, tunnel WhatsApp,
machine éditoriale. **Un seul fichier HTML, zéro dépendance, zéro installation.**

## Ouvrir (1 double-clic)
1. `python3 build-data.py` → génère `data.js` (campagne La Grande Vision par défaut).
2. Ouvrir `index.html` dans un navigateur.

> Autre campagne : `python3 build-data.py <chemin/campagne.json>`.

## Design (langage visuel)
- **Esthétique** : minimaliste premium, **bento grid**, **glassmorphism**, ombres douces,
  angles arrondis, contraste élevé.
- **Thème** : **dark mode natif profond** + accents électriques (bleu `#4BA3FF`,
  violet `#7C5CFF`, mint `#34E5C4`, gold `#D4AF37`) ; **thème clair** en 1 clic.
- **Typo** : Plus Jakarta Sans (titres) + Inter (texte) — repli système hors-ligne.
- **UX** : mobile-first, **Command+K** (palette de recherche globale), micro-interactions,
  **skeletons** de chargement, compteurs animés, graphiques SVG épurés (donut, aire,
  barres, anneau de progression) **sans librairie**.

## Données
Calculé sur les **180 contenus réels** de `campagne.json` (répartition piliers/plateformes,
statuts, planning 90 j, prochaines publications). Les **KPI de performance** (portée,
messages, RDV, conversion) sont des **objectifs/projections** tant que **PostHog/Meta**
ne sont pas branchés (badge « Projections » affiché).

## Reconstruire après une nouvelle génération
```bash
cd ../../departements/marketing/clients/la-grande-vision/_generateur && python3 generer.py
cd ../../../../../../outils/dashboard && python3 build-data.py
```
