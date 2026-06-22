# AWEMA — Agence Web Marketing Africaine

> Système d'exploitation (OS) d'une agence web & marketing panafricaine, conçu pour être
> piloté de façon **holistique** par des humains **et** des agents IA.

Ce dépôt n'est pas un simple dossier de fichiers : c'est le **cerveau opérationnel** de
l'agence. Chaque département y range ses méthodes, ses templates et ses livrables clients
de façon **standardisée**, **documentée** et **réutilisable** par n'importe quel agent
(humain ou IA) qui rejoint une mission.

---

## 🎯 Principe directeur

> **Tout ce qui est produit doit pouvoir être repris, compris et ré-exécuté par un autre
> agent sans contexte préalable.**

C'est pourquoi :

- chaque dossier contient un `README.md` qui explique son rôle ;
- les méthodes sont séparées des livrables (méthode = réutilisable, livrable = spécifique
  à un client) ;
- les données volumineuses (calendriers, contenus) sont **générées par script** pour
  rester cohérentes et régénérables ;
- la charte graphique et les conventions sont centralisées et **obligatoires**.

---

## 🗂️ Structure du dépôt

```
.
├── README.md                  ← vous êtes ici (porte d'entrée)
├── AGENTS.md                  ← onboarding express pour agents IA / humains
├── docs/                      ← documentation transverse de l'agence
│   ├── 01-agence.md           ← vision, organisation, départements
│   ├── 02-onboarding.md       ← comment démarrer une mission en 10 min
│   ├── 03-conventions.md      ← nommage, structure, qualité, definition of done
│   └── 04-charte-graphique.md ← charte commune + chartes clients
│
├── departements/              ← un dossier par département de l'agence
│   └── marketing/             ← Département Marketing & Contenu
│       ├── README.md
│       ├── methodologie/      ← méthodes réutilisables (ex : production éditoriale)
│       ├── templates/         ← gabarits vierges réutilisables
│       └── clients/           ← un dossier par client
│           └── la-grande-vision/   ← MISSION 1 (cabinet d'optique, Yopougon)
│
├── outils/                    ← outils d'agence réutilisables (transverses)
│   └── revue-visuels/         ← app de revue/annotation des visuels (→ prompts)
│
└── scripts/                   ← utilitaires transverses (export PDF, etc.)
```

> 📌 Les départements à venir (Web/Dev, Design, Growth/Ads, Data, RH, Finance…) suivront
> exactement la même structure. Voir [`docs/01-agence.md`](docs/01-agence.md).

---

## 🚀 Démarrage rapide

| Vous êtes… | Lisez en priorité |
|---|---|
| Un **agent IA** assigné à une mission | [`AGENTS.md`](AGENTS.md) puis le `README.md` du département |
| Un **nouveau collaborateur** | [`docs/02-onboarding.md`](docs/02-onboarding.md) |
| Au **département Marketing** | [`departements/marketing/README.md`](departements/marketing/README.md) |
| Sur la **mission La Grande Vision** | [`departements/marketing/clients/la-grande-vision/README.md`](departements/marketing/clients/la-grande-vision/README.md) |
| À la recherche d'un **outil** (revue de visuels…) | [`outils/README.md`](outils/README.md) |

---

## 🏥 Mission en cours — La Grande Vision

**Client :** La Grande Vision — Cabinet d'optique
**Lieu :** Yopougon, Abidjan, Côte d'Ivoire
**Département pilote :** Marketing & Contenu
**Livrable :** Système marketing complet, automatisé et industrialisable (90 jours, 180 contenus, tunnel WhatsApp, CRM, automatisation).

➡️ Tout est dans [`departements/marketing/clients/la-grande-vision/`](departements/marketing/clients/la-grande-vision/).

---

## 🧭 Conventions essentielles (résumé)

1. **Français** comme langue de travail.
2. **Markdown** pour la documentation, **CSV** pour les données tabulaires, **Python** pour
   la génération.
3. Un dossier = un `README.md`.
4. La **charte graphique** (`docs/04-charte-graphique.md`) est **non négociable**.
5. Rien n'est « fini » tant que ce n'est pas conforme à la *Definition of Done*
   (`docs/03-conventions.md`).

---

_AWEMA OS — v1.0 · Première mission livrée par le Département Marketing._
