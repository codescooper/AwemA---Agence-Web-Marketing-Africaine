# _generateur — Machine éditoriale

Scripts Python **déterministes** qui produisent les livrables de volume.

| Fichier | Rôle |
|---|---|
| `generer.py` | Moteur : calendrier, contenus, scripts vidéo, scoring |
| `sujets.py` | Banque de sujets par pilier (facile à enrichir) |

## Lancer
```bash
python3 generer.py
```

## Ce qui est généré (chemins relatifs au dossier client)
- `02-calendrier-editorial/calendrier-editorial.csv` (180 lignes)
- `03-contenus/contenus.md` (180 fiches)
- `04-scripts-video/scripts-video.md` (60 scripts)
- `08-scoring/scoring.csv` (180 lignes + formules Google Sheets)

## Étendre / personnaliser
- **Ajouter des sujets** : éditer `sujets.py` (listes par pilier).
- **Changer les gabarits de texte/prompt** : éditer les fonctions de `generer.py`.
- **Changer la cadence / les dates** : constantes en haut de `generer.py`.

Aucune dépendance externe (Python 3 standard).
