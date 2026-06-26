# ROADMAP — AWEMA (source unique)

> Source **unique** de la feuille de route. `AWEMA-OS.md` pointe ici. Vision : [[PRD-AWEMA]].
> Exécution détaillée : [[PLAN-EXECUTION-BETA]]. Principe : **qualité > quantité**, **zéro régression**.

## Légende
✅ fait · 🟡 prêt mais non activé · 🔜 en cours / prochain · 🧊 repoussé après la bêta · 💡 idée

---

## Horizon 0 — Acquis (ne pas régresser)
- ✅ Socle monorepo, conventions, charte, auto-hébergement (config → build → apply).
- ✅ Présence digitale réelle : **Meta** (1 token → toutes les Pages), **TikTok** (OAuth + rotation),
  **YouTube** (clé API). Fusion multi-réseaux + alias.
- ✅ Cockpit multi-clients (Command Center), visualiseur, charte par plateforme, « Présence par réseau ».
- ✅ Opérateur `/awema` (langage naturel, secrets jamais exposés, historique).
- ✅ Landing produit, onboarding bêta, programme bêta (conditions, places, copie d'accueil, retours).
- 🟡 **LinkedIn** : connecteur + assistant OAuth prêts ; live bloqué (email pro) → activable.

---

## Horizon 1 — NOW : substrat IA & garde-fous (avant tout agent)
> Objectif : poser les fondations IA **sans rien casser**. Tout est **additif**.

1. ✅ **Garde-fous anti-régression** — harnais `tests/` stdlib (`python3 -m unittest discover -s tests`) :
   merge multi-réseaux, consolidation, schémas d'agents. CI : `.github/workflows/tests.yml`.
2. 🔜 **Dégradation gracieuse** — étiqueter dans l'UI toute métrique indisponible/dépréciée (badge
   « source indisponible ») au lieu d'un `null` muet. *(reste à faire)*
3. ✅ **Client IA Claude** — `scripts/awema_ai.py` (API Messages Anthropic, modèle configurable,
   **skip gracieux sans clé**). Secret `ANTHROPIC_API_KEY` (géré par l'opérateur : `awema set claude …`).
4. ✅ **Contrat d'agent** — `scripts/agents.json` + `scripts/run-agent.py` + convention
   `_agents/<agent>.json` (intégrée au registre par `build.py`) + **carte « Assistants IA »** au cockpit.

> **M0 livré** (cf. [[PLAN-EXECUTION-BETA]]). Prochain : M1 (Mémoire) puis M2 (Analyste).

---

## Horizon 2 — BÊTA : le « wow » (peu de features, ultra-finies)
> 5–6 livrables qui font dire « je gagne des heures ». Chaque agent est **additif** et **sourcé**.

1. ✅ **Mémoire Marketing** (`memoire.json`) + éditeur `memoire.html` + `awema client memoire` +
   exposition au registre + carte cockpit. *(M1 livré)*
2. ✅ **Agent Analyste** — *pourquoi / que faire* sur la présence réelle → `_agents/analyste.json` →
   panneau **« Pourquoi & Que faire »** (constats sourcés + actions, preuve chiffrée, label « proposition IA »)
   dans la vue Présence digitale. *(M2 livré — sortie live dès `ANTHROPIC_API_KEY` fournie)*
3. ✅ **Agent Stratège** — cadence + meilleures heures + objectifs + plan éditorial hebdo →
   `_agents/stratege.json` → panneau **« Plan recommandé »** (cockpit). *(M3 livré — contrat d'agent
   généralisé : sorties structurées au-delà d'`items`)*
4. ⭐ **Agent Créatif** — idées, hooks, scripts, prompts image (Claude) → `creatif.json` + action
   « **Générer ?** » dans le visualiseur.
5. ⭐ **Proactivité** — agrégateur → `actions-du-jour.json` rendu en **tête du Command Center** ;
   workflow planifié `agents.yml`.
6. ⭐ **Onboarding → wow < 30 min** — données de démo « effet wow » + parcours pilote poli + alignement
   de la copie d'accueil.

**Périmètre bêta volontairement réduit** : on **masque** (« bientôt ») les vues inachevées (Calendrier,
Scoring, Tunnel, Automatisation) plutôt que de montrer de l'inachevé.

---

## Horizon 3 — POST-BÊTA (sur retours des 20 pilotes)
- 🧊 **Module Intelligence Marketing** + **agent Veille** (`marche.json` : concurrents, parts de voix, tendances).
- 🧊 **Agent Modérateur** (tri commentaires/DM, réponses préparées — nécessite ingestion/permissions write).
- 🧊 **Agent Chef de projet** (validations, tâches, campagnes ; coordination des agents).
- 🧊 **Instagram** (IG Pro relié), **LinkedIn live** (déblocage email pro), **X/Threads** (à évaluer).
- 🧊 **Collaboration multi-utilisateur** (rôles, attributions).
- 🧊 **Couche analytique / séries temporelles** (points d'extension déjà prévus — cf. PRD §8).
- 🧊 **Opérateur** pousse lui-même Secrets/Variables GitHub (fin du copier-coller).

---

## Repoussé / déprioritaire (assumé)
- 🧊 Export PDF (`html2pdf.py`, `export-pdf.sh`, `csv2html.py`) — utilitaires d'agence, pas un wow bêta.
- 🧊 `generer-image-openai.py` (OpenAI) — **réaligner sur Claude** au module Créatif, sinon repousser.
- 🧊 Vues dashboard inachevées — masquées « bientôt » jusqu'à finition post-bêta.

## Ce qui impressionnera les 20 pilotes (résumé)
Cockpit qui **propose** 3 actions réelles du jour · Analyste qui **explique** · Créatif qui **produit**
en 1 clic · le tout à **leur marque**, sur **leurs vraies données**, en **< 30 min**. L'IA **travaille**.
