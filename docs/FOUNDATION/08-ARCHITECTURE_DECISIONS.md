---
titre: 08 — ARCHITECTURE DECISIONS (ADR)
statut: vivant
maj: 2026-06-27
---

# 08 — Journal des décisions d'architecture (ADR)

> Toute décision **structurante** produit un ADR. Format : **Contexte · Problème · Décision ·
> Conséquences · Alternatives rejetées**. Un ADR est **immuable** une fois accepté ; on le **remplace**
> par un nouvel ADR (statut `Remplacé par ADR-XXX`) plutôt que de le réécrire.

| ADR | Titre | Statut |
|---|---|---|
| 001 | Agents = jobs, JSON = vérité, cockpit = renderer | ✅ Accepté |
| 002 | Séparation Kernel / Modules | ✅ Accepté |
| 003 | Marketing = seul module officiel | ✅ Accepté |
| 004 | Plugins préférés aux modifications du Kernel | ✅ Accepté |
| 005 | Vocabulaire « Module » sans renommage physique de `departements/` | 🔁 Remplacé par ADR-006 |
| 006 | Renommage `departements/` → `modules/` | ✅ Accepté |
| 007 | GitHub = back-end (écriture navigateur → repo → Actions) | ✅ Accepté |

---

## ADR-001 — Agents = jobs, JSON = vérité, cockpit = renderer
**Statut** : Accepté (origine : `docs/PRD-AWEMA.md` §3 ; formalisé ici).
**Contexte.** Le produit veut « une équipe d'agents IA » tout en respectant l'ADN (auto-hébergé, zéro
serveur, Git = vérité, stdlib).
**Problème.** Comment ajouter de l'IA sans serveur permanent, sans dépendance lourde, et sans risquer de
corrompre les données réelles existantes ?
**Décision.** Un agent = un **script Python** (stdlib + **un** appel HTTPS LLM) déclenché par GitHub
Actions ou `/awema`. Entrées = fichiers du client. Sorties = **artefacts JSON additifs**
(`_donnees/_agents/<agent>.json`). Le **cockpit statique** les lit et les rend. L'humain valide/rejette.
**Conséquences.** (+) Un seul secret (clé LLM), aucun serveur, **zéro régression** (les agents
n'écrivent jamais `reseaux.json`), sorties auditables/diff-ables. (−) Pas de temps réel ; latence =
cadence des workflows.
**Alternatives rejetées.** Back-end permanent/SaaS (viole zéro-SaaS) ; agents écrivant directement dans
`reseaux.json` (risque de régression) ; framework d'agents lourd (viole stdlib/simplicité).

## ADR-002 — Séparation Kernel / Modules
**Statut** : Accepté (2026-06-27).
**Contexte.** AWEMA vise un OS multi-domaines, mais seul le Marketing existe. Sans frontière claire, la
logique métier risque de contaminer le cœur et de bloquer l'extensibilité.
**Problème.** Où s'arrête le « cœur universel » et où commence le « métier » ?
**Décision.** Définir un **Kernel** de 11 concepts universels (cf. [02-KERNEL](02-KERNEL.md)) **sans
aucune logique métier**. Dépendance **à sens unique** : un module connaît le Kernel ; **le Kernel ne
connaît jamais un module**. Le Kernel se manifeste comme conventions + contrats + outils transverses,
pas comme un framework.
**Conséquences.** (+) Extensibilité (de nouveaux modules deviennent possibles) ; cœur stable et testable ;
clarté. (−) Discipline requise pour ne pas glisser du métier dans le Kernel ; un effort de classification.
**Alternatives rejetées.** Monolithe sans frontière (couplage, dette) ; micro-modules dès aujourd'hui
(complexité prématurée, viole la simplicité).

## ADR-003 — Marketing = seul module officiel
**Statut** : Accepté (2026-06-27).
**Contexte.** Tentation d'élargir vite (Finance, RH, CRM…). Ressources limitées ; le Marketing n'est pas
encore exemplaire.
**Problème.** Faut-il développer plusieurs domaines en parallèle ?
**Décision.** **Concentrer toute l'énergie sur le module Marketing.** Les autres domaines sont
seulement **rendus possibles par l'architecture** (Kernel + modèle de plugins) ; leur **logique n'est
pas développée**. On peut documenter leur possibilité, pas la coder.
**Conséquences.** (+) Profondeur et qualité sur un domaine ; « peu de fonctionnalités, ultra-finies ».
(−) Frustration de différer des idées séduisantes hors Marketing.
**Alternatives rejetées.** OS multi-domaines immédiat (dispersion, qualité diluée) ; figer le Marketing
sans préparer l'extensibilité (dette future).

## ADR-004 — Plugins préférés aux modifications du Kernel
**Statut** : Accepté (2026-06-27).
**Contexte.** Une plateforme communautaire doit s'enrichir sans déstabiliser son cœur.
**Problème.** Comment étendre AWEMA (connecteurs, agents, fournisseurs IA) sans casser le Kernel ni
multiplier les régressions ?
**Décision.** Étendre **par plugin déclaratif additif** (entrée de manifeste : `awema-connectors.json`,
`agents.json`, `ia-providers.json`). Modifier le Kernel **seulement** si un concept universel manque, et
**toujours via un ADR**. Cf. [04-PLUGIN_MODEL](04-PLUGIN_MODEL.md).
**Conséquences.** (+) Contributions sûres et isolées ; cœur stable ; skip gracieux par défaut. (−) Le
modèle de plugins doit rester simple et bien documenté pour être réellement préféré.
**Alternatives rejetées.** Fork/patch du Kernel pour chaque besoin (fragmentation) ; système de plugins
à chargement dynamique complexe (viole stdlib/simplicité).

## ADR-005 — Vocabulaire « Module » sans renommage physique de `departements/`
**Statut** : 🔁 **Remplacé par ADR-006** (2026-06-27, le même jour). Décision initiale conservée
ci-dessous pour mémoire ; le renommage a finalement été **exécuté** sur décision de l'architecte.
**Contexte.** La FOUNDATION introduit le mot **« Module »**. Physiquement, un domaine vit dans
`departements/<dept>/`, et `outils/_data/build.py` scanne `departements/*/clients/*` ; les chemins
clients, tests et workflows en dépendent.
**Problème.** Faut-il renommer `departements/` → `modules/` pour aligner le vocabulaire ?
**Décision.** **Non, pas maintenant.** On adopte « Module » comme **terme conceptuel** ; l'emplacement
physique reste `departements/<module>/`. Un éventuel renommage est une **migration future, additive et
réversible** (ex. chemin configurable, ou `modules/` en alias), conditionnée à un ADR dédié. Aucun
changement cassant cette session.
**Conséquences.** (+) Zéro régression ; doc et code restent cohérents via cette note. (−) Léger écart
vocabulaire/répertoire, explicitement tracé ici.
**Alternatives rejetées.** Renommer immédiatement (casse `build.py`, chemins, tests — viole « ne pas
casser l'existant ») ; garder uniquement « département » (perd la clarté du modèle Kernel/Module).

## ADR-006 — Renommage `departements/` → `modules/`
**Statut** : Accepté (2026-06-27). **Remplace ADR-005.**
**Contexte.** La FOUNDATION (ADR-002/003) a posé le modèle **Kernel / Module** et fait du Marketing le
seul module officiel. Le répertoire portait encore le nom historique `departements/`.
**Problème.** L'écart vocabulaire (« module ») vs répertoire (`departements/`) nuit à la clarté pour une
plateforme communautaire ; ADR-005 l'avait **différé** par prudence.
**Décision.** **Renommer `departements/` → `modules/`** maintenant, de façon **mécanique et sûre** :
(1) `git mv departements modules` ; (2) remplacer le chemin `departements` → `modules` dans le code,
les docs, les workflows et `.gitignore` ; (3) renommer le **champ JSON** `"departement"` → `"module"`
dans les `client.json` et les scripts qui l'écrivent ; (4) régénérer le registre (`build.py`) ;
(5) tests verts. Aucune logique métier modifiée.
**Conséquences.** (+) Vocabulaire et structure **alignés** ; clarté pour les contributeurs. (+) `build.py`,
`run-agent.py`, `awema.py`, `connect-reseaux.py`, `preparer-copie-beta.py` scannent désormais `modules/`.
(−) Un fork existant doit refaire le `git mv` + ajuster ses chemins (migration triviale, documentée ici).
**Vérification.** 29 tests unittest verts ; aucune occurrence résiduelle de `departements` hors documents
historiques ; cockpit chargé sans erreur.
**Alternatives rejetées.** Conserver `departements/` (ADR-005 — incohérence durable) ; renommer aussi le
**module** « marketing » (inutile : seul le conteneur changeait de nom) ; introduire un alias `modules/`
→ `departements/` (complexité sans bénéfice).

## ADR-007 — GitHub = back-end (écriture navigateur → repo → Actions)
**Statut** : Accepté (2026-06-27).
**Contexte.** L'outil vise des utilisateurs **non techniciens**. Or l'ADN impose un **front statique
sans serveur** : le navigateur ne peut pas écrire dans le dépôt, d'où des étapes manuelles (télécharger
un JSON, le déposer, lancer `build.py`). Le **traitement** (build + agents) est déjà automatisé par
GitHub Actions ; seul le **chemin d'écriture** reste manuel.
**Problème.** Comment offrir « l'utilisateur **valide**, tout se fait en arrière-plan » **sans** introduire
un serveur qu'on héberge (donc sans trahir « zéro SaaS, auto-hébergé ») ?
**Décision.** **GitHub *est* le back-end.** Le navigateur écrit dans le dépôt de l'utilisateur via l'**API
REST GitHub** (`Contents`), puis déclenche une **Action** (build + agents) via `workflow_dispatch`. Le
cockpit (GitHub Pages) sert le résultat ~1–2 min après. Brique réutilisable : `outils/_design/awema-github.js`.
Auth : un **PAT à granularité fine**, limité au seul dépôt (Contents R/W, Actions R/W), saisi **une fois**
et stocké **côté navigateur** (`localStorage`, jamais dans le dépôt — analogue au store `.awema`).
Le **mode manuel** (téléchargement / commande) reste disponible en **repli** (zéro régression).
**Conséquences.** (+) Non-technicien : remplir → « Enregistrer » → résultat servi. (+) Reste **auto-hébergé**
(chacun son GitHub), **aucun serveur qu'on héberge**, Git = vérité. (−) Le token vit dans le navigateur
(sensible → portée minimale, mono-dépôt, révocable). (−) `file://` est limité par CORS → exécuter via
`http.server`/Pages pour l'écriture. (−) Dépendance à la disponibilité de l'API GitHub.
**Alternatives rejetées.** Compagnon local (assouplit « pas de serveur », exige un lancement) ; SaaS hébergé
(trahit l'ADN auto-hébergé) ; rester 100 % manuel (ne répond pas au besoin non-technicien) ; OAuth App
(nécessiterait un serveur pour le client secret).

## ADR-008 — Configuration des clés sans quitter AWEMA (variables auto, secrets guidés)
**Statut** : Accepté (2026-06-28).
**Contexte.** Avec ADR-007, le navigateur écrit déjà fichiers et déclenche les Actions. Restait **un** geste
technique : pour que les **agents en arrière-plan (cron Actions)** puissent appeler l'IA et les réseaux, la
clé doit vivre en **Secret GitHub** — donc l'agence devait aller dans *Settings → Secrets → Actions* à la main.
**Problème.** Comment supprimer ce dernier aller-retour dans les menus GitHub, sans (a) héberger un serveur,
(b) committer un secret, ni (c) embarquer une dépendance crypto lourde contre l'ADN « zéro dépendance, sans build » ?
**Décision.** **Deux niveaux, selon la sensibilité de la donnée :**
- **Variables Actions** (non sensibles : `AWEMA_AI_PROVIDER=groq`…) → écrites **automatiquement** par le
  navigateur via l'API `actions/variables` (texte clair, aucune crypto requise).
- **Secrets Actions** (clés API, tokens) → l'agence **saisit la valeur dans AWEMA** ; le navigateur la **copie**
  et **ouvre l'écran GitHub exact** (`settings/secrets/actions/new`) : **un seul collage**, plus de navigation.
  L'écriture **100 % automatique** des secrets exige un chiffrement **sealed-box** (X25519+XSalsa20-Poly1305) :
  on **n'implémente pas de crypto maison** (risque) et on **ne télécharge pas** de lib (offline-first). Le point
  d'intégration est **prêt** (`AwemaGH.saveSecret` chiffre via `AwemaGH.seal` si une lib auditée mono-fichier
  est déposée dans `outils/_design/vendor/`) : **amélioration progressive**, sans imposer la dépendance.
Le PAT peut recevoir, **en option**, les portées `Variables` R/W et `Secrets` R/W ; sinon tout retombe sur le
flux guidé (aucune régression, portée minimale préservée).
**Conséquences.** (+) Une agence configure ses clés **sans jamais ouvrir les menus GitHub** (variables) ou en
**un collage** (secrets). (+) `configuration.html` devient un assistant : colle la clé → fournisseur enregistré
seul → secret guidé. (+) Bannière d'accueil 1er lancement → la mise en route. (−) L'auto-écriture des secrets
attend une lib crypto vendue mono-fichier (documentée, opt-in). (−) Le flux guidé reste un collage manuel tant
qu'elle n'est pas déposée. (−) Variables/Secrets API → CORS : exécuter via `http.server`/Pages (déjà le cas).
**Vérification.** Tests verts ; `configuration.html` chargé (assistant IA visible, fournisseur + champ clé) ;
`AwemaGH.setVariable/saveSecret/guideSecret` exportés ; aucun secret écrit dans le dépôt.
**Alternatives rejetées.** Crypto sealed-box écrite à la main (risque de sécurité, non testable hors-ligne) ;
mettre les clés API en **Variables** clair (fuite : visibles en lecture/logs) ; serveur/proxy qui détient les
clés (trahit « zéro SaaS ») ; laisser le geste 100 % manuel (ne répond pas au besoin non-technicien).

## ADR-009 — OAuth réseaux 100 % Pages-native (échange du code dans une Action)
**Statut** : Accepté (2026-06-28).
**Contexte.** L'onboarding TikTok exigeait **Python + un serveur `localhost`** (`tiktok-onboard.py` capture le
`code` OAuth sur `127.0.0.1:8723`, puis échange `code→refresh_token` avec le `client_secret`). Une agence qui
n'utilise **que GitHub Pages** (sans machine locale) ne pouvait donc pas connecter ses réseaux.
**Problème.** Comment connecter un compte TikTok **depuis le navigateur sur Pages**, alors que l'échange du
code requiert le **`client_secret`** — qui **ne peut pas vivre dans une page publique** ?
**Décision.** Appliquer **ADR-007** à l'OAuth : **le navigateur capte le `code`, une GitHub Action fait
l'échange.** (1) `connect-tiktok.html` construit l'URL d'autorisation avec `redirect_uri = oauth.html` (HTTPS,
déjà la page de retour enregistrée) ; (2) TikTok renvoie sur `oauth.html?code=…` ; (3) la page déclenche
`tiktok-exchange.yml` via `workflow_dispatch` (`AwemaGH.runWorkflow(file, inputs, strict)`) en passant `code`
+ `redirect_uri` + `slug` ; (4) l'Action (`scripts/tiktok-exchange.py`) échange avec
`TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET` (Secrets) et enregistre le `refresh_token` rotatif dans la Variable
`TIKTOK_TOKENS` via `TIKTOK_PAT` — **exactement la persistance déjà éprouvée** par `tiktok-onboard.py`. Les 3
Secrets se posent depuis `connect-tiktok.html` (réutilise `AwemaGH.saveSecret`/`guideSecret`, ADR-008).
**Conséquences.** (+) Connexion d'un compte TikTok **sans Python, sans localhost** — un clic + *Authorize*.
(+) Le `client_secret` reste **server-side** (Secret), jamais dans la page. (+) `redirect_uri` HTTPS = plus
de bricolage `localhost`. (+) La logique d'échange est **partagée** avec le flux local (zéro divergence). (−) Le
`code` transite en **entrée de workflow** (visible dans le journal du run) : acceptable car **usage unique +
expiration courte + inutile sans le secret**. (−) Le flux Python reste en repli (utile hors-ligne). (−) Non
testable depuis le sandbox (TikTok + API GitHub bloqués) → vérification sur la Pages de l'utilisateur.
**Vérification.** `tiktok-exchange.py` se compile et échoue **proprement** (`::error::`) sans secrets ; YAML du
workflow valide ; `oauth.html`/`connect-tiktok.html` rendus sans erreur JS (construction de l'URL d'autorisation
et capture du `code` OK) ; suite unittest verte.
**Alternatives rejetées.** Échange dans le navigateur (exposerait le `client_secret`) ; proxy/SaaS détenant le
secret (trahit « zéro SaaS ») ; garder Python+localhost obligatoire (exclut les utilisateurs Pages-only) ;
stocker le token en fichier committé (un token dans Git = fuite).
**Généralisation (2026-06-28).** Le motif est désormais appliqué à **tous les réseaux OAuth** : `oauth.html` est
**multi-fournisseur** (TikTok / LinkedIn / Facebook via le préfixe du `state` : `tt:` / `li:` / `fb:`) et
déclenche le bon workflow (`tiktok-exchange.yml` / `linkedin-exchange.yml` / `meta-exchange.yml`). Pour Meta,
« Se connecter avec Facebook » échange le code → token longue durée (60 j) → Variable `META_TOKEN`
(lue en `secrets.META_TOKEN || vars.META_TOKEN`), supprimant le parcours manuel Graph API Explorer. Les réseaux **à token collé** (Meta, YouTube, WhatsApp) et
les **clés IA** passent par un widget commun `awema-connect.js` → `AwemaGH.saveSecret`/`guideSecret`. LinkedIn
réutilise le PAT TikTok (`secrets.AWEMA_PAT || secrets.TIKTOK_PAT`). **Résultat : plus aucune page n'impose de
commande** ; le terminal Python ne subsiste qu'en repli `<details>`.

---

> **Prochain ADR libre : ADR-010.** Créer un ADR avant toute décision structurante (frontière de
> données, nouveau module officiel, changement de contrat d'agent/plugin, migration de répertoires).
