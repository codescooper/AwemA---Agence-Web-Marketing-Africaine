# 10 — Présentation Direction

[`presentation-direction.md`](presentation-direction.md) est un deck **premium de 32 slides**
au format **Marp** (Markdown → Slides/PDF), conforme à la charte (Bleu Nuit, Bleu Ciel, Gold,
Montserrat + Poppins).

## Contenu (couvre toutes les exigences)
Présentation du cabinet · Marché · Concurrence · Personas · Positionnement · Proposition de
valeur · Piliers éditoriaux · Stratégie réseaux · Calendrier · Tunnel WhatsApp ·
Automatisation · KPI/Scoring · Roadmap · Budget · Conclusion.

Chaque slide indique le **visuel recommandé** (`> 🎨 Visuel : ...`) à produire avec les
prompts de `../05-prompts-visuels/`.

## Exporter en PDF / PPTX / HTML
```bash
# nécessite Marp CLI (npx @marp-team/marp-cli)
npx @marp-team/marp-cli presentation-direction.md --pdf
npx @marp-team/marp-cli presentation-direction.md --pptx   # pour Google Slides / PowerPoint
```
Voir aussi `scripts/export-pdf.sh` à la racine du dépôt.

## Vers Google Slides
Exporter en `.pptx` puis *Importer* dans Google Slides, ou recréer les slides via le MCP
Google Drive/Slides à partir de ce plan.
