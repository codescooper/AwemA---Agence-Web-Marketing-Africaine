# Bibliothèque de Prompts Visuels — La Grande Vision

Gabarits maîtres réutilisables. Remplacer `{{SUJET}}` par le thème du contenu. La charte est
déjà intégrée.

---

## A. Carrousel pédagogique (PIL1)

**Canva**
```
Format: carrousel Instagram 1080x1350 (4:5), 5 slides.
Palette: fond Bleu Nuit #0A1F44, texte blanc, accents Bleu Ciel #4BA3FF, numéros & CTA en Gold #D4AF37.
Typographie: titres Montserrat ExtraBold, corps Poppins Regular.
Composition: 1 idée par slide, pictogrammes ligne fine, beaucoup d'espace.
Visuels: icônes santé visuelle (œil, écran, lunettes), photo humaine slide 1.
CTA (dernière slide): bouton Gold « Réservez votre bilan · WhatsApp ».
Sujet: {{SUJET}}.
```
**Midjourney**
```
Editorial infographic-style photo about {{SUJET}}, deep navy blue #0A1F44 background, sky blue #4BA3FF and gold #D4AF37 accents, clean medical look, soft natural light, person interacting with eyewear, copy space, premium healthcare branding --ar 4:5 --stylize 250
```
**GPT Image**
```
Photographie professionnelle réaliste illustrant {{SUJET}}, ambiance cabinet d'optique moderne à Abidjan, lumière douce, palette bleu nuit/bleu ciel/gold, cadrage 4:5, espace pour texte, compatible publicité Meta.
```

## B. Mise en avant produit / monture (PIL2)

**Canva**
```
Format: 1080x1350. Fond dégradé Bleu Nuit → Bleu Ciel. Détails Gold.
Typographie: Montserrat Bold (nom collection), Poppins (détails).
Composition: monture en héros au centre, ombre douce, reflets premium.
Visuels: photo studio de lunettes nette, fond neutre.
CTA: « Venez l'essayer · Yopougon » en Gold.
Sujet: {{SUJET}}.
```
**Midjourney**
```
Premium product photography of eyeglasses, studio lighting, neutral background with deep navy #0A1F44 and gold #D4AF37 accents, sharp focus, luxury eyewear advertising, reflections, macro detail --ar 4:5 --stylize 250
```
**GPT Image**
```
Photo studio réaliste d'une paire de lunettes premium, éclairage professionnel, fond sobre, touches gold, qualité publicité, cadrage 4:5. Sujet: {{SUJET}}.
```

## C. Témoignage / preuve sociale (PIL3)

**Canva**
```
Format: 1080x1350. Fond clair #F7F9FC, bandeau Bleu Nuit, guillemets Gold.
Typographie: citation en Poppins SemiBold, nom en Montserrat.
Composition: portrait client souriant à gauche, citation à droite, étoiles Gold.
CTA: « Vous aussi ? Écrivez-nous · WhatsApp ».
Sujet: {{SUJET}}.
```
**Midjourney**
```
Authentic warm portrait of a happy African client wearing stylish glasses, eyewear clinic in Abidjan, soft natural light, navy and gold brand accents, genuine smile, testimonial style, shallow depth of field --ar 4:5 --stylize 250
```
**GPT Image**
```
Portrait réaliste et chaleureux d'un(e) client(e) souriant(e) portant des lunettes, ambiance authentique, lumière naturelle, accents bleu nuit/gold, style témoignage, compatible Meta. Sujet: {{SUJET}}.
```

## D. Offre / CTA conversion (PIL4)

**Canva**
```
Format: Story 1080x1920. Fond Bleu Nuit, gros titre blanc, bouton Gold proéminent.
Typographie: Montserrat ExtraBold.
Composition: titre offre en haut, visuel central, bouton « RDV WhatsApp » en bas.
Visuels: icône WhatsApp, lunettes, badge « Bilan ».
CTA: « 📲 Écrivez RDV sur WhatsApp ».
Sujet: {{SUJET}}.
```
**Midjourney**
```
Bold marketing key visual for an eyewear clinic promotion, deep navy #0A1F44 background, gold #D4AF37 call-to-action button, sky blue accents, clean premium layout, space for headline, advertising style --ar 4:5 --stylize 250
```
**GPT Image**
```
Visuel publicitaire réaliste pour une offre de cabinet d'optique, fond bleu nuit, bouton gold visible, mention WhatsApp, cadrage 4:5, compatible Meta Ads. Sujet: {{SUJET}}.
```

## E. Vie locale / communauté (PIL5)

**Midjourney**
```
Warm lifestyle photo of a family in Yopougon, Abidjan, wearing glasses, neighborhood vibe, golden hour, navy and gold brand palette, joyful authentic, documentary style --ar 4:5 --stylize 250
```

## F. Coulisses / B2B (PIL6)

**Midjourney**
```
Professional behind-the-scenes photo of a modern optometry clinic, optician using precision eye-measurement technology, clean medical environment, navy #0A1F44 and gold #D4AF37 accents, corporate trustworthy mood, soft light --ar 4:5 --stylize 250
```

---

## Astuce production
Pour générer en lot : copier le prompt du type voulu, remplacer `{{SUJET}}` par le titre du
contenu (colonne « Titre » du calendrier), conserver le suffixe Midjourney `--ar 4:5
--stylize 250`.
