# _exports-pdf — Livrables PDF

PDF professionnels générés par `scripts/export-pdf.sh` (à la racine du dépôt),
conformes à la charte (Bleu Nuit / Bleu Ciel / Gold, Montserrat + Poppins).

| Fichier | Source | Équivalent livrable |
|---|---|---|
| `01-contenus-180.pdf` | `03-contenus/contenus.md` | **Google Doc** (180 contenus) |
| `02-scripts-video.pdf` | `04-scripts-video/` | Doc scripts vidéo |
| `03-calendrier-editorial.pdf` | `02-calendrier-editorial/` | **Google Sheet** (calendrier) |
| `04-scoring.pdf` | `08-scoring/` | **Google Sheet** (scoring) |
| `05-strategie-audit.pdf` | `01-strategie/` | Doc stratégie |
| `06-personas.pdf` | `01-strategie/` | Doc personas |
| `07-tunnel-whatsapp.pdf` | `06-tunnel-whatsapp/` | Doc tunnel |
| `08-crm-relance.pdf` | `07-crm-relance/` | Doc CRM |
| `09-automatisation.pdf` | `09-automatisation/` | Doc automatisation |
| `10-presentation-direction.pdf` | `10-presentation/` | **Google Slides** |

> Régénérer : `bash scripts/export-pdf.sh` depuis la racine.
> Les PDF ne sont pas versionnés par défaut (voir `.gitignore`) ; ils sont reproductibles.
