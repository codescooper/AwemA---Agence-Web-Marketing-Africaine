# 09 — Automatisation : la Machine Éditoriale Autonome

Objectif : un système qui, **chaque mois**, s'auto-améliore et reproduit le cycle complet,
avec un minimum d'intervention humaine (validation seulement).

## Le cycle mensuel automatisé

```
1. Analyse des résultats      (collecte KPI → scoring)
2. Détection des meilleurs    (tri Score Global, notes A)
3. Génération des sujets       (les A nourrissent la banque de sujets)
4. Génération du calendrier    (generer.py)
5. Génération des scripts       (generer.py)
6. Génération des visuels       (prompts → Canva/MJ/GPT)
7. Génération des publications  (planification multi-plateformes)
```

Trois implémentations équivalentes sont décrites ci-dessous : **Make**, **n8n**, **Zapier**.
Choisir selon l'outil disponible chez le client. Le cœur logique (génération) reste
`_generateur/generer.py`.

---

## A. Workflow Make (Integromat)

**Scénario 1 — Collecte & Scoring (quotidien / hebdo)**
1. **Trigger :** Scheduler (tous les jours 23:00).
2. **Facebook/Instagram/LinkedIn Insights** modules → récupérer portée, engagement,
   commentaires, partages par post.
3. **WhatsApp / PostHog** → messages reçus, RDV (événements `message_recu`, `rdv_pris`).
4. **Google Sheets — Update Row** → écrire E:J dans l'onglet *Scoring* (les formules
   K:Q se recalculent seules).

**Scénario 2 — Cycle mensuel (1er du mois)**
1. **Trigger :** Scheduler (1er du mois 06:00).
2. **Google Sheets — Search Rows** : récupérer les contenus notés **A**.
3. **Router** → pour chaque A : extraire pilier + sujet.
4. **HTTP / Cloud Function** : appeler `generer.py` (ou réécrire `sujets.py` en ajoutant les
   sujets gagnants en tête de liste) → régénère calendrier + contenus + scripts.
5. **Google Drive — Upload** : déposer les CSV/MD + exports PDF.
6. **OpenAI / Canva module** : pour chaque ligne du nouveau calendrier, envoyer le *Prompt
   Visuel* → générer le visuel → stocker dans Drive.
7. **Buffer / Meta / Notification** : pré-programmer les posts (statut « En attente
   validation »).
8. **Gmail / Slack** : notifier l'équipe « Nouveau cycle prêt à valider ✅ ».

```
[Scheduler 1/mois] → [Sheets: get notes A] → [Iterator]
   → [Run generer.py] → [Drive upload] → [Canva/OpenAI: visuels]
   → [Scheduler posts: statut À valider] → [Gmail: notifier équipe]
```

---

## B. Workflow n8n

**Workflow « scoring-quotidien »**
- `Cron` (23:00) →
- `HTTP Request` (Graph API Meta) + `HTTP Request` (LinkedIn) + `PostHog` node →
- `Function` (mapper les métriques par ID de contenu) →
- `Google Sheets` (Update) onglet Scoring.

**Workflow « cycle-mensuel »**
- `Cron` (1er du mois) →
- `Google Sheets` (Read, filtre Note = A) →
- `Execute Command` : `python3 _generateur/generer.py` (n8n self-hosted) →
- `Read Binary Files` (CSV/MD) → `Google Drive` (Upload) →
- `Split In Batches` sur le calendrier →
  - `HTTP Request` (API génération d'image avec le Prompt GPT Image) →
  - `Google Drive` (Upload visuel) →
- `HTTP Request` (planificateur social) statut brouillon →
- `Gmail` (notifier) + `Google Calendar` (créer les rappels de publication).

> n8n self-hosted permet `Execute Command` → idéal pour lancer le générateur Python
> directement et garder la logique dans le dépôt.

---

## C. Workflow Zapier

Zapier ne lance pas de script Python arbitraire : on combine Zaps + un *Code step* (JS) ou
un webhook vers une Cloud Function qui exécute `generer.py`.

**Zap 1 — Collecte → Scoring**
- *Trigger :* Schedule by Zapier (quotidien).
- *Action :* Facebook Pages / Instagram / LinkedIn → Get metrics.
- *Action :* Google Sheets → Update Row (Scoring E:J).

**Zap 2 — Cycle mensuel**
- *Trigger :* Schedule by Zapier (mensuel).
- *Action :* Google Sheets → Lookup (Notes A).
- *Action :* Webhooks by Zapier → POST vers Cloud Function `regenerer` (exécute
  `generer.py`, renvoie les fichiers).
- *Action :* Google Drive → Upload.
- *Action :* OpenAI (DALL·E) → image depuis *Prompt GPT Image*.
- *Action :* Buffer → brouillon de publication.
- *Action :* Gmail → notifier l'équipe.

**Zap 3 — Tunnel & CRM (transverse)**
- *Trigger :* nouveau message WhatsApp (via provider type 360dialog/Twilio).
- *Action :* Google Sheets (CRM) → créer/maj contact + statut.
- *Action :* Google Calendar → créer le RDV.
- *Delay + Action :* envoyer les relances J1/J3/J7… (cf. `../07-crm-relance/`).

---

## Schéma d'architecture (vue logique)

```
            ┌──────────────────────────────────────────┐
            │   SOURCES (Meta / TikTok / LinkedIn /     │
            │   WhatsApp / PostHog)                     │
            └───────────────┬──────────────────────────┘
                            ▼ (API)
        ┌─────────────────────────────────────┐
        │  ORCHESTRATEUR (Make / n8n / Zapier) │
        └───────┬───────────────────┬──────────┘
                ▼                   ▼
   ┌────────────────────┐   ┌────────────────────────┐
   │ Google Sheet        │   │ _generateur/generer.py │
   │ (Scoring, formules) │   │ (calendrier, contenus, │
   │ → Notes A→E         │   │  scripts, prompts)     │
   └─────────┬──────────┘   └───────────┬────────────┘
             │  les "A"  ───────────────►│ (nouveaux sujets)
             ▼                            ▼
   ┌────────────────────┐   ┌────────────────────────┐
   │ Génération visuels  │   │ Planification & publi.  │
   │ (Canva / MJ / GPT)  │   │ (Buffer / Meta / TikTok)│
   └────────────────────┘   └────────────────────────┘
                            ▼
                  ┌────────────────────┐
                  │ Validation humaine  │  ← seul point manuel
                  └────────────────────┘
```

## Rôle des MCP disponibles (si connectés en session)
- **Google Drive / Sheets** → stockage & scoring.
- **Canva** → génération des visuels depuis les *Prompts Canva*.
- **PostHog** → mesure (événements `message_recu`, `rdv_pris`, `vente`).
- **Gmail / Google Calendar** → relances CRM & rappels RDV.

## Point de contrôle humain
Le seul point manuel est la **validation** (Onglet 2, colonne *Statut* : `En revue → Validé`).
Tout le reste est automatisable.
