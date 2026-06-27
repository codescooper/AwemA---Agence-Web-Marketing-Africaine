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
| 005 | Vocabulaire « Module » sans renommage physique de `departements/` | ✅ Accepté |

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
**Statut** : Accepté (2026-06-27).
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

---

> **Prochain ADR libre : ADR-006.** Créer un ADR avant toute décision structurante (frontière de
> données, nouveau module officiel, changement de contrat d'agent/plugin, migration de répertoires).
