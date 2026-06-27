# 07 — CRM & Calendrier de Relance (J0 → J90)

Système de relance multicanal (**SMS · WhatsApp · Email**) pour transformer chaque contact
en client, puis en client fidèle. Tous les messages sont **rédigés**.

> Principe : le bon message, au bon moment, sur le bon canal. WhatsApp = relation,
> SMS = rappel court, Email = contenu de valeur & preuve.

---

## Vue d'ensemble

| Jour | Étape | Canal prioritaire | Intention |
|---|---|---|---|
| **J0** | Bienvenue / 1ᵉʳ contact | WhatsApp | Accueillir, qualifier |
| **J1** | Rappel & valeur | SMS + WhatsApp | Rappeler le RDV / relancer |
| **J3** | Relance prospect | WhatsApp + Email | Convertir l'indécis |
| **J7** | Suivi après visite | WhatsApp + Email | Satisfaction + avis |
| **J14** | Confort & 2ᵉ paire | WhatsApp | Vente complémentaire |
| **J30** | Contenu expert | Email | Entretenir l'expertise |
| **J60** | Réactivation | SMS + WhatsApp | Rappeler la marque |
| **J90** | Contrôle / fidélité | WhatsApp + Email | Re-bilan, parrainage |

---

## J0 — Bienvenue

**WhatsApp**
```
Bonjour {{PRENOM}} 👋 Bienvenue à La Grande Vision ! Merci de votre message. On s'occupe de
votre vue avec le sourire 😊. Dites-nous votre besoin (bilan / lunettes / progressifs).
```

## J1 — Rappel & valeur

**SMS**
```
La Grande Vision : bonjour {{PRENOM}}, votre vue compte ! Pour votre bilan à Yopougon,
répondez ici ou WhatsApp {{NUM}}. 👓
```
**WhatsApp**
```
Petit rappel 😊 souhaitez-vous qu'on réserve votre bilan cette semaine ? On a des créneaux
en semaine et le week-end. Répondez « OUI » et on s'occupe de tout.
```

## J3 — Relance prospect (indécis)

**WhatsApp**
```
Bonjour {{PRENOM}} 👋 Beaucoup repoussent leur bilan… puis regrettent d'avoir attendu pour
voir clair 👀. Le bilan est simple, rapide et sans engagement. On vous trouve un créneau ?
```
**Email** — *Objet : Votre vue mérite 20 minutes cette semaine 👓*
```
Bonjour {{PRENOM}},

Vous nous avez contactés pour votre vue — merci !
Un bilan à La Grande Vision, c'est : un diagnostic sérieux, des conseils honnêtes, et des
solutions adaptées à votre budget.

📅 Réserver en 2 clics : {{LIEN_WHATSAPP}}
📍 Yopougon, Abidjan

À très vite,
L'équipe La Grande Vision — « Voir la vie en grand. »
```

## J7 — Suivi après visite

**WhatsApp**
```
Bonjour {{PRENOM}} 😊 Comment se passent vos premiers jours avec vos lunettes ? Un réglage
gratuit si besoin 👍. Et si vous avez aimé, un avis Google nous aiderait : {{LIEN_AVIS}} ⭐
```
**Email** — *Objet : Tout est confortable, {{PRENOM}} ? 👓*
```
Bonjour {{PRENOM}},
Merci de votre confiance ! Vos lunettes doivent être parfaitement confortables. Le moindre
ajustement est offert. Et votre avis compte énormément : {{LIEN_AVIS}}.
À bientôt, l'équipe La Grande Vision.
```

## J14 — Confort & 2ᵉ paire

**WhatsApp**
```
Bonjour {{PRENOM}} 👋 Deux semaines déjà ! 💡 Une 2ᵉ paire (soleil à votre vue ou lecture)
change vraiment le quotidien. On a des offres en ce moment, ça vous intéresse ? 😎
```

## J30 — Contenu expert (nurturing)

**Email** — *Objet : 3 réflexes simples pour protéger vos yeux des écrans*
```
Bonjour {{PRENOM}},
Ce mois-ci, nos conseils d'expert : la règle 20-20-20, le bon éclairage, et l'importance
des pauses. 👀
Besoin d'un contrôle ? On est là : {{LIEN_WHATSAPP}}.
La Grande Vision — Yopougon.
```

## J60 — Réactivation

**SMS**
```
La Grande Vision : {{PRENOM}}, vos yeux vont bien ? Pensez au contrôle. RDV WhatsApp {{NUM}} 👓
```
**WhatsApp**
```
Bonjour {{PRENOM}} 😊 Ça fait 2 mois ! Tout va bien côté vision ? Si un proche a besoin d'un
bilan, on prend soin de toute la famille à Yopougon. 🏘️
```

## J90 — Contrôle & fidélité / parrainage

**WhatsApp**
```
Bonjour {{PRENOM}} 🎉 Merci de votre fidélité ! 👓 Parrainez un proche : il bénéficie d'un
bilan privilégié, et vous d'un avantage sur votre prochaine paire. Donnez-nous son prénom ?
```
**Email** — *Objet : Merci {{PRENOM}} 🙏 + une attention pour vos proches*
```
Bonjour {{PRENOM}},
3 mois déjà ! Pour vous remercier, parrainez un proche : avantage pour vous deux.
Et pensez à votre contrôle annuel — on vous rappellera le moment venu. 👍
La Grande Vision — « Voir la vie en grand. »
```

---

## Champs CRM minimum (à tenir)
`Prénom · Nom · Téléphone · Canal · Persona · Besoin · Statut · Date RDV · Date visite ·
Achat · Montant · Avis laissé · Date prochaine relance`

> Voir [`../09-automatisation/`](../09-automatisation/) pour automatiser ces relances
> (Make / n8n / Zapier + Google Calendar + Gmail/WhatsApp API).
