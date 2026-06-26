---
titre: AWEMA — Donner l'accès à une agence (page de contrôle)
tags: [awema, admin, acces, controle, licence]
maj: 2026-06-26
---

# 🗝️ Donner l'accès à une agence — page de contrôle

> **Ta page Obsidian de référence** : tout le nécessaire quand tu veux donner l'accès à quelqu'un.
> Ouvre-la, suis la checklist, garde la main.

---

## ❓ « Y a-t-il un élément qu'ils ne pourront pas contourner ? » — la réponse honnête

**Dans le code : NON.** Le projet est open-source et auto-hébergé. Quiconque a le code peut retirer
n'importe quelle vérification logicielle (licence, bannière, « kill switch »). Toute serrure écrite
*dans le dépôt* est, par nature, **contournable** par une personne technique.

**Hors du code : OUI — l'accès aux API officielles.** C'est la **plateforme** (Meta, TikTok, LinkedIn)
qui l'applique, pas ton code. Après toute leur config, le **dernier élément manquant** pour que l'outil
soit *réellement* fonctionnel sur les Pages de **leurs** clients, c'est un **jeton de production valide**
— et celui-ci ne peut venir que d'une **App vérifiée** (Business Verification + App Review). Si cette App
est **la tienne** (statut *Tech Provider*), alors :

- ils **ne peuvent pas fabriquer** un jeton valide sans passer par toi ;
- tu **délivres et révoques** l'accès par agence, quand tu veux ;
- c'est **incontournable** car enforce côté Meta/TikTok, pas dans le dépôt.

> 🔑 **Ton vrai levier = être le fournisseur d'accès API (Tech Provider).** La « licence » ci-dessous
> est l'**outil opérationnel** (le code qu'on s'échange, le suivi, la base légale) ; l'**API access**
> est le **cadenas réel**.

### Les deux modèles — à choisir consciemment
| Modèle | Indépendance agence | Ton contrôle | Quand |
|---|---|---|---|
| **A — Agence autonome** : chaque agence crée SES propres Apps (Meta/TikTok…) | Totale | Aucun (juste licence légale) | Tu veux un écosystème ouvert |
| **B — AWEMA Tech Provider** : les agences passent par TES Apps pour les jetons de prod | Faible sur l'API | **Fort, révocable** | Tu veux garder la main (recommandé pour la bêta) |

Pour un **verrou incontournable**, choisis **B**. Tu restes le « robinet » d'accès API.

---

## ✅ Checklist : donner l'accès à UNE agence (modèle B)

1. **Réceptionne la candidature** (formulaire `rejoindre.html` → email). Vérifie le profil.
2. **Réserve une place** dans `config/beta-seats.json` (statut → `invite`, nom/handle/contact).
3. **Envoie l'email de bienvenue** (modèle : [[email-bienvenue]]) : lien du dépôt **copie d'accueil**
   (Template repository), `onboarding.html`, conditions ([[11-programme-beta]]), guide API ([[14-acces-api-agence]]).
4. **Délivre une licence** : `python3 scripts/awema.py licence delivrer "<Nom Agence>"` → te donne une
   **clé** à transmettre. (Tu peux la coller dans la fiche de la place.)
5. **Donne l'accès API (le cadenas)** — modèle B :
   - Ajoute leur(s) Page(s) client(s) à **ton** App Meta (System User token *scopé* à ces Pages), ou
   - Ajoute-les comme **testeurs/utilisateurs** de tes Apps TikTok/LinkedIn le temps de la bêta.
   - Tu peux **révoquer** à tout moment côté plateforme → l'outil cesse de récupérer les données.
6. **Marque la place** `active` dans `config/beta-seats.json` + note la date.
7. **Suivi** : un retour utile/mois (issues GitHub). Sinon → avertissement (30 j) → recyclage.

### Révoquer un accès
- **API (effet immédiat, incontournable)** : retire la Page de ton App Meta / retire le testeur TikTok/LinkedIn,
  ou révoque le token. → plus aucune donnée ne remonte, quoi qu'ils fassent côté code.
- **Licence** : `python3 scripts/awema.py licence revoquer` (sur communication) + statut place → `recyclee`.
- **Place** : libère-la dans `config/beta-seats.json` (proposer à la liste d'attente).

---

## 📬 Tout sous la main (liens rapides)
- Formulaire de candidature : `rejoindre.html`
- Email de bienvenue (modèle) : [[email-bienvenue]]
- Conditions & prérequis : [[11-programme-beta]]
- Guide accès API (dev entreprise) : [[14-acces-api-agence]]
- Connecter une IA (gratuite) : `connect-ia.html` · [[12-connecter-ia]]
- Sécurité & isolation : [[13-securite-donnees]]
- Suivi des 20 places : `config/beta-seats.json`
- Générer la copie d'accueil : `python3 scripts/preparer-copie-beta.py ../awema-beta`
- Licence : `python3 scripts/awema.py licence …` (delivrer / set / verifier / revoquer)

---

## 🧩 Licence — comment ça marche (et ses limites)
- `config/licence.json` porte `{agence, cle, statut}`. Le dashboard affiche **« non activée »** tant
  qu'aucune clé valide n'est posée, avec « contactez AWEMA pour activer ».
- C'est un **frein + une base légale** (les conditions l'exigent), **pas** une serrure incontournable
  (code éditable). Le **vrai** verrou reste l'**accès API** (modèle B).
- Tu délivres la clé par agence et tu la révoques sur manquement.

> En résumé : **tu gardes la main par l'API (incontournable) ; la licence est l'outil de gestion.**
