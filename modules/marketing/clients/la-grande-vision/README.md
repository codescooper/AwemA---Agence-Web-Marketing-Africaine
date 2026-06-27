# Mission — La Grande Vision (Cabinet d'optique)

> **Système marketing complet, automatisé et industrialisable** pour le cabinet d'optique
> **La Grande Vision**, Yopougon — Abidjan, Côte d'Ivoire.

Cette mission est la **première livraison** du Département Marketing de l'AWEMA. Elle sert
aussi de **référence** : tout nouvel agent peut la reprendre, la comprendre et la
ré-exécuter.

---

## 🎯 Objectifs business

1. **Générer des rendez-vous** (consultations visuelles).
2. **Générer des ventes de montures**.
3. **Développer la notoriété locale** à Yopougon.
4. **Construire une image d'expert** de la santé visuelle.

## 📡 Canaux

Facebook · Instagram · TikTok · LinkedIn · WhatsApp Business.

## 🎨 Charte

Bleu Nuit `#0A1F44` · Bleu Ciel `#4BA3FF` · Gold `#D4AF37` · Montserrat + Poppins.
➡️ Détails : [`docs/04-charte-graphique.md`](../../../../docs/04-charte-graphique.md).

---

## 🗂️ Plan de la mission (sous-dossiers)

| # | Dossier | Livrable |
|---|---|---|
| 00 | [`00-brief/`](00-brief/) | Brief client complet |
| 01 | [`01-strategie/`](01-strategie/) | Audit, marché, concurrence, personas, positionnement, piliers |
| 02 | [`02-calendrier-editorial/`](02-calendrier-editorial/) | Calendrier 90 j / 180 contenus (CSV) |
| 03 | [`03-contenus/`](03-contenus/) | Les 180 contenus rédigés |
| 04 | [`04-scripts-video/`](04-scripts-video/) | 60+ scripts Reels/TikTok/Shorts |
| 05 | [`05-prompts-visuels/`](05-prompts-visuels/) | Prompts Canva / Midjourney / GPT Image |
| 06 | [`06-tunnel-whatsapp/`](06-tunnel-whatsapp/) | Tunnel WhatsApp (7 étapes) |
| 07 | [`07-crm-relance/`](07-crm-relance/) | Séquences CRM J0→J90 |
| 08 | [`08-scoring/`](08-scoring/) | Scoring automatique + formules |
| 09 | [`09-automatisation/`](09-automatisation/) | Workflows Make / n8n / Zapier |
| 10 | [`10-presentation/`](10-presentation/) | Présentation direction (30+ slides) |
| — | [`_generateur/`](_generateur/) | Générateur Python du volume |
| — | [`_exports-pdf/`](_exports-pdf/) | Exports PDF |

---

## ⚙️ Régénérer tous les livrables de volume

```bash
cd _generateur
python3 generer.py
```

Cela (re)génère : le calendrier (180 lignes), les 180 fiches de contenu, les 60 scripts
vidéo et les prompts associés — tout en respectant la charte et les piliers.

## 📄 Exporter en PDF

```bash
# depuis la racine du dépôt
bash scripts/export-pdf.sh
```
Voir [`scripts/README.md`](../../../../scripts/README.md).

---

## ✅ État de la mission

| Livrable | Statut |
|---|---|
| Brief | ✅ |
| Stratégie (audit, personas, piliers, positionnement) | ✅ |
| Calendrier éditorial 180 contenus | ✅ (généré) |
| Contenus rédigés | ✅ (générés) |
| 60 scripts vidéo | ✅ (générés) |
| Prompts Canva / Midjourney / GPT Image | ✅ |
| Tunnel WhatsApp | ✅ |
| CRM & relances J0→J90 | ✅ |
| Scoring automatique | ✅ |
| Automatisation (Make/n8n/Zapier) | ✅ |
| Présentation direction | ✅ |
