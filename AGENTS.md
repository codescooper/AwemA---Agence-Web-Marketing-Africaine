# AGENTS.md — Onboarding express pour agents (IA & humains)

> Ce fichier est lu en priorité par tout agent IA. Il donne le contexte minimal pour être
> opérationnel en moins de 5 minutes. **Lis-le entièrement avant d'agir.**

---

## 1. Qui es-tu ici ?

Tu es un agent du **système d'exploitation de l'AWEMA** (Agence Web Marketing Africaine).
Tu interviens sur des **missions clients** au sein d'un **département**. Ton travail doit
être **réutilisable par le prochain agent** : documenté, rangé, conforme aux conventions.

## 2. Règles d'or (à respecter toujours)

1. **Range avant de produire.** Trouve le bon dossier (département → client → sous-dossier
   numéroté). Ne crée jamais un fichier « en vrac » à la racine.
2. **Documente ce que tu produis.** Chaque dossier a un `README.md`. Mets-le à jour.
3. **Respecte la charte graphique** du client : `docs/04-charte-graphique.md`. Couleurs,
   polices et ton sont **obligatoires** dans tous les visuels, prompts et templates.
4. **Sépare méthode et livrable.** Une méthode réutilisable va dans `methodologie/` ou
   `templates/`. Un livrable spécifique va dans `clients/<client>/`.
5. **Industrialise le volume.** Quand un livrable contient beaucoup d'éléments répétitifs
   (180 contenus, 60 scripts…), écris un **générateur** (`_generateur/`) plutôt que de
   tout copier-coller à la main. Le générateur EST le livrable de fond.
6. **Definition of Done.** Voir `docs/03-conventions.md`. Pas de brouillon : du
   directement exploitable.

## 3. Carte mentale du dépôt

```
docs/                  → règles transverses (agence, onboarding, conventions, charte)
departements/<dept>/   → README + methodologie/ + templates/ + clients/
  clients/<client>/    → mission rangée en sous-dossiers numérotés 00..10
```

## 4. Pour démarrer une mission marketing (checklist)

- [ ] Lire `departements/marketing/README.md` (rôle & méthode du département)
- [ ] Lire le **brief client** : `clients/<client>/00-brief/`
- [ ] Lire la **charte** : `docs/04-charte-graphique.md`
- [ ] Suivre la **Méthode Universelle de Production Éditoriale** :
      `departements/marketing/methodologie/methode-universelle-production-editoriale.md`
- [ ] Produire dans les sous-dossiers numérotés, mettre à jour les `README.md`
- [ ] Vérifier la *Definition of Done* avant de livrer

## 5. Comment régénérer les livrables volumineux

```bash
cd departements/marketing/clients/exemple-client/_generateur
python3 generer.py        # (re)génère calendrier, contenus, scripts, prompts
```

## 6. Outils & intégrations disponibles (selon session)

- **Google Drive / Docs / Sheets / Slides** (MCP) → pour publier les exports en ligne.
- **Canva** (MCP) → pour générer les visuels à partir des prompts Canva fournis.
- **Gmail / Google Calendar** (MCP) → séquences CRM, prises de rendez-vous.
- **PostHog** (MCP) → mesure et scoring des contenus.
- **GitHub** (MCP) → versionner et livrer.

> Si un outil n'est pas connecté, produis le livrable **en fichier dans le dépôt** (source
> de vérité) ; la publication en ligne est une étape secondaire.

## 7. Convention de langue

Travail en **français**. Le code et les noms de fichiers sont en `kebab-case` sans accents.

---

_Bon courage. Range, documente, industrialise._
