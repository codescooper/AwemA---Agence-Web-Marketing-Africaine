---
titre: AWEMA OS — Journal & Vision
tags: [awema, statut, vision, roadmap, presence-en-ligne]
maj: 2026-06-25
statut: actif
---

# 🐝 AWEMA OS — Journal & Vision

> **Note maîtresse** (Obsidian-friendly). Ouvre le dépôt comme un coffre Obsidian, ou copie
> cette note dans ton coffre. Source de vérité du projet : ce qui est fait, où on va.

## 🎯 Vision (objectif à partir de maintenant)

Faire d'AWEMA OS un **cockpit polyvalent et pratique** pour la **gestion complète de la
présence en ligne ET de l'activité de marché d'une entité** :

1. **Présence en ligne 360°** — agréger *toutes* les plateformes d'une entité au même endroit :
   Facebook ✅, Instagram ⏳, TikTok ✅, **YouTube** (à venir), **LinkedIn** (à venir), X/Threads…
   → audience, engagement, contenus, commentaires à répondre, meilleurs posts, cadence, créneaux.
2. **Activité de marché** — au-delà de l'entité : veille concurrentielle, tendances du secteur,
   parts de voix, benchmark — pour *décider*, pas seulement *constater*.
3. **Pilotable en langage naturel** — via l'opérateur `/awema` : « connecte YouTube de
   code-scooper », « compare-moi à la concurrence »… il ne demande que l'inconnu et agit.
4. **Multi-entités** — chaque client = une entité gérée de bout en bout (présence + marché + contenu).

> Principe constant : **données réelles, zéro fiction** ; **secrets jamais dans le dépôt** ;
> **automatisable** (GitHub Actions) ; **réutilisable** par humains et agents IA.

---

## ✅ État actuel (ce qui tourne)

### Socle & organisation
- Monorepo « système d'exploitation de l'agence » : `departements/`, `outils/`, `docs/`, `scripts/`.
- Conventions + charte ([[docs/04-charte-graphique]]) : Bleu Nuit #0A1F44 · Bleu Ciel #4BA3FF · Gold #D4AF37 · Montserrat/Poppins.
- 26 clients réels dans le registre (`outils/_data/agence.js`, régénéré par `build.py`).

### Mission 1 — La Grande Vision (marketing complet)
- 180 contenus / 90 j, scripts vidéo, prompts (Canva/Midjourney/GPT) par plateforme,
  tunnel WhatsApp, CRM J0→J90, scoring A→E, automatisation Make/n8n/Zapier, exports PDF.

### Dashboard (Command Center) — `outils/dashboard/`
- **Cockpit multi-clients** : audience agence, par client (audience, engagement, à répondre,
  contenus), chips par réseau, cadence, **liens directs** (profils, visualiseur, présence).
- **Présence digitale** par client : réactions détaillées, commentaires à répondre (inbox CM),
  abonnés les plus actifs, cadence, meilleur créneau, types de contenu, top posts, vues, évolution.
- **Vue d'ensemble** : « Actions du jour » (commentaires à répondre + alerte cadence) + prochaines pubs.
- Design premium (glassmorphism, dark/clair, Command+K, bento, SVG charts sans lib).

### Visualiseur — `outils/revue-visuels/`
- Refondu sur le design system, **sélecteur de client** (s'adapte à *tous* les clients),
  état vide propre pour les clients sans plan.

### Présence digitale (pipeline réel)
- **Meta (Facebook/Instagram)** ✅ : 1 token → 1 client par Page (`--meta-all`), insights v21
  (limite : portée/reach plus exposée → on a les **vues de Page**, réactions, commentaires, top posts…).
- **TikTok** ✅ : Display API v2, OAuth par compte, refresh tokens **rotatifs** gérés via Variable
  GitHub + **GH_PAT** (rotation auto). Assistant d'onboarding `scripts/tiktok-onboard.py`.
- Fusion **multi-réseaux** : un client agrège FB + TikTok (ex. **code-scooper** : FB 285 + TikTok 6 992
  = audience 7 277 ; **de-alman** : TikTok 703).
- Sync autonome : `.github/workflows/sync-reseaux.yml` (Meta, lundi 06:00) + `sync-tiktok.yml` (06:30).

### Opérateur `/awema` — `scripts/awema.py` + `.claude/commands/awema.md`
- Pilotage **langage naturel** : connecte/rotation des plateformes ; **ne demande que l'inconnu** ;
  garde le **dernier identifiant + historique** dans `.awema/credentials.json` (gitignoré, chmod 600).
- Manifeste extensible : `scripts/awema-connectors.json`.

### Site / GitHub Pages
- **Page d'accueil** (`index.html`) + **guide « Connecter TikTok »** (`connect-tiktok.html`) avec
  boutons « copier » et liens directs. Pages légales (`legal/`) + page OAuth (`oauth.html`).
- `.nojekyll` (sert `_data`/`_design`). À servir **depuis la racine**.

---

## 🔌 Plateformes — état

| Plateforme | État | Méthode | Notes |
|---|---|---|---|
| Facebook | ✅ | Graph API (token) | 1 token → toutes les Pages |
| Instagram | ⏳ | Graph API (IG Pro relié) | aucun compte IG Pro relié pour l'instant |
| TikTok | ✅ | Display API v2 (OAuth/compte) | refresh tokens rotatifs + GH_PAT |
| **YouTube** | 🔜 prochain | **YouTube Data API v3 (clé API)** | **simple** : stats publiques de chaîne sans OAuth |
| **LinkedIn** | 🔜 | OAuth + Marketing Developer Platform | **complexe** : app review, admin de la page |
| X / Threads | 💡 idée | API payante / scraping limité | à évaluer |

---

## 🗺️ Roadmap (prochaines étapes)

- [ ] **YouTube** (priorité — facile) : connecteur `--youtube-all` (clé API + `yt_channel_id` par client).
      Récupère abonnés, vues totales, nb vidéos, + top vidéos (statistiques publiques).
- [ ] **LinkedIn** : app LinkedIn + OAuth org + récup. abonnés/impressions (plus lourd).
- [ ] **Instagram** : relier des comptes IG Pro aux Pages FB → métriques IG réelles.
- [ ] **Activité de marché** : veille concurrents (mêmes connecteurs sur des comptes publics
      concurrents), parts de voix, tendances → onglet « Marché » au dashboard.
- [ ] **Opérateur** : `/awema` pousse lui-même Secrets/Variables GitHub (fin du copier-coller).
- [ ] **Alertes** : notifier (mail/WhatsApp) quand un commentaire attend, cadence en retard, pic d'audience.

---

## 🔐 Sécurité (invariants)
- Aucun token/secret dans le dépôt (vérifié). Vivent dans : Secrets/Variables GitHub + `.awema/` local.
- `.gitignore` : `.awema/`, `tiktok_tokens.out`.
- TikTok : refresh tokens rotatifs resauvegardés via `GH_PAT` (permission *Variables: Read and write*).
- App TikTok en **Sandbox** (comptes de test) ; secret **Sandbox** ≠ Production.

---

## 🧭 Glossaire
- **OAuth** : autorisation déléguée (l'utilisateur connecte son compte). **refresh_token** : jeton longue
  durée pour obtenir des jetons d'accès ; **rotatif** côté TikTok (un nouveau à chaque rafraîchissement).
- **PAT** : clé GitHub personnelle ; ici permission *Variables: Read and write* pour réécrire `TIKTOK_TOKENS`.
- **Slug** : identifiant de dossier client (`code-scooper`). Le slug dans `TIKTOK_TOKENS` doit matcher le client.
- **Insights** : statistiques natives d'une plateforme (portée, vues…). En **v21** Meta, beaucoup sont dépréciées.

---

## 📓 Journal (jalons)
- **2026-06-22** — Init AWEMA OS + Mission 1 (La Grande Vision) ; outil Revue des Visuels ; prompts/desc par post.
- **2026-06-22/23** — Dashboard Command Center ; design system ; multi-clients ; présence digitale réelle.
- **2026-06-23** — Pipeline Meta autonome (un token → toutes les Pages) ; correctifs insights v21 ;
  cockpit community management ; **TikTok** (connecteur + assistant + pages légales/OAuth) ; page d'accueil.
- **2026-06-23** — **Opérateur `/awema`** (langage naturel, mémoire d'identifiants + historique).
- **2026-06-25** — TikTok finalisé : **GH_PAT** (rotation auto) ; **code-scooper** FB+TikTok (7 277) ;
  **de-alman** (703) ; client.json auto pour clients TikTok. **Nouvelle vision : présence + marché, multi-plateformes.**
