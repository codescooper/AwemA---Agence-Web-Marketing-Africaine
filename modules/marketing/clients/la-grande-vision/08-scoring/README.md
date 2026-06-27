# 08 — Système de Scoring automatique

Correspond à l'**Onglet 3** du Google Sheet. Note chaque contenu de **A à E** et propose
automatiquement : **À reproduire / À optimiser / À abandonner**.

Le fichier [`scoring.csv`](scoring.csv) est généré (180 lignes) avec les **formules Google
Sheets déjà écrites** dans les colonnes de score : il suffit de l'importer et de remplir les
6 colonnes de mesure.

---

## Colonnes

| Colonne | Lettre | Saisie | Description |
|---|---|---|---|
| ID | A | auto | Identifiant du contenu |
| Titre | B | auto | Titre |
| Plateforme | C | auto | Plateforme |
| Objectif | D | auto | Objectif |
| **Portée** | E | **manuelle** | Personnes atteintes |
| **Engagement** | F | **manuelle** | Likes/réactions |
| **Partages** | G | **manuelle** | Partages |
| **Commentaires** | H | **manuelle** | Commentaires |
| **Messages** | I | **manuelle** | Messages reçus (WhatsApp/DM) |
| **RDV** | J | **manuelle** | Rendez-vous générés |
| Score Engagement | K | formule | (F+G+H)/Portée ×100 |
| Score Portée | L | formule | Portée / Portée max ×100 |
| Score Conversion | M | formule | Messages / Portée ×100 |
| Score RDV | N | formule | RDV / Messages ×100 |
| Score Global | O | formule | pondéré (voir ci-dessous) |
| Note | P | formule | A → E |
| Recommandation | Q | formule | À reproduire / optimiser / abandonner |

> Les colonnes E→J sont remplies à partir des **insights natifs** (Meta/TikTok/LinkedIn) ou
> automatiquement via **PostHog** (voir `../09-automatisation/`).

---

## Formules (Google Sheets) — ligne 2, à recopier vers le bas

```text
Score Engagement   K2 = =IFERROR(ROUND(((F2+G2+H2)/MAX(E2,1))*100,1),0)
Score Portée       L2 = =IFERROR(ROUND((E2/MAX(MAX($E$2:$E$181),1))*100,1),0)
Score Conversion   M2 = =IFERROR(ROUND((I2/MAX(E2,1))*100,1),0)
Score RDV          N2 = =IFERROR(ROUND((J2/MAX(I2,1))*100,1),0)
Score Global       O2 = =ROUND(K2*0.3+L2*0.2+M2*0.25+N2*0.25,1)
Note               P2 = =IFS(O2>=80,"A",O2>=60,"B",O2>=40,"C",O2>=20,"D",TRUE,"E")
Recommandation     Q2 = =IFS(P2="A","À reproduire",OR(P2="B",P2="C"),"À optimiser",TRUE,"À abandonner")
```

### Pondération du Score Global

| Composante | Poids | Pourquoi |
|---|---|---|
| Engagement | 30 % | qualité de la résonance |
| Portée | 20 % | diffusion |
| Conversion (messages) | 25 % | intérêt commercial réel |
| RDV | 25 % | **résultat business final** |

### Barème des notes

| Note | Score global | Lecture | Action |
|---|---|---|---|
| **A** | ≥ 80 | Excellent | **À reproduire** (dupliquer le format/sujet) |
| **B** | 60–79 | Bon | À optimiser (ajuster hook/visuel) |
| **C** | 40–59 | Moyen | À optimiser (tester un angle) |
| **D** | 20–39 | Faible | Surveiller / refondre |
| **E** | < 20 | Très faible | **À abandonner** |

---

## Mise en forme conditionnelle (recommandée)

- Note A = fond vert · B = vert clair · C = jaune · D = orange · E = rouge.
- Colonne Recommandation : icônes ✅ / 🔧 / ⛔.

## Boucle d'optimisation

Chaque mois : trier par **Score Global** ↓ → les **A** alimentent les nouveaux sujets
(`_generateur/sujets.py`), les **E** sont retirés. Cette boucle est automatisée dans
[`../09-automatisation/`](../09-automatisation/).

## Régénérer
```bash
cd ../_generateur && python3 generer.py
```
