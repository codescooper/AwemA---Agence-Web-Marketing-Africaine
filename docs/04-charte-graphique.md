# 04 — Charte Graphique

La charte est **obligatoire** : tous les visuels, slides, templates, prompts Canva et
prompts IA doivent la respecter strictement.

---

## Charte AWEMA (agence)

L'agence adopte par défaut une identité sobre et premium. Lorsqu'une mission client a sa
propre charte, **la charte client prime** sur les visuels destinés au client.

---

## Charte Client — gabarit (à remplir pour CHAQUE client)

> Duplique ce gabarit pour ton client. La **charte client prime** sur les visuels qui lui sont destinés.
> Renseigne-la aussi dans sa Mémoire Marketing (`memoire.json` → `charte`).

### Couleurs

| Rôle | Nom | HEX | Usage |
|---|---|---|---|
| Primaire | — | `#______` | Fonds, titres |
| Secondaire | — | `#______` | Accents, liens |
| Accent | — | `#______` | CTA, détails premium (≤ 10 %) |
| Neutre clair | — | `#______` | Fonds clairs, respiration |
| Neutre foncé | — | `#______` | Textes secondaires |

**Règles d'usage** : une couleur dominante (~60 %), une d'appui (~30 %), une touche d'accent (≤ 10 %).
Contraste AA minimum (accessibilité).

### Typographies

| Usage | Police | Graisses |
|---|---|---|
| Titres / Display | — | Bold / ExtraBold |
| Corps de texte | — | Regular / Medium |

Pas plus de 2 familles. Interligne aéré.

### Style, univers & signature
- Adjectifs de marque (3 à 6) : —
- Style photographique / illustratif : —
- À éviter : —
- Slogan / positionnement : —

---

## Bloc « charte » à insérer dans les prompts IA

> Adapte ce gabarit à la charte de ton client, puis copie-le dans tout prompt Canva / Midjourney / GPT Image :

```
Palette: <couleur dominante> (dominant), <couleur d'appui> (accent), <couleur premium> (details).
Typography style: <police titres> (headlines) + <police corps> (body).
Mood: <3-5 adjectifs de marque>.
Lighting: bright, soft, natural. Composition: clean, airy, generous white space.
Context: <secteur & localisation du client>.
```

> 💡 Palette par défaut (celle d'AWEMA, modifiable via `config/agence.json` → `charte`) :
> Bleu Nuit `#0A1F44` · Bleu Ciel `#4BA3FF` · Gold `#D4AF37` · Violet `#7C5CFF` · Menthe `#34E5C4` · Rose `#FF7D9C`.
