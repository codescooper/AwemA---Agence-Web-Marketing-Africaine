---
titre: 🏠 AWEMA — Accueil du vault (index admin)
tags: [awema, index, accueil, moc]
maj: 2026-06-26
---

# 🏠 AWEMA — Accueil du vault

> **Point d'entrée unique.** Ouvre ce dossier comme **coffre Obsidian** (Open folder as vault),
> puis ouvre cette note. Tout part d'ici.

## 🏛️ Fondations (référence stable — priment en cas de conflit)
- [[FOUNDATION/README]] — Constitution, Kernel, principes, plugins, agents, données, gouvernance, ADR

## 🎯 Vision & pilotage
- [[AWEMA-OS]] — note maîtresse (vision, état, journal)
- [[PRD-AWEMA]] — référence produit (OS d'agence assistée par IA, architecture des agents)
- [[ROADMAP]] — feuille de route (source unique : NOW / BÊTA / POST-BÊTA)
- [[PLAN-EXECUTION-BETA]] — plan module par module (M0→M6, zéro régression)
- [[AUTO-DESCRIPTION]] — auto-description portable (pour analyse externe)

## 🗝️ Contrôle & accès (admin)
- [[ACCES-AGENCE]] — **page de contrôle** : donner/retirer l'accès à une agence
- [[email-bienvenue]] — modèle d'email à envoyer aux agences acceptées
- [[11-programme-beta]] — programme bêta : conditions, prérequis, 20 places
- `config/beta-seats.json` — suivi des 20 places · `config/licence.json` — activation
- **Registres privés (preuve, `.awema/`)** : licences délivrées · demandes d'accès API
- Formulaires : `rejoindre.html` (candidature) · `demande-acces.html` (accès API managé) · `liste-attente.html` (lancement)

### Commandes admin clés
```
# Licence (qui a le droit — base juridique)
python3 scripts/awema.py licence delivrer "Agence" contact=email   # délivre + enregistre (preuve)
python3 scripts/awema.py licence registre                          # qui · quand · statut
python3 scripts/awema.py licence verifier-cle <cle>                # prouve la délivrance

# Accès API managé (qui passe par TES API — validé par agence ; défaut = agence autonome)
python3 scripts/awema.py acces lister                              # demandes + statut
python3 scripts/awema.py acces accepter <id> | refuser <id>        # tu décides

# Liste d'attente du lancement (sur abonnement) — PRIVÉE, hors git (.awema/)
python3 scripts/awema.py attente ajouter "Nom" contact=email      # enregistre un·e intéressé·e
python3 scripts/awema.py attente lister | compter                 # qui attend · combien

# Copie d'accueil pour les pilotes (sans tes données)
python3 scripts/preparer-copie-beta.py ../awema-beta
```

## 🔒 Sécurité & données
- [[13-securite-donnees]] — isolation (chaque pilote = son fork), repo privé, secrets, RGPD

## 🔌 Connecter les plateformes
- [[05-connecter-reseaux]] · [[06-obtenir-token-meta]] — Meta (Facebook/Instagram)
- [[07-connecter-tiktok]] — TikTok · [[10-connecter-linkedin]] — LinkedIn
- [[14-acces-api-agence]] — **accès API « dev entreprise »** (Meta App Review, etc.)
- [[12-connecter-ia]] — brancher une IA (options **gratuites** : Groq, Gemini, Ollama…)
- Guides web : `connect-tiktok.html` · `connect-youtube.html` · `connect-linkedin.html` · `connect-ia.html`

## 🏗️ Auto-hébergement & conventions
- [[09-auto-hebergement]] — forker & personnaliser · `setup.html`
- [[01-agence]] · [[02-onboarding]] · [[03-conventions]] · [[04-charte-graphique]]

## 🤖 Les agents IA (cœur produit)
- Analyste · Stratège · Créatif · Proactivité (« 3 choses à faire aujourd'hui »)
- Manifeste `scripts/agents.json` · client `scripts/awema_ai.py` · runner `scripts/run-agent.py`
- Lancer : `python3 scripts/run-agent.py <agent> --all` (clé IA requise ; actions-du-jour marche sans IA)

## 📊 État (au 2026-06-26)
- 27 clients réels · cockpit + 4 agents · landing + onboarding + copie d'accueil bêta
- IA agnostique (gratuites mises en avant) · contrôle d'accès (licence + validation API)
- ~29 tests verts · branche de travail : `claude/keen-planck-p66rds`

---
> 💡 Astuce Obsidian : active l'affichage **graphe** pour voir les liens entre notes ; cette note est
> le **MOC** (Map of Content) — reviens-y toujours.
