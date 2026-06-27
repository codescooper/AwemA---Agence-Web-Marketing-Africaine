# 04 — Scripts Vidéo (60)

[`scripts-video.md`](scripts-video.md) contient **60 scripts** courts (Reels / TikTok /
Shorts), 30–60 s, générés par `_generateur/generer.py`.

Structure de chaque script : **Hook → Problème → Démonstration → Solution → CTA**,
présentée en tableau temporel (voix off + incrustations à l'écran), charte respectée.

Chaque script embarque aussi :
- une **description prête à copier** (légende + hashtags) adaptée au réseau de destination
  (Reel Instagram / TikTok / YouTube Shorts) ;
- un **prompt de couverture/miniature** à la charte (vertical **1080x1920 · 9:16**, texte
  minimaliste, illustration en avant) en versions **Canva** et **Midjourney**.

Exemples de sujets couverts :
- Comment savoir que vos lunettes ne sont plus adaptées ?
- Les signes d'une mauvaise vision
- Pourquoi les verres progressifs changent la vie
- Les erreurs qui abîment vos yeux

## Régénérer
```bash
cd ../_generateur && python3 generer.py
```
