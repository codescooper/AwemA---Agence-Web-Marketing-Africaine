---
titre: PROJECT_SELF_DESCRIPTION — Mémoire permanente d'AWEMA OS
objet: Contexte complet, autoportant, destiné à un autre LLM pour reprendre le projet sans lire le dépôt.
genere_le: 2026-06-27
fidelite: "Faits tirés du dépôt + déductions explicitement étiquetées « DÉDUCTION »."
---

# AWEMA OS — Auto-description exhaustive (mémoire permanente)

> **Comment lire ce document.** Il est conçu pour être lu seul, sans accès au dépôt. Tout ce qui est
> affirmé comme un fait provient de la lecture directe des fichiers. Tout ce qui est une interprétation
> est précédé de **DÉDUCTION** et justifié. Les noms de fichiers, commandes, clés JSON et identifiants
> sont cités **tels quels** pour être réutilisables.
>
> **Avertissement de cohérence.** Le projet a connu un **repositionnement majeur** (juin 2026) : d'un
> « système d'exploitation d'une agence marketing » (couches `README.md`, `AGENTS.md`, `departements/`)
> vers un « **système d'exploitation d'une agence digitale assistée par IA** » (couches `docs/PRD-AWEMA.md`,
> agents IA, landing produit, programme bêta). **Les deux couches coexistent dans le dépôt** ; certaines
> incohérences en découlent et sont signalées en §14–15.

---

# 1. Vision du projet

## Pourquoi le projet existe
AWEMA (Agence Web Marketing Africaine) est le **système d'exploitation d'une agence digitale assistée
par IA**. Ce n'est pas un dossier de fichiers ni un simple tableau de bord : c'est le **cerveau
opérationnel** d'une agence, pensé pour être piloté **holistiquement par des humains ET des agents IA**,
et pour être **forké et réutilisé** par n'importe quelle agence.

Le principe directeur (cité de `README.md`) : **« Tout ce qui est produit doit pouvoir être repris,
compris et ré-exécuté par un autre agent sans contexte préalable. »**

## Quel problème il résout
Un community manager / une petite agence gère la présence en ligne de **nombreux clients** éparpillés
sur plusieurs réseaux (Facebook, Instagram, TikTok, YouTube, LinkedIn, WhatsApp). Le problème :
- jongler entre des dizaines de comptes et de tableaux de bord natifs ;
- ne pas savoir **pourquoi** un contenu marche, ni **quoi faire** ensuite ;
- perdre des heures en analyse, planification et production de contenu ;
- dépendre d'un SaaS coûteux qui détient les données.

AWEMA agrège **toute** la présence d'une entité au même endroit (**données réelles, zéro fiction**) et
fait **travailler une équipe d'agents IA** qui observent, analysent, **proposent** et préparent — au
lieu de simplement répondre. Le différenciateur, cité de `PRD-AWEMA.md` : ❌ avant « agréger plusieurs
réseaux » → ✅ désormais **« faire travailler une équipe d'agents IA spécialisés »**. Formule clé :
**« L'IA ne répond pas. Elle travaille. »** et **« AWEMA propose »** (vs « on consulte »).

## Pour qui
- **Cible primaire** : community managers et **petites agences digitales ouest-africaines** (le projet
  est conçu et illustré en Côte d'Ivoire — Abidjan, Yopougon) gérant plusieurs clients TPE/PME
  (restaurants, optique, créateurs de contenu, associations, e-commerce…).
- **Cible secondaire** : tout indépendant/agence voulant **auto-héberger** un cockpit de pilotage
  social sans SaaS, et le personnaliser à sa marque.
- **Public technique** : agents IA (comme Claude Code) opérant le système en langage naturel, et
  développeurs forkant la base.

---

# 2. Mission

Donner à chaque agence un **centre de commandement proactif**, auto-hébergé et à sa marque, qui :
1. **réunit** toute la présence en ligne réelle de ses clients (multi-réseaux, fusionnée) ;
2. **fait travailler des agents IA spécialisés** (Analyste, Stratège, Créatif, Proactivité…) qui
   produisent des **propositions sourcées et actionnables** ;
3. reste **100 % la propriété de l'agence** (données chez elle, zéro dépendance SaaS, fork & config) ;
4. permet à un pilote d'atteindre son **premier « wow » en moins de 30 minutes** (onboarding → données
   réelles → première recommandation IA).

Promesse pilote (citée du PRD) : en ouvrant le cockpit, l'agence comprend immédiatement « **je gagne
plusieurs heures par semaine** ». Devise produit : **« Qualité > quantité. Peu de fonctionnalités,
extrêmement bien finies. »**

---

# 3. Valeur apportée

| Pour qui | Valeur concrète |
|---|---|
| **CM / agence** | Une vue unique multi-réseaux **réelle** ; gain de temps ; l'IA dit *pourquoi* et *quoi faire* ; production de contenu en 1 clic ; instance à sa marque ; données privées. |
| **Client final** | Présence pilotée avec régularité, community management réactif, contenu cohérent avec sa charte et ses personas. |
| **Agent IA** | Un dépôt entièrement documenté, conventionné, déterministe : il peut reprendre une mission sans contexte, produire des artefacts JSON additifs, et opérer les connexions en langage naturel. |
| **Écosystème** | Modèle **forkable** : chaque agence héberge sa copie ; pas de point central ; base réutilisable. |

Différenciateurs revendiqués : **agrégation multi-réseaux réelle** + **community management** intégré +
**opérateur IA en langage naturel** + **équipe d'agents IA proactive** + **auto-hébergement sans SaaS**.

---

# 4. Philosophie

## ADN — invariants non négociables (cités de `PRD-AWEMA.md` / `AWEMA-OS.md`)
1. **Auto-hébergement** — chaque agence forke et héberge **sa** propre instance ; **zéro SaaS** central.
2. **Git = source de vérité** — l'état vit dans des fichiers JSON versionnés, pas dans une base de données.
3. **GitHub Pages** — le front est servi en statique (`.nojekyll`, depuis la racine).
4. **HTML / CSS / JS vanilla** — aucune dépendance front, fichiers autonomes, exécutables en `file://`.
5. **Python stdlib uniquement** — les scripts n'utilisent que la bibliothèque standard (urllib, json…).
   *(Exception assumée : `html2pdf.py` qui requiert Playwright/Chromium — un utilitaire hors cœur.)*
6. **Données réelles, zéro fiction** — on n'invente jamais une métrique ; un agent **annote** la donnée
   réelle et étiquette ses sorties « proposition IA ».
7. **Aucun secret dans le dépôt** — jamais. Les secrets vivent dans GitHub Secrets/Variables ou le
   store local `.awema/` (gitignoré, `chmod 600`).
8. **Fork simple + personnalisation par config** — un seul fichier `config/agence.json` repersonnalise
   toute l'instance.
9. **Opérateur IA en langage naturel** — `/awema` connecte/maintient les plateformes ; ne demande que
   ce qui est inconnu.

## Décision d'architecture fondatrice — ADR-001
**« Agents = jobs, JSON = vérité, cockpit = renderer ».** C'est le pivot qui réconcilie « équipe
d'agents IA » avec l'ADN :
- un **agent** = un **script Python** (stdlib + **un** appel HTTPS LLM) déclenché par **GitHub Actions**
  (planifié / `workflow_dispatch`) **ou** localement via l'opérateur `/awema`. L'agent **est** le
  back-end : éphémère, sans serveur permanent ;
- **entrées** : `memoire.json`, `reseaux.json`, `campagne.json` (et plus tard `marche.json`) ;
- **sorties** : des **artefacts JSON déterministes additifs** dans `_donnees/_agents/<agent>.json` —
  les agents **ne modifient jamais** `reseaux.json` → **zéro régression** sur la donnée réelle ;
- **cockpit statique** : lit ces artefacts et les **rend proactivement** ;
- **humain dans la boucle** : les sorties sont des **propositions** horodatées et **sourcées** ;
  l'humain valide/rejette → réécrit le JSON.

Conséquence : ajouter de l'IA **n'introduit qu'un seul secret** (une clé LLM) et **aucun serveur**.

## Conventions de travail (citées de `docs/03-conventions.md`, `AGENTS.md`)
- **Langue** : français (travail et livraison).
- **Nommage** : `kebab-case`, **sans accents**, sans espaces. Préfixe numérique pour l'ordre
  (`00-brief`, `01-strategie`…). Dossiers techniques préfixés `_` (`_generateur/`, `_donnees/`,
  `_agents/`, `_exports-pdf/`).
- **Un dossier = un `README.md`** décrivant rôle, contenu, régénération.
- **Méthode ≠ livrable** : la méthode réutilisable va dans `methodologie/` ou `templates/` ; le livrable
  spécifique dans `clients/<client>/`.
- **Industrialiser le volume** : au-delà de ~20 éléments répétitifs, écrire un **générateur déterministe**
  (`_generateur/`) plutôt que copier-coller. *« Le générateur EST le livrable de fond. »*
- **Definition of Done** : rangé · documenté · conforme à la charte · cohérent avec la stratégie ·
  directement exploitable (zéro placeholder/TODO) · porteur d'un KPI · régénérable par script.
- **Git** : branches de travail dédiées (ex. `claude/...`) ; commits en français ; **aucune PR sans
  demande explicite**.

---

# 5. Architecture générale

## Vue d'ensemble du flux de données
```
config/agence.json ──► build.py ──► outils/_data/config.js (window.AWEMA_CONFIG) ──┐
config/ia-providers.json ─► build.py ─► outils/_data/ia-providers.js ──────────────┤
departements/<dept>/clients/<client>/_donnees/                                      │
   ├─ client.json (obligatoire)                                                     │
   ├─ reseaux.json (présence réelle)        ──► build.py ──► outils/_data/agence.js │
   ├─ memoire.json (Mémoire Marketing)                       (window.AWEMA_REGISTRY)│
   ├─ campagne.json (plan éditorial)                                                │
   └─ _agents/<agent>.json (sorties IA)                                             │
                                                                                    ▼
                          Pages HTML statiques + outils (apply.js applique la marque)
                          index.html · dashboard · revue-visuels · onboarding · connect-*
                                                                                    ▼
                                   Navigateur (100 % statique, zéro serveur)

Alimentation des données réelles (hors-ligne, via Internet) :
  GitHub Actions / opérateur /awema ──► connect-reseaux.py ──► reseaux.json
  GitHub Actions / opérateur /awema ──► run-agent.py ──► _agents/*.json
```

## Arborescence complète et rôle de chaque dossier
```
/                                  Racine = sert GitHub Pages (statique)
├── README.md                      Porte d'entrée (couche « OS d'agence » historique)
├── AGENTS.md                      Onboarding express pour agents IA & humains
├── AWEMA OS — v1.0
│
├── docs/                          Documentation transverse + référence produit (la couche « OS IA »)
│   ├── 00-INDEX.md                MOC Obsidian (point d'entrée admin)
│   ├── 01-agence.md … 04-charte-graphique.md   Vision, onboarding, conventions, charte
│   ├── 05-…-10-connecter-linkedin.md           Guides de connexion par plateforme
│   ├── 11-programme-beta.md       Conditions & prérequis du programme bêta
│   ├── 12-connecter-ia.md         Brancher une IA (options gratuites)
│   ├── 13-securite-donnees.md     Isolation des données, secrets, RGPD
│   ├── 14-acces-api-agence.md     Accès API « dev entreprise » (modèles A / B)
│   ├── ACCES-AGENCE.md            Page de contrôle admin (donner/retirer accès, licence)
│   ├── AUTO-DESCRIPTION.md        Auto-description antérieure (analyse externe)
│   ├── AWEMA-OS.md                Note maîtresse : vision + journal + état
│   ├── PRD-AWEMA.md               North Star produit (référence d'architecture)
│   ├── ROADMAP.md                 Feuille de route — SOURCE UNIQUE
│   ├── PLAN-EXECUTION-BETA.md     Plan module par module M0→M6 (zéro régression)
│   └── email-bienvenue.md         Modèle d'email aux agences acceptées
│
├── departements/                  Un dossier par département de l'agence
│   └── marketing/                 SEUL département actif (6 autres « à venir » : Web, Design, Ads, Data, CRM, Direction)
│       ├── README.md
│       ├── methodologie/          Méthode Universelle de Production Éditoriale (10 phases)
│       ├── templates/             Gabarits vierges : persona, fiche-contenu, script-video, calendrier, scoring
│       └── clients/               27 CLIENTS RÉELS, un dossier chacun
│           ├── <client-simple>/_donnees/{client,reseaux}.json [+ _agents/actions-du-jour.json]
│           └── la-grande-vision/  Mission 1 complète (pipeline éditorial 00→10 + _generateur + _exports-pdf)
│
├── outils/                        Outils web réutilisables (transverses, 100 % statiques)
│   ├── README.md
│   ├── _data/                     COUCHE DE DONNÉES : registre généré
│   │   ├── build.py               Scanne departements/ + config/ → génère les .js
│   │   ├── agence.js              window.AWEMA_REGISTRY (clients + licence)   [GÉNÉRÉ]
│   │   ├── config.js              window.AWEMA_CONFIG (branding)              [GÉNÉRÉ]
│   │   ├── ia-providers.js        window.AWEMA_IA_PROVIDERS                   [GÉNÉRÉ]
│   │   ├── platforms.js           window.AWEMA_PLATFORMS (charte par réseau)  [statique]
│   │   └── apply.js               Applique la marque à toute page [data-ag], réécrit liens GitHub
│   ├── _design/                   DESIGN SYSTEM « AWEMA UI »
│   │   ├── awema-ui.css           Tokens couleurs/typo + composants (.card .btn .bento …)
│   │   └── awema-ui.js            ic()/injectIcons()/toast()/initTheme()/countUp()/copy()
│   ├── dashboard/                 COMMAND CENTER (cockpit multi-clients)
│   │   ├── index.html             Cockpit (bento, SVG charts sans lib, Command+K, ?client=)
│   │   ├── build-data.py          campagne.json → data.js
│   │   └── data.js                window.CAMPAGNE [GÉNÉRÉ]
│   └── revue-visuels/             VISUALISEUR (revue/annotation des visuels → prompts)
│       ├── index.html             3 colonnes (liste filtrable / aperçu / métadonnées+prompts)
│       ├── build-data.py          campagne.json → data.js
│       ├── data.js                [GÉNÉRÉ]
│       └── INTEGRATION-GENERATION-IMAGE.md   3 méthodes pour générer une image depuis un prompt
│
├── scripts/                       Cœur logique (Python stdlib) + manifestes
│   ├── awema.py                   OPÉRATEUR : connexions, licence, accès, attente, clients, setup
│   ├── awema_ai.py                CLIENT IA AGNOSTIQUE (Anthropic + OpenAI-compatibles), skip gracieux
│   ├── run-agent.py               Exécute les agents → _agents/*.json ; aggreger_actions() déterministe
│   ├── connect-reseaux.py         CONNECTEUR présence (Meta/TikTok/YouTube/LinkedIn) → reseaux.json
│   ├── agents.json                MANIFESTE des agents IA (analyste, stratege, creatif)
│   ├── awema-connectors.json      MANIFESTE des connecteurs (meta, tiktok, youtube, linkedin, whatsapp, ia)
│   ├── tiktok-onboard.py          Assistant OAuth TikTok (capture code + rotation refresh tokens)
│   ├── linkedin-onboard.py        Assistant OAuth LinkedIn (génère LINKEDIN_TOKEN)
│   ├── generer-image-openai.py    Génération d'image via OpenAI Images (hors cœur bêta)
│   ├── preparer-copie-beta.py     Crée une COPIE D'ACCUEIL propre (0 donnée réelle, 1 client démo)
│   ├── csv2html.py / md2html.py / html2pdf.py / export-pdf.sh   Pipeline d'export PDF (utilitaires)
│   ├── reseaux-ignore.json        Pages Facebook à exclure de la synchro
│   └── _demo/                     Client de DÉMO « Éclat Beauté » (client+memoire+reseaux+_agents/*)
│
├── config/                        Configuration de l'instance
│   ├── agence.json                Branding/charte/fork (POINT UNIQUE de personnalisation)
│   ├── aliases.json               Rattache un compte (clé de token) à une fiche canonique
│   ├── ia-providers.json          Registre des fournisseurs d'IA (gratuits mis en avant)
│   ├── beta-seats.json            Suivi des 20 places du programme bêta + liste_attente
│   └── licence.json               Activation de l'instance (statut + clé)
│
├── tests/                         Harnais anti-régression (unittest stdlib) — ~29 tests
│   └── test_{merge,consolidation,schemas,memoire,ia,licence,actions}.py + util.py
│
├── .github/
│   ├── workflows/                 tests.yml · agents.yml · sync-reseaux.yml · sync-tiktok.yml
│   └── ISSUE_TEMPLATE/            1-retour-beta.yml · 2-bug.yml · 3-idee.yml · config.yml
│
├── .claude/commands/awema.md      Définition du skill /awema (opérateur en langage naturel)
├── .obsidian/                     Ouvre le dépôt comme coffre Obsidian (accueil = docs/00-INDEX.md)
├── .awema/                        Store local PRIVÉ (gitignoré) : credentials + registres (preuve)
│
├── index.html                     LANDING produit (animée, chiffres réels, CTAs liste d'attente)
├── onboarding.html                Parcours pilote en 4 étapes (anneau de progression localStorage)
├── setup.html                     Personnaliser l'agence → config/agence.json
├── nouveau-client.html            Créer la fiche d'un client → client.json
├── memoire.html                   Éditer la Mémoire Marketing → memoire.json
├── liste-attente.html             Liste d'attente du lancement (sur abonnement) → mailto + merci.html
├── merci.html                     Confirmation après inscription
├── rejoindre.html                 Candidature au programme bêta (20 places) → mailto
├── demande-acces.html             Demande d'accès API managé (modèle B) → mailto
├── connect-{facebook,tiktok,youtube,linkedin,whatsapp,ia}.html   Guides pas à pas
├── oauth.html                     Callback OAuth (TikTok/LinkedIn) : affiche/copie le code
└── legal/{terms,privacy}.html     Mentions légales
```

## Rôle des sous-dossiers `_donnees/` (par client)
| Fichier | Contenu | Requis |
|---|---|---|
| `client.json` | Profil : `id`, `nom`, `secteur`, `lieu`, `departement`, `statut`, `initiales`, `reseaux{facebook,instagram,tiktok,linkedin,whatsapp,youtube}`, `chemins{campagne,reseaux,revue}`, optionnels `fb_page_id`/`yt_handle`/`yt_channel_id`. | ✅ (pour être listé) |
| `reseaux.json` | Présence réelle consolidée multi-réseaux (voir schéma §6). | optionnel |
| `memoire.json` | Mémoire Marketing : identité, ton, personas, produits, FAQ… | optionnel |
| `campagne.json` | Plan éditorial (`total`, `contenus[]`). | optionnel |
| `_agents/<agent>.json` | Sorties additives des agents (analyste/stratege/creatif/actions-du-jour). | optionnel |

## Dépendances
- **Runtime front** : aucune (HTML/CSS/JS vanilla, fonctionne en `file://` et GitHub Pages).
- **Runtime back** : Python 3 **stdlib uniquement** pour le cœur (`awema.py`, `awema_ai.py`,
  `run-agent.py`, `connect-reseaux.py`, `build.py`, onboarders, tests).
- **Exceptions hors cœur** : `html2pdf.py` (Playwright + Chromium), `export-pdf.sh` (Marp CLI optionnel),
  `generer-image-openai.py` (clé OpenAI payante).
- **Services externes (HTTP)** : Meta Graph API v21, TikTok Display API v2, YouTube Data API v3,
  LinkedIn Community Management/REST API, OpenAI Images API, et un LLM au choix (Anthropic ou
  OpenAI-compatible) via `awema_ai.py`.
- **Plateforme** : GitHub (Pages, Actions, Secrets/Variables, Issues).

---

# 6. Flux de travail

## Schéma exact de `reseaux.json` (présence réelle consolidée)
```json
{
  "connecte": true,
  "source": "tiktok-display-api | meta-graph-api | youtube-data-api | linkedin-rest-api | manuel",
  "maj": "ISO-8601",
  "client": "<slug>",
  "global": { "audience", "posts", "likes", "commentaires", "partages", "portee", "vues", "engagement_taux" },
  "par_reseau": {
    "facebook|instagram|tiktok|linkedin|youtube": { "abonnes","posts","likes","commentaires","partages","portee","vues" }
  },
  "reactions": { "like","love","care","haha","wow","sad","angry" },           // Facebook
  "cadence": { "dernier_post","jours_depuis","posts_30j","posts_par_semaine","dernier_reseau","multi_reseaux" },
  "meilleur_creneau": { "jour","heure","par_jour{Lundi..Dimanche}","recommandation" },
  "types_contenu": { "<type>": { "n","engagement_moyen" } },
  "a_repondre": { "total", "exemples[]" },
  "top_commentateurs": [], "top_fans": [],
  "top_posts": [ { "titre","plateforme","date","lien","likes","commentaires","partages","vues","type" } ],
  "evolution_audience": [ { "date","valeur" } ],
  "tiktok": {…}, "youtube": {…}, "linkedin": {…}                              // blocs spécifiques par plateforme
}
```
`portee` est quasi toujours `null` : **dégradation gracieuse** consécutive à la **dépréciation des
insights Meta en v21** (seul `page_views_total` survit). Le `cadence` est **multi-réseaux** :
`dernier_reseau` indique d'où vient la dernière publication parmi tous les réseaux.

## Comment un humain utilise AWEMA OS (cycle complet)
1. **Forker & personnaliser** : `setup.html` (ou `awema setup …`) écrit `config/agence.json` ;
   `python3 outils/_data/build.py` régénère le branding. Activer GitHub Pages (branche `main`, `/`).
2. **Ajouter un client** : `nouveau-client.html` (ou `awema client new …`) crée `client.json`.
3. **Renseigner la Mémoire Marketing** : `memoire.html` (ou `awema client memoire …`) crée `memoire.json`.
4. **Connecter les réseaux** : guides `connect-*.html` → obtenir tokens → les placer en GitHub Secrets
   (ou store local) → `connect-reseaux.py --meta-all/--tiktok-all/--youtube-all/--linkedin-all` remplit
   `reseaux.json`. En automatique, les workflows `sync-reseaux.yml`/`sync-tiktok.yml` le font (lundi).
5. **Brancher une IA** (optionnel) : `connect-ia.html` → clé d'un fournisseur (gratuit possible).
6. **Faire travailler les agents** : `run-agent.py analyste|stratege|creatif --all` (workflow
   `agents.yml`, quotidien) → `_agents/*.json`. Sans clé IA, **skip gracieux**.
7. **Piloter** : ouvrir le **dashboard** ; en tête, le feed **« 3 choses à faire aujourd'hui »** ; par
   client, panneaux « Pourquoi & Que faire » (Analyste), « Plan recommandé » (Stratège), « Idées prêtes »
   (Créatif). Valider/rejeter les propositions.

## Comment un agent IA travaille (ADR-001, détail d'exécution)
`run-agent.py <agent> <slug|--all>` →
1. lit le manifeste `agents.json` (rôle, `entrees`, `modele`, `systeme`, `instruction`, `schema_hint`,
   `liste`, `item_requis`, `champs_sortie`) ;
2. rassemble les **entrées disponibles** du client (`reseaux.json`, `memoire.json`, `campagne.json`) ;
3. construit le prompt et appelle `awema_ai.chat(...)` (un seul appel LLM) ;
4. **valide** la sortie contre l'enveloppe commune (`valider_enveloppe`) ;
5. écrit `_donnees/_agents/<agent>.json` (**additif**, ne touche jamais `reseaux.json`).

Enveloppe commune (sortie de tout agent) :
`{ "agent", "genere_le", "modele", "provenance":{client,fichiers,genere_par}, "items":[…] }`
(+ champs structurés supplémentaires déclarés via `champs_sortie`, ex. `cadence_recommandee`).

## Comment l'humain intervient (boucle de validation)
Les sorties d'agents sont des **propositions** étiquetées « proposition IA », horodatées et **sourcées**
(chaque insight cite une **preuve** = métrique réelle). L'humain les lit dans le cockpit, puis
**valide/rejette**. Les actions destructrices ou engageantes (ex. écrire dans `campagne.json` depuis le
Créatif) **n'ont lieu que sur validation humaine explicite**.

## Cycle complet (boucle vertueuse)
```
Connexion réseaux → reseaux.json (réel)
        ↓
Agents IA (Analyste/Stratège/Créatif) → _agents/*.json (propositions sourcées)
        ↓
Agrégateur Proactivité (déterministe) → actions-du-jour.json (« 3 choses à faire »)
        ↓
Humain valide → contenu produit → publié → mesuré (re-sync)
        ↺  (les nouvelles données réelles nourrissent le tour suivant)
```

---

# 7. Conventions (toutes celles découvertes)

- **Langue** : français partout (UI, docs, commits).
- **Nommage fichiers/dossiers** : `kebab-case` sans accents ni espaces ; préfixe numérique d'ordre
  (`00-…`, `01-…`) ; dossiers techniques préfixés `_`.
- **Un dossier = un `README.md`** obligatoire.
- **Méthode vs livrable** : séparés (`methodologie/`/`templates/` vs `clients/<client>/`).
- **Industrialisation** : générateur déterministe dès ~20 éléments répétitifs.
- **Slug** : identifiant de dossier client (ex. `code-scooper`) ; doit correspondre à la clé dans
  `TIKTOK_TOKENS` et aux alias (`config/aliases.json`).
- **Fichiers générés** (ne jamais éditer à la main) : `outils/_data/agence.js`, `config.js`,
  `ia-providers.js`, `outils/dashboard/data.js`, `outils/revue-visuels/data.js`.
- **Personnalisation par attribut** : éléments HTML marqués `data-ag="nom|initiales|tagline|…"` sont
  remplis par `apply.js` depuis `window.AWEMA_CONFIG`.
- **Paramètre d'URL** `?client=<id>` : sélectionne un client (dashboard, memoire).
- **Secrets** : jamais dans le dépôt ; GitHub Secrets/Variables + `.awema/` (gitignoré, `chmod 600`).
- **Données privées (RGPD)** : la liste d'attente et les registres de preuve vivent dans `.awema/`
  (hors git) ; `config/beta-seats.json` ne doit contenir que pseudo/handle + contact minimal.
- **Git** : branches de travail `claude/...` ; commits français descriptifs ; pas de PR sans demande.
- **Charte graphique non négociable** : couleurs AWEMA — Bleu Nuit `#0A1F44`, Bleu Ciel `#4BA3FF`,
  Gold `#D4AF37`, Violet `#7C5CFF`, Menthe `#34E5C4`, Rose `#FF7D9C` ; polices Montserrat (titres) +
  Poppins (corps). Chaque **réseau** garde **sa** charte (via `platforms.js`).

# 8. Standards

- **Definition of Done** (7 critères, voir §4).
- **Definition de « terminé » par module** (PLAN-EXECUTION) : code+schéma+manifeste à jour · skip
  gracieux sans clé · tests d'invariants verts · rendu cockpit vérifié (capture) · doc à jour · commit
  atomique sur branche de travail.
- **Skip gracieux** : toute brique IA / tout connecteur s'auto-désactive sans clé/token (CI verte,
  usage hors-ligne intact).
- **Schéma validé avant écriture** : une sortie d'agent invalide n'est pas écrite (loggée).
- **Sourcé & horodaté** : chaque artefact porte `source`/`genere_le`/`modele`/`provenance`.
- **Cockpit dégrade proprement** : artefact absent → « pas encore généré », jamais une erreur.
- **Un test par invariant** : fusion réseaux, consolidation, schémas d'agents, mémoire, sélection IA,
  licence/accès, actions du jour.
- **Niveau de qualité** : « agence marketing premium » ; pas d'ébauche, directement exploitable.

---

# 9. Agents IA

> Manifeste : `scripts/agents.json`. Runner : `scripts/run-agent.py`. Client LLM : `scripts/awema_ai.py`.
> **Bêta livrée** : Analyste, Stratège, Créatif, + Proactivité (agrégateur déterministe).
> **Post-bêta (cible, non implémentés)** : Veille, Modérateur, Chef de projet.

### Analyste ⭐ (livré)
- **Rôle** : explique les résultats — *pourquoi ? que faire ? que reproduire ?*
- **Responsabilités** : produire 3–6 items (≥3 `insight`, ≥2 `reco`), chacun avec une **preuve**
  chiffrée OBLIGATOIRE pointant une métrique réelle ; n'invente aucun chiffre.
- **Entrées** : `reseaux.json` + `memoire.json`. **Modèle** : `claude-opus-4-8`.
- **Sortie** : `_agents/analyste.json`, `items[]` `{type:"insight|reco", titre, explication,
  preuve{metrique,valeur,variation?}, action?}`. **Item requis** : `type, titre, explication`.
- **Interactions** : rendu dans le panneau « Pourquoi & Que faire » ; sa première `reco` alimente
  l'agrégateur Proactivité.

### Stratège ⭐ (livré)
- **Rôle** : transformer la performance en **plan** (cadence, meilleures heures, objectifs, planning).
- **Entrées** : `reseaux.json` + `memoire.json` + `campagne.json`. **Modèle** : `claude-opus-4-8`.
- **Sortie** : `_agents/stratege.json` — `champs_sortie` `cadence_recommandee`, `meilleures_heures[]`,
  `objectifs[]` + `liste` `plan_editorial[]` `{jour,heure?,format,angle,reseau}`. **Item requis** :
  `jour, format, angle, reseau`.
- **Interactions** : panneau « Plan recommandé » ; n'écrit pas `campagne.json` sans validation humaine.

### Créatif ⭐ (livré)
- **Rôle** : produire des publications prêtes (hooks, scripts, prompts image, variantes).
- **Entrées** : `memoire.json` + `reseaux.json` + `campagne.json`. **Modèle** : `claude-sonnet-4-6`.
- **Sortie** : `_agents/creatif.json` — `liste` `idees[]` `{hook,script,format,reseau,prompt_image,
  variantes[]}`. **Item requis** : `hook, format, reseau`. *(Pas d'image générée : un prompt prêt à
  coller — pas de dépendance OpenAI dans le chemin bêta.)*
- **Interactions** : panneau « Idées prêtes à publier » + bloc dans le visualiseur ; sur validation,
  écriture dans `campagne.json`.

### Proactivité — `actions-du-jour` (livré, **sans clé IA**)
- **Rôle** : passer de « on consulte » à « AWEMA propose ». **Déterministe** (fonction pure
  `aggreger_actions(reseaux, agents)`), n'exige aucune clé.
- **Entrées** : `reseaux.json` + les sorties `analyste/stratege/creatif` si présentes.
- **Sortie** : `_agents/actions-du-jour.json`, `items[]` `{priorite(1-3),type,titre,detail,source,
  action{label,kind,target}}`, **max 6**, triés par priorité.
- **Règles déterministes** : cadence en retard (`jours_depuis>7`, et message spécifique `>90`) ·
  `a_repondre.total` commentaires · audience en baisse (dernier point < précédent) · format gagnant
  (max `engagement_moyen`) · 1ʳᵉ `reco` Analyste · 1ᵉʳ item Stratège · 1ᵉʳ item Créatif.
- **Interactions** : hero « N choses à faire aujourd'hui » en tête du Command Center.

### Veille / Modérateur / Chef de projet (cible, **non implémentés**)
- **Veille** : concurrents/hashtags/tendances → `marche.json` (module Intelligence Marketing).
- **Modérateur** : tri commentaires/DM/réactions, réponses préparées → `moderateur.json` (nécessite
  ingestion + permissions write).
- **Chef de projet** : suit validations/tâches/campagnes, coordonne les agents → `projet.json`.

### Client LLM agnostique (`awema_ai.py`)
- Supporte **Anthropic** (`/messages`) et tout fournisseur **compatible OpenAI** (`/chat/completions`).
- Sélection : `AWEMA_AI_PROVIDER=<id>` sinon **auto-détection** de la première clé présente.
- Modèle surchargeable via `AWEMA_AI_MODEL`. Clé lue dans l'environnement puis dans `.awema/`.
- **Sans clé → `disponible()=False`, `chat()=None`** (skip gracieux). Fonctions clés : `chat()`,
  `enveloppe()`, `valider_enveloppe()`, `modele_actif()`. CLI : `--providers`, `--check`.

---

# 10. Modules

## Modules existants (M0→M6, tous livrés)
| Module | Objet | Livrables clés |
|---|---|---|
| **M0** Substrat IA & garde-fous | Faire tourner un agent sans risque | `tests/` (unittest), `awema_ai.py`, `agents.json`, `run-agent.py`, schéma d'enveloppe commun |
| **M1** Mémoire Marketing | Carburant des agents | `memoire.json` (identité, ton, personas, produits, FAQ…), `memoire.html`, `awema client memoire`, exposition au registre |
| **M2** Agent Analyste ⭐ | Premier wow (pourquoi/quoi) | `_agents/analyste.json`, panneau « Pourquoi & Que faire » |
| **M3** Agent Stratège ⭐ | Perf → plan | `_agents/stratege.json`, panneau « Plan recommandé » |
| **M4** Agent Créatif ⭐ | Publications prêtes | `_agents/creatif.json`, panneau « Idées prêtes » + visualiseur |
| **M5** Proactivité ⭐ | « AWEMA propose » | `actions-du-jour.json`, hero Command Center, workflow `agents.yml` |
| **M6** Onboarding wow < 30 min | Effet immédiat | client démo « Éclat Beauté » isolé, étape démo dans `onboarding.html`, `?client=`, `preparer-copie-beta.py` aligné |

**Modules « produit » applicatifs** : Landing (`index.html`), Onboarding pilote, Setup/auto-hébergement,
Nouveau client, Mémoire, Cockpit (dashboard), Visualiseur (revue-visuels), Opérateur `/awema`,
Programme bêta (candidature + places + email), Liste d'attente (lancement), Licence + Accès API.

## Modules manquants / partiels (cible documentée, non livrés)
- **Intelligence Marketing** (`marche.json`) + agent **Veille** — *« mon marché »* (concurrents, parts
  de voix). C'est ce qui justifierait le « + activité de marché » du slogan ; **absent du code**.
- **Agent Modérateur**, **Agent Chef de projet** — post-bêta.
- **Instagram** (aucun compte IG Pro relié), **LinkedIn live** (bloqué : email pro requis),
  **X/Threads** (idée).
- **WhatsApp Business (Cloud API)** : connecteur `--whatsapp-all` **planifié** ; seul le guide existe.
- **Vues dashboard inachevées** : Calendrier, Scoring A→E, Tunnel WhatsApp, Automatisation → à
  **masquer « bientôt »** pour la bêta.
- **Couche analytique / séries temporelles** : points d'extension **prévus mais à ne pas implémenter**
  maintenant (`_data/timeseries/<client>/<metric>.ndjson` append-only ; `evolution_audience` en est
  l'amorce).
- **Collaboration multi-utilisateur** (rôles), **opérateur qui pousse lui-même Secrets/Variables**.

---

# 11. Documentation (inventaire + résumés)

**Racine**
- `README.md` — porte d'entrée, couche « OS d'agence » historique, structure, démarrage rapide, mission
  La Grande Vision, conventions essentielles.
- `AGENTS.md` — onboarding express agents IA/humains : règles d'or (range, documente, charte,
  méthode≠livrable, industrialise, DoD), carte mentale, checklist mission, outils MCP selon session.

**docs/** (référence transverse + produit)
- `00-INDEX.md` — MOC Obsidian, point d'entrée admin (commandes licence/accès/attente).
- `01-agence.md` — vision agence, 7 départements, structure obligatoire.
- `02-onboarding.md` — démarrer une mission en 10 min ; carte des sous-dossiers 00→10.
- `03-conventions.md` — langue, nommage, formats, DoD, conventions Git.
- `04-charte-graphique.md` — charte AWEMA + charte client (La Grande Vision : optique, « Voir la vie en grand »).
- `05-connecter-reseaux.md` — architecture de connexion (3 voies), cockpit CM Facebook, limite v21.
- `06-obtenir-token-meta.md` — 7 étapes pour `META_TOKEN`, `FB_PAGE_ID`, `IG_USER_ID`.
- `07-connecter-tiktok.md` — Display API, OAuth par compte, rotation des refresh tokens, `TIKTOK_TOKENS`.
- `08-agent-awema.md` — opérateur `/awema` (commandes, mémoire `.awema/credentials.json`, manifeste).
- `09-auto-hebergement.md` — forker/personnaliser (3 façons), GitHub Pages, récupérer les mises à jour upstream.
- `10-connecter-linkedin.md` — Community Management API, vérif Page, OAuth, blocage email pro.
- `11-programme-beta.md` — 20 places à vie gratuites ; prérequis ; 8 conditions ; cycle de place
  (Active/Avertissement/Recyclée) ; parcours onboarding.
- `12-connecter-ia.md` — IA agnostique, options gratuites, activation, rotation.
- `13-securite-donnees.md` — isolation par fork, risque du dépôt public, sécurité des tokens, RGPD, checklist.
- `14-acces-api-agence.md` — accès « dev entreprise » par plateforme ; **modèle A (défaut)** vs **B (opt-in)**.
- `ACCES-AGENCE.md` — page de contrôle admin : le seul **verrou incontournable = l'accès API** ; checklist
  donner/retirer l'accès ; délivrance de licence comme **preuve juridique**.
- `AUTO-DESCRIPTION.md` — auto-description antérieure (ce présent document en est une version étendue).
- `AWEMA-OS.md` — note maîtresse : vision, ADN, état, plateformes, **journal daté** des jalons.
- `PRD-AWEMA.md` — North Star produit, ADR-001, équipe d'agents, proactivité, mémoire, critères de succès.
- `ROADMAP.md` — **source unique** : Horizon 0 (acquis) / 1 (NOW) / 2 (BÊTA M0–M6) / 3 (POST-BÊTA).
- `PLAN-EXECUTION-BETA.md` — modules M0→M6 (règles d'or anti-régression, critères d'acceptation, séquencement).
- `email-bienvenue.md` — modèle d'email aux agences acceptées (5 sections).

**Par dossier** : chaque dossier d'`outils/`, `scripts/`, `departements/`, `templates/` porte son
`README.md` (convention « un dossier = un README »).

---

# 12. Processus métier (reconstitués)

## P1 — Onboarding d'un pilote/agence (programme bêta → instance)
`rejoindre.html` (candidature mailto) → l'admin réserve une place (`config/beta-seats.json` statut
`invite`) → envoi `email-bienvenue.md` (lien copie d'accueil) → délivrance d'une **licence**
(`awema licence delivrer "Nom" contact=…` → clé `AWEMA-XXXX-XXXX-XXXX` + registre privé
`.awema/licences-registre.json`) → le pilote forke la **copie d'accueil**, personnalise, active Pages,
ajoute un client, connecte un réseau, envoie un premier retour. Place → `active`.

## P2 — Connexion d'une plateforme (présence réelle)
Choix du modèle (A autonome / B managé) → obtention des accès (App + token, guides `connect-*.html` /
`docs/05-…/14-…`) → secrets en GitHub Secrets/Variables (ou `.awema/`) → `connect-reseaux.py --<reseau>-all`
→ `reseaux.json` mis à jour → `build.py` → cockpit. Automatisé par `sync-reseaux.yml` / `sync-tiktok.yml`.

## P3 — Production de propositions IA
`agents.yml` (quotidien 06:30 UTC, skip sans clé) lance `run-agent.py analyste|stratege|creatif --all`,
puis `actions-du-jour --all`, puis `build.py`, puis commit des `_agents/*.json` régénérés.

## P4 — Pipeline éditorial complet (modèle « La Grande Vision », département Marketing)
Méthode Universelle en 10 phases : **Audit → Personas → Piliers → Calendrier → Production → Validation
→ Publication → Mesure → Optimisation → Boucle IA**. Mappée aux dossiers `00-brief … 10-presentation`.
Le volume (180 contenus / 90 jours, 2/jour) est **généré** par `_generateur/generer.py` (déterministe ;
`DATE_DEBUT=2026-07-01`, `JOURS=90`, `POSTS_PAR_JOUR=2`) → produit `calendrier-editorial.csv`,
`contenus.md`, `scripts-video.md`, `scoring.csv`, `campagne.json`. Livrables annexes : tunnel WhatsApp
(7 étapes), CRM J0→J90, scoring A→E, automatisation (Make/n8n/Zapier), présentation direction (30+ slides),
exports PDF.

## P5 — Revue des visuels (boucle d'amélioration)
`revue-visuels` lit `campagne.json` → l'opérateur étudie/annote/demande des modifications → « Générer
prompt mis à jour » → regénération (Canva/Midjourney/ChatGPT/API) → re-revue. Statuts : À produire /
En revue / Validé / À retoucher. Export `retours-campagne.{json,md}`.

## P6 — Gouvernance : licence + accès API (contrôle & base juridique)
**Licence** = outil **opérationnel** de suivi + **base légale** (registre = preuve « à qui/quand »),
**pas** une serrure (code open-source, vérification éditable). **Le seul verrou incontournable = l'accès
API** : en **modèle B (AWEMA Tech Provider)**, l'éditeur est le « robinet » et peut **révoquer** (la
plateforme l'applique). Demande d'accès managé : `demande-acces.html` → `awema acces demande/lister/
accepter/refuser` (registre privé `.awema/acces-api-registre.json`, validation **par agence**). Par
**défaut (modèle A)**, chaque agence fournit **ses propres** API → autonomie totale.

## P7 — Lancement commercial (état le plus récent, juin 2026)
**Repositionnement** : les 10 places pilotes ouvertes sont **complètes** ; le produit ouvrira **sur
abonnement**. Collecte des intéressés via `liste-attente.html` → `merci.html` (mailto), registre privé
`.awema/liste-attente.json` (`awema attente ajouter|lister|compter`, dédoublonnage par contact).
**DÉDUCTION** : la stratégie « 20 places gratuites à vie » (docs/11, beta-seats) précède cette bascule ;
les deux discours coexistent dans le dépôt (voir §14).

## P8 — Stratégie deux-dépôts (en cours)
**DÉDUCTION** (fortement étayée par la branche `main` et les échanges récents) : le dépôt de
**production reste privé** (contient les 27 vrais clients), et un **dépôt public séparé** (template
`awema-os`, alimenté par la branche orpheline `main` sans données réelles) sert de **base testeurs** /
« Template repository ». La copie propre est produite par `git archive main` ou `preparer-copie-beta.py`.

---

# 13. Points forts

1. **Architecture sobre et cohérente** : ADR-001 (agents = jobs, JSON = vérité, cockpit = renderer) est
   élégante, additive et **sans serveur** ; ajouter de l'IA n'ajoute qu'un secret.
2. **Zéro régression by design** : agents additifs, skip gracieux, schémas validés, **harnais de tests**
   stdlib en CI.
3. **Données réelles, zéro fiction** : discipline forte (preuves chiffrées, étiquetage « proposition IA »).
4. **Auto-hébergement réel** : personnalisation par un **seul** fichier `config/agence.json` propagée
   partout via `build.py` + `apply.js`.
5. **IA agnostique avec options gratuites** : zéro verrou fournisseur ; abaisse la barrière d'entrée.
6. **Proactivité sans IA** : l'agrégateur « actions du jour » fonctionne **même sans clé** (alertes
   déterministes) → valeur immédiate.
7. **Sécurité pensée** : secrets hors dépôt, store local gitignoré `chmod 600`, rotation + historique,
   isolation par fork, registres de preuve privés.
8. **Documentation dense et structurée** : PRD/ROADMAP/PLAN cohérents, journal daté, MOC Obsidian.
9. **Design system premium** partagé (`awema-ui`), cockpit sans librairie graphique.
10. **Opérateur en langage naturel** (`/awema`) qui « ne demande que l'inconnu ».

# 14. Faiblesses

1. **Double identité non résolue** : la couche « OS d'agence marketing » (`README.md`, `AGENTS.md`,
   `departements/`, pipeline éditorial) et la couche « OS d'agence assistée par IA » (PRD, agents,
   landing) coexistent ; `README.md` parle encore de « mission La Grande Vision » comme cœur.
2. **Discours bêta contradictoire** : « 20 places gratuites à vie » (docs/11, `beta-seats.json`) vs
   « 10 places complètes + lancement sur abonnement » (landing/liste d'attente récentes).
3. **Promesse « + activité de marché »** dans le slogan (`config/agence.json`) alors que le module
   Intelligence Marketing / agent Veille **n'existe pas** encore.
4. **Vues dashboard inachevées** (Calendrier, Scoring, Tunnel, Automatisation) encore présentes — risque
   de montrer de l'inachevé tant qu'elles ne sont pas masquées « bientôt ».
5. **Dépendance forte à un écosystème instable** : Meta v21 a déprécié la majorité des insights
   (portée/reach) → beaucoup de `null` ; LinkedIn live **bloqué** (email pro) ; IG non connecté.
6. **GitHub Pages gratuit = dépôt public = données business exposées** : tension réelle entre
   auto-hébergement gratuit et confidentialité (atténuée par la stratégie deux-dépôts, encore manuelle).
7. **Plan éditorial peu rempli** : un seul client (La Grande Vision) a une `campagne.json` complète.
8. **`generer-image-openai.py` (OpenAI)** incohérent avec « Claude/agnostique par défaut » (à réaligner
   ou repousser, déjà noté dans le PRD).
9. **Frictions d'intégration** observées : l'intégration GitHub ne peut pas créer de dépôt ni déclencher
   de workflows (403) ; la politique réseau de l'environnement limite les pushes au dépôt courant.

# 15. Dette technique

- **Couplage documentaire** : informations dupliquées entre `AWEMA-OS.md`, `PRD`, `ROADMAP` (atténué
  par la règle « ROADMAP = source unique », mais le journal et l'état réapparaissent ailleurs).
- **`docs/AUTO-DESCRIPTION.md` vs ce document** : deux auto-descriptions à maintenir en cohérence.
- **`reseaux.json` redondant** : blocs spécifiques (`tiktok`, `youtube`, `linkedin`) **dupliquent**
  partiellement `par_reseau` et `top_posts` → source de divergence possible.
- **Tests** : ~29 tests couvrent les invariants purs (merge, consolidation, schémas, mémoire, IA,
  licence, actions) mais **pas** le rendu HTML ni les connecteurs réseau (appels réseau non mockés).
- **Co-localisation données/template** : la séparation « instance privée avec données » / « template
  public propre » repose sur des scripts + discipline manuelle (`preparer-copie-beta.py`, `git archive`),
  pas sur une frontière structurelle.
- **`docs/14` récap. secrets** mentionne `TIKTOK_PAT` tandis que le manifeste/`AWEMA-OS` parlent de
  `GH_PAT` → **incohérence de nommage** du PAT TikTok à harmoniser.
- **Génération de PDF** hors ADN (Playwright) — utilitaire à isoler clairement du cœur.

# 16. Opportunités

1. **Unifier le récit** : faire de la couche « OS assistée par IA » le discours principal et reléguer le
   pipeline éditorial « agence » comme **un module** (Marketing) parmi d'autres.
2. **Livrer le module Marché + agent Veille** : c'est le différenciateur promis et le pas vers « parts
   de voix » ; il réutilise les **mêmes connecteurs** sur des comptes publics.
3. **Industrialiser la stratégie deux-dépôts** : automatiser la publication du template public propre
   (action « publish-template ») pour supprimer la friction manuelle.
4. **Brancher l'IA gratuite par défaut** (Groq/Gemini/Ollama) dès l'onboarding pour que le « wow »
   arrive sans carte bancaire.
5. **Couche séries temporelles** (déjà prévue) : passer d'instantanés à des tendances réelles
   (`evolution_audience` → `.ndjson` append-only) sans casser le JSON.
6. **Agent Modérateur** branché sur WhatsApp Cloud API : transformer le cockpit en **canal de
   conversion**, pas seulement d'analyse.
7. **Mécanisme d'abonnement** (cohérent avec le repositionnement « sur abonnement ») adossé à la licence
   + accès API comme levier de monétisation.
8. **Tests de rendu** (Playwright) pour verrouiller le cockpit, et **mocks** des connecteurs.

# 17. Risques

| Risque | Impact | Atténuation existante / proposée |
|---|---|---|
| **Dépendance API tierces** (Meta v21, TikTok, LinkedIn) | Métriques perdues, connecteurs cassés | « Adaptateur de source » prévu (capacités déclarées) ; dégradation gracieuse |
| **Données business exposées** (dépôt public) | Fuite concurrentielle | Instance privée / local / hébergeur à accès contrôlé ; copie d'accueil propre |
| **Fuite de secret** | Compromission de comptes | Secrets hors dépôt, rotation + historique, révocation documentée |
| **Confiance dans l'IA** (hallucination) | Mauvaises décisions | Règle « preuve obligatoire », étiquetage « proposition IA », humain dans la boucle |
| **Contrôle d'accès faible** (code open-source) | Usage non autorisé | Le verrou réel = accès API (modèle B) ; licence = base juridique/preuve |
| **Dette de cohérence** (double identité, discours bêta) | Confusion utilisateurs/contributeurs | Unifier récit et offre ; source unique déjà adoptée pour la roadmap |
| **Passage à l'échelle** (50–200 clients en JSON) | Lenteur build/rendu | Couche analytique/cache prévue (à ne pas implémenter prématurément) |
| **Maintenance solo** | Continuité du projet | Documentation exhaustive + conventions « reprenable par un autre agent » |

---

# 18. Architecture cible supposée (DÉDUCTION)

**DÉDUCTION** (étayée par PRD §1, ADR-001, ROADMAP Horizon 3) : la cible est un **OS d'agence digitale**
où le cockpit devient un **centre de commandement** réunissant **progressivement** réseaux, CM, IA,
contenus, calendrier, clients, campagnes, **veille/marché**, analytics, collaboration, automatisation —
le tout piloté par une **équipe d'agents IA** (Analyste, Stratège, Créatif **livrés** ; Veille,
Modérateur, Chef de projet **à venir**) qui produisent des artefacts JSON additifs rendus par un front
statique. Le modèle économique cible (DÉDUCTION, étayée par le repositionnement récent) : **abonnement**,
avec **licence** (base juridique/preuve) et **accès API managé (modèle B)** comme leviers de contrôle
incontournables. La frontière technique cible : **instance privée par agence** (données) + **template
public** (code), avec une couche **séries temporelles** et un **adaptateur de source** pour absorber la
volatilité des API — explicitement « à prévoir, ne pas implémenter » tant que le cœur bêta n'est pas
parfait. Principe directeur permanent : **qualité > quantité**, **zéro régression**, **données réelles**.

---

# 19. Questions ouvertes (pour un nouvel architecte)

1. **Identité** : AWEMA est-il « un OS d'agence » (multi-départements, pipeline éditorial) ou « un cockpit
   social assisté par IA » ? Lequel est le produit, lequel est un module ?
2. **Offre** : on tranche comment entre « 20 places gratuites à vie » et « lancement sur abonnement » ?
   Que deviennent les pilotes fondateurs au passage payant ?
3. **Slogan vs réalité** : garde-t-on « activité de marché » dans le slogan avant d'avoir le module Veille ?
4. **Confidentialité** : quel hébergement par défaut pour concilier gratuité (Pages public) et données
   privées ? Le template public est-il maintenu en miroir automatique du privé ?
5. **Passage à l'échelle** : à partir de combien de clients le couple JSON + GitHub Actions + `build.py`
   atteint ses limites ? Quand activer la couche analytique/timeseries ?
6. **IA** : quel fournisseur par défaut pour la bêta (gratuit vs qualité) ? Comment gérer le coût des
   agents en quotidien sur N clients ?
7. **Dépendances** : quelle stratégie face à la dépréciation continue des API (Meta v21) ? L'adaptateur
   de source doit-il devenir prioritaire ?
8. **Contrôle** : la licence sans verrou technique suffit-elle juridiquement ? Faut-il systématiser le
   modèle B (Tech Provider) pour les clients communs ?
9. **Tests** : faut-il ajouter des tests de rendu (Playwright) et des mocks de connecteurs avant
   d'ouvrir largement ?
10. **Gouvernance produit** : qui valide la roadmap quand les retours des pilotes affluent ? Comment
    arbitrer « qualité > quantité » sous pression de demandes ?

---

# 20. Suggestions (sans modifier le projet)

1. **Aligner README/AGENTS sur le PRD** : présenter d'emblée AWEMA comme « OS d'agence assistée par IA »,
   et positionner le pipeline éditorial comme le module « Marketing ».
2. **Réconcilier l'offre** dans un seul document canonique (places, gratuité, abonnement, avantages
   fondateurs) et y faire pointer landing + docs/11 + beta-seats.
3. **Masquer les vues inachevées** du dashboard derrière un badge « bientôt » avant toute ouverture
   large (déjà recommandé dans ROADMAP).
4. **Harmoniser le nommage des secrets** (`GH_PAT` vs `TIKTOK_PAT`) à travers docs et workflows.
5. **Automatiser la publication du template public** (un workflow « publish-template » qui rejoue
   `git archive main` / `preparer-copie-beta.py`) pour supprimer la friction manuelle.
6. **Prioriser le différenciateur** : livrer un MVP de l'agent **Veille** + onglet « Marché » (réutilise
   les connecteurs) pour honorer le slogan.
7. **Activer une IA gratuite par défaut** au premier lancement (Groq/Gemini/Ollama) pour garantir le
   « wow < 30 min » sans clé payante.
8. **Documenter la séparation données/code** comme une frontière structurelle (deux dépôts) plutôt que
   conventionnelle.
9. **Étendre les tests** : rendu cockpit (Playwright) + connecteurs (réponses API mockées) pour
   verrouiller les chemins critiques.
10. **Amorcer la couche séries temporelles** côté écriture seulement (`evolution_audience` →
    `.ndjson` append-only) sans changer la source de vérité JSON, comme prévu dans le PRD §8.

---

## Annexe A — Commandes essentielles
```bash
# Registre & build (après toute édition de config ou de données)
python3 outils/_data/build.py

# Opérateur
python3 scripts/awema.py list | needs <plat> | set <plat> CLE=VAL | rotate <plat> CLE=VAL | connect <plat>
python3 scripts/awema.py setup nom="…" github.owner="…" charte.ciel="#…"
python3 scripts/awema.py client new <slug|auto> nom="…" secteur="…" tiktok="…"
python3 scripts/awema.py client memoire <slug> ton="…" persona+="Nom::besoin::objection"
python3 scripts/awema.py licence delivrer "Agence" contact=email   # + registre/verifier-cle/revoquer-cle/set
python3 scripts/awema.py acces demande "Agence" client= reseau= motif=   # + lister/accepter/refuser
python3 scripts/awema.py attente ajouter "Nom" contact=email profil=…    # + lister/compter

# Connecteurs présence
python3 scripts/connect-reseaux.py --meta-all|--tiktok-all|--youtube-all|--linkedin-all

# Agents IA
python3 scripts/awema_ai.py --providers | --check
python3 scripts/run-agent.py --list
python3 scripts/run-agent.py analyste|stratege|creatif <slug|--all>
python3 scripts/run-agent.py actions-du-jour --all      # déterministe, sans clé IA

# Tests
python3 -m unittest discover -s tests

# Copie d'accueil propre (sans données réelles)
python3 scripts/preparer-copie-beta.py ../awema-beta
```

## Annexe B — Workflows GitHub
| Workflow | Déclencheur | Secrets/Variables | Effet |
|---|---|---|---|
| `tests.yml` | push / PR / dispatch | aucun | `unittest discover -s tests` (anti-régression) |
| `agents.yml` | dispatch + cron quotidien (~06:30 UTC) | clés IA (toutes optionnelles ; skip si aucune) | analyste/stratege/creatif + actions-du-jour → `_agents/*.json` → build → commit |
| `sync-reseaux.yml` | dispatch + cron lundi 06:00 UTC | `META_TOKEN` (req), `YOUTUBE_API_KEY`/`LINKEDIN_TOKEN` (opt) | `--meta-all`/`--youtube-all`/`--linkedin-all` → build → commit |
| `sync-tiktok.yml` | dispatch + cron lundi 06:30 UTC | `TIKTOK_CLIENT_KEY/SECRET`, Variable `TIKTOK_TOKENS`, PAT | `--tiktok-all` + rotation des refresh tokens → commit |

## Annexe C — Fournisseurs d'IA (`config/ia-providers.json`)
- **Gratuits** (`type: openai`) : Groq, Google Gemini, OpenRouter (`:free`), Cerebras, Mistral (essai),
  GitHub Models, Ollama (local), Together.
- **Payants** : Anthropic/Claude (`type: anthropic`, défaut, crédits d'essai), OpenAI.
- Sélection : `AWEMA_AI_PROVIDER=<id>` + clé correspondante (env ou `.awema/`) ; sinon auto-détection.
  Modèle surchargeable via `AWEMA_AI_MODEL`.

## Annexe D — Glossaire
- **ADN** : invariants non négociables du projet (§4).
- **ADR-001** : décision d'architecture « agents = jobs, JSON = vérité, cockpit = renderer ».
- **Slug** : identifiant de dossier client (`code-scooper`).
- **Copie d'accueil** : version propre du dépôt (0 donnée réelle, 1 client démo) pour les pilotes.
- **Modèle A / B** : agence autonome (ses API) / AWEMA Tech Provider (API d'AWEMA, sur validation).
- **Skip gracieux** : auto-désactivation propre d'une brique sans sa clé/token.
- **Dégradation gracieuse** : afficher « source indisponible » plutôt qu'un `null` muet (ex. insights v21).

---

_Fin de la mémoire permanente. Mettre à jour ce document à chaque évolution structurelle (nouvel agent,
nouveau module, changement d'offre, frontière données/code). Toute affirmation non étiquetée « DÉDUCTION »
reflète l'état du dépôt au 2026-06-27._
