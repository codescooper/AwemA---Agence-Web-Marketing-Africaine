# AWEMA — Auto-description complète (pour analyse externe)

> Document **autoportant** : destiné à une IA (ou un expert) qui n'a **pas** accès au dépôt.
> Objectif : permettre d'évaluer la **pertinence** du produit et de proposer des **pistes
> d'amélioration**. Rédigé de façon factuelle et neutre. Données chiffrées = état réel au moment
> de la rédaction (26 juin 2026).

---

## 1. Ce que c'est, en une phrase
AWEMA (« Agence Web Marketing Africaine ») est un **monorepo auto-hébergé** qui sert de **système
d'exploitation** pour gérer la **présence en ligne** (et, à terme, l'**activité de marché**) de
plusieurs entités clientes d'une agence web — pilotable aussi bien par des humains que par des
agents IA, avec un principe constant : **données réelles, zéro fiction**.

## 2. Public visé & proposition de valeur
- **Utilisateur principal** : une petite agence de marketing digital (contexte ouest-africain,
  Côte d'Ivoire) qui gère la com de nombreux clients (restaurants, opticiens, créateurs, asso…).
- **Promesse** : agréger *tous* les réseaux d'un client au même endroit (audience, engagement,
  community management, plan éditorial), **sans backend ni abonnement SaaS**, et **réutilisable**
  par d'autres agences qui *forkent* le projet et le personnalisent à leur marque.
- **Modèle de distribution** : pas de SaaS central. Chaque agence **héberge sa propre instance**
  (fork GitHub + GitHub Pages) et configure un seul fichier.

## 3. Partis-pris techniques (contraintes volontaires)
- **Front = pages HTML/CSS/JS *vanilla* mono-fichier**, sans framework ni étape de build, servies
  en `file://` *ou* via **GitHub Pages**. Aucune dépendance npm côté run.
- **Back = scripts Python *stdlib uniquement*** (aucune dépendance pip) : connecteurs d'API,
  générateurs, convertisseurs. Sorties **déterministes** (JSON/CSV/JS).
- **Pas de base de données ni de serveur** : l'état vit dans des fichiers JSON versionnés en git.
- **Sécurité** : aucun secret dans le dépôt. Les jetons vivent dans **GitHub Secrets/Variables**
  (CI) et/ou un store **local `.awema/` gitignoré** (avec historique). `.nojekyll` pour servir les
  dossiers `_data`/`_design`.
- **Automatisation** : **GitHub Actions** récupère les vraies métriques (les runners ont Internet)
  et **commite** les données ; un *bot* met à jour `reseaux.json` + le registre.

## 4. Architecture & flux de données
```
config/agence.json ─┐
                    ├─ build.py ─► outils/_data/config.js  (window.AWEMA_CONFIG)  ─► apply.js (thème, marque, liens fork)
departements/.../client.json,    ─► outils/_data/agence.js  (window.AWEMA_REGISTRY) ─► dashboard / visualiseur
   reseaux.json, campagne.json
outils/_data/platforms.js  (identité de marque par réseau) ─► landing + dashboard
```
- **Modèle de données par client** : `departements/<dept>/clients/<slug>/_donnees/`
  - `client.json` : profil (nom, secteur, lieu, initiales) + handles réseaux + IDs techniques
    (`fb_page_id`, `yt_handle`/`yt_channel_id`, `linkedin_org_id`…) + chemins.
  - `reseaux.json` : **présence digitale réelle** — `global` (audience, posts, likes, commentaires,
    partages, vues, taux d'engagement), `par_reseau` (facebook/instagram/tiktok/youtube/linkedin),
    objets riches `tiktok`/`youtube`/`linkedin`, plus sections *community management* : `reactions`,
    `cadence`, `meilleur_creneau`, `types_contenu`, `a_repondre` (inbox), `top_commentateurs`,
    `top_posts`, `evolution_audience` (historique).
  - `campagne.json` : plan éditorial (contenus, prompts, descriptions).
- **Fusion multi-réseaux** : chaque connecteur n'écrit que « son » réseau et **préserve les autres**
  dans le même `reseaux.json`, puis **reconsolide** les totaux. Un système d'**alias** (`config/aliases.json`)
  rattache un compte (clé de token) à une fiche client canonique (évite les doublons).

## 5. Composants (tous présents dans le dépôt)
**Pages web (statiques)**
- `index.html` — landing produit animée (hero, plateformes à leurs couleurs, features, « comment ça
  marche », **stats réelles** lues du registre avec compteurs animés, section beta).
- `onboarding.html` — parcours beta guidé en 4 étapes, anneau de progression, sauvegarde locale.
- `setup.html` — assistant de **personnalisation** (génère `config/agence.json`, aperçu live, checklist d'hébergement).
- `nouveau-client.html` — formulaire d'onboarding d'un client (génère la fiche + commande opérateur + checklist).
- `connect-tiktok.html`, `connect-youtube.html`, `connect-linkedin.html` — guides pas-à-pas par réseau.
- `oauth.html`, `legal/terms.html`, `legal/privacy.html` — redirection OAuth & pages légales.
- `outils/dashboard/` (**~810 lignes**) — *Command Center* : vues Vue d'ensemble, Calendrier,
  Contenus, Scoring A→E, **Présence digitale** (cockpit community management), Tunnel WhatsApp,
  Automatisation, Clients, Réglages. Palette de commandes (⌘K), thème clair/sombre, compteurs animés,
  **charte par plateforme** (chaque réseau garde ses couleurs/glyphes).
- `outils/revue-visuels/` (**~514 lignes**) — visualiseur du plan de contenu par client (prompts pro,
  descriptions, génération d'image, validation).

**Scripts Python (stdlib)**
- `connect-reseaux.py` (**~1100 lignes**) — connecteurs : **Meta Graph** (découverte de TOUTES les
  Pages via un seul token → un client par Page), **TikTok Display API** (OAuth, refresh tokens
  *rotatifs*), **YouTube Data API** (stats publiques, sans OAuth), **LinkedIn Community Management**
  (stats de Page entreprise). + import manuel CSV.
- `awema.py` (**~390 lignes**) — **opérateur** : gestion d'identifiants multi-plateformes (store local
  `.awema` avec dernier + historique), `connect`/`rotate`/`set`/`get`/`history`, création de client,
  `setup` (édite la config de l'agence). Piloté en langage naturel par la commande `/awema`.
- `tiktok-onboard.py`, `linkedin-onboard.py` — assistants OAuth (capture auto via serveur local ou
  collage d'URL ; échange code → token ; rangement sécurisé).
- Utilitaires : `md2html.py`, `csv2html.py`, `html2pdf.py`, `generer-image-openai.py`, `export-pdf.sh`.
- `outils/_data/build.py` — agrège les clients → registre `agence.js` + `config.js`.

**Manifeste & config**
- `scripts/awema-connectors.json` — déclare, par plateforme, les identifiants requis + commandes
  (extensible : ajouter une plateforme = ajouter une entrée).
- `config/agence.json` (personnalisation), `config/aliases.json` (alias de slugs).
- `.claude/commands/awema.md` — persona de l'opérateur IA.

**Automatisation (GitHub Actions)**
- `sync-reseaux.yml` — étapes Meta → YouTube → LinkedIn → rebuild → commit (chaque étape ignorée si
  son secret manque).
- `sync-tiktok.yml` — refresh TikTok + réécriture de la Variable `TIKTOK_TOKENS` via un PAT fin.

**Docs** : `docs/01..10` (agence, onboarding, conventions, charte, connecter chaque réseau,
auto-hébergement) + `docs/AWEMA-OS.md` (note maîtresse façon Obsidian : vision, état, roadmap, journal).

## 6. État réel (chiffres au 26/06/2026)
- **27 clients** ; **27** `reseaux.json` marqués connectés ; **23** avec une audience agrégée réelle.
- Comptes réellement connectés par réseau : **Facebook ≈ 26**, **TikTok 2**, **YouTube 1**, **LinkedIn 0**.
- **1 seul client** dispose d'un **plan de contenu** (`campagne.json`) — *La Grande Vision*, 180 contenus.
- Exemple de fiche riche : *Code Scooper* — audience consolidée **7 318** (Facebook 287 + TikTok 6 999
  + YouTube 32), avec community management dérivé des posts Facebook.

## 7. Limites & points ouverts (connus)
- **Meta Graph v21** a déprécié la plupart des *insights* (portée/impressions/croissance) → seul
  `page_views_total` survit ; l'engagement est donc rapporté **par abonné** (faute de reach).
- **LinkedIn live bloqué** : la *Community Management API* exige un **email professionnel** (domaine
  personnalisé) — non disponible pour l'instant ; le connecteur est codé mais sans token valide.
- **Instagram** déclaré dans le modèle mais non connecté (dépend d'un compte IG Business lié à une Page).
- **Volet « activité de marché »** (veille concurrentielle, tendances, parts de voix) : **annoncé dans
  la vision mais non implémenté**. L'outil couvre aujourd'hui la *présence*, pas encore le *marché*.
- **Plan éditorial** : structure prête mais peu rempli (1 client). Pas de générateur de plan automatisé branché.
- **Tests** : un mode *fixture* hors-ligne existe pour Meta, mais pas de suite de tests unitaires/CI de non-régression.
- **Co-localisation** : la donnée d'une agence réelle vit dans le même dépôt que le « template » à forker
  (pas encore de séparation nette template ↔ données).
- **Permissions GitHub** : l'intégration ne peut pas déclencher les workflows (lancement manuel requis).

## 8. Ce qui marche concrètement aujourd'hui
- Un **seul token Meta** peuple des dizaines de Pages en clients avec données réelles + cockpit CM.
- **TikTok** de bout en bout (OAuth, rotation auto des tokens via PAT, fusion dans la fiche).
- **YouTube** stats publiques via clé API.
- **Dashboard multi-clients** réactif, **landing** + **onboarding beta** + **auto-hébergement** (fork +
  config) opérationnels.
- **Opérateur `/awema`** : connexion/rotation/onboarding en langage naturel, secrets jamais exposés.

## 9. Questions ouvertes pour l'analyste
1. La proposition « OS auto-hébergé sans backend » est-elle **pertinente** vs un vrai SaaS, pour la
   cible (agences à faible compétence technique) ? Où est le point de bascule ?
2. Le choix **« tout en fichiers JSON versionnés + Actions »** tient-il à l'échelle (50, 200 clients,
   multi-agences) ? Quels goulots ?
3. Quelle est la **vraie valeur différenciante** : l'agrégation multi-réseaux ? le community management ?
   l'opérateur IA ? l'auto-hébergement ?
4. Le volet **« activité de marché »** (non fait) est-il le chaînon qui justifie le nom, ou une distraction ?
5. Priorités si l'objectif est **20 agences beta dans 3 mois** ?
