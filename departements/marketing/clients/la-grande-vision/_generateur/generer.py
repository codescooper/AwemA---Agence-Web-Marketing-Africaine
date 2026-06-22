#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur éditorial — La Grande Vision (cabinet d'optique, Yopougon).

Produit, de façon DÉTERMINISTE, l'ensemble des livrables de volume :
  - 02-calendrier-editorial/calendrier-editorial.csv  (180 lignes)
  - 03-contenus/contenus.md                           (180 fiches détaillées)
  - 04-scripts-video/scripts-video.md                 (60 scripts)
  - 08-scoring/scoring.csv                            (180 lignes + formules)
  - _donnees/campagne.json                            (données pour l'outil de revue)

Tout respecte la charte (docs/04-charte-graphique.md), les personas
(01-strategie/02-personas.md) et les piliers (01-strategie/04-piliers-editoriaux.md).

Usage :  python3 generer.py
"""
import csv
import json
import os
from datetime import date, timedelta

from sujets import BANQUE

# Visuels Canva produits (index de contenu -> aperçus + vignette).
# Enrichi au fil des générations Canva ; l'outil de revue affiche ces aperçus.
#   image   : vignette renderable dans l'outil (repli gracieux si hors-ligne)
#   apercus : liens Canva durables (vue) des propositions finalisées
CANVA_VISUELS = {
    1: {  # Post pédagogique « 5 signes que vos lunettes ne sont plus adaptées »
        "image": "https://design.canva.ai/bLDBKd3Skc9Thw-",
        "apercus": [
            "https://www.canva.com/d/atEPIY42hLuU28y",
            "https://www.canva.com/d/Q9GLMuBEZeAGIwZ",
            "https://www.canva.com/d/3_kvb3xgkjBhOUy",
            "https://www.canva.com/d/wM3D4WtSBlT7-l6",
        ],
    },
    2: {  # Story conversion « Réservez votre bilan en 2 clics »
        "image": "https://design.canva.ai/rYl4kFxFP64dAWn",
        "apercus": [
            "https://www.canva.com/d/-4fRJbr6SgBekC6",
            "https://www.canva.com/d/Qyo0W_xBly63IYJ",
            "https://www.canva.com/d/CGc06VcZGfKNg9S",
            "https://www.canva.com/d/2k_NP02D8uyMSNt",
        ],
    },
}

# --------------------------------------------------------------------------- #
# Paramètres de campagne
# --------------------------------------------------------------------------- #
DATE_DEBUT = date(2026, 7, 1)   # J0 de la campagne
JOURS = 90
POSTS_PAR_JOUR = 2
HEURE_MATIN = "08:00"
HEURE_SOIR = "18:30"
TOTAL = JOURS * POSTS_PAR_JOUR   # 180

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- #
# Charte (pour les prompts)
# --------------------------------------------------------------------------- #
CHARTE_PROMPT = (
    "deep navy blue #0A1F44 (dominant), sky blue #4BA3FF (accent), "
    "gold #D4AF37 (premium details); Montserrat + Poppins typography; "
    "premium, modern, medical, trustworthy, family-friendly mood; "
    "bright soft natural light; clean airy composition; "
    "optical/eyewear clinic in Yopougon, Abidjan, Côte d'Ivoire"
)

# Direction artistique imposée à TOUS les visuels :
# texte minimaliste + illustration mise en avant (le visuel domine, le texte respire).
STYLE_VISUEL = (
    "Style: TEXTE MINIMALISTE (un titre accrocheur de 3 à 6 mots maximum, aucun pavé de "
    "texte), ILLUSTRATION/VISUEL MIS EN AVANT (le sujet visuel occupe ~75-85% de la "
    "surface), une seule idée, hiérarchie claire, beaucoup d'espace négatif."
)

# Spécifications par plateforme de destination (format natif optimal).
PLATEFORMES_SPEC = {
    "Instagram":         {"ratio": "4:5",  "px": "1080x1350", "ar": "4:5"},
    "Facebook":          {"ratio": "4:5",  "px": "1080x1350", "ar": "4:5"},
    "TikTok":            {"ratio": "9:16", "px": "1080x1920", "ar": "9:16"},
    "LinkedIn":          {"ratio": "1:1",  "px": "1080x1080", "ar": "1:1"},
    "WhatsApp Business": {"ratio": "9:16", "px": "1080x1920", "ar": "9:16"},
}


def spec_visuel(plateforme, fmt):
    """Format cible : un format Story/Reel force le 9:16, sinon format natif plateforme."""
    if any(k in fmt for k in ("Story", "Reel")):
        return {"ratio": "9:16", "px": "1080x1920", "ar": "9:16"}
    return PLATEFORMES_SPEC.get(plateforme, {"ratio": "4:5", "px": "1080x1350", "ar": "4:5"})


def titre_court(titre):
    """Titre d'accroche court (≤ 6 mots) pour l'incrustation minimaliste du visuel."""
    mots = titre.replace("« ", "").replace(" »", "").split()
    court = " ".join(mots[:6])
    return court + ("…" if len(mots) > 6 else "")


# --------------------------------------------------------------------------- #
# Métadonnées des piliers
# --------------------------------------------------------------------------- #
PILIERS = {
    "PIL1": {"nom": "Pédagogie & Santé visuelle", "objectif": "Notoriété/Expertise",
             "personas": ["P1", "P2", "P3"], "plateformes": ["Instagram", "TikTok", "Facebook", "LinkedIn"]},
    "PIL2": {"nom": "Produits & Montures", "objectif": "Vente",
             "personas": ["P4", "P3", "P2"], "plateformes": ["Instagram", "TikTok", "Facebook"]},
    "PIL3": {"nom": "Preuve sociale & Témoignages", "objectif": "Confiance/Conversion",
             "personas": ["P1", "P3", "P2", "P4"], "plateformes": ["Facebook", "Instagram", "LinkedIn"]},
    "PIL4": {"nom": "Offres & Conversion", "objectif": "RDV/Vente",
             "personas": ["P1", "P2", "P3", "P4"], "plateformes": ["WhatsApp Business", "Facebook", "Instagram"]},
    "PIL5": {"nom": "Vie locale & Communauté", "objectif": "Notoriété locale",
             "personas": ["P1", "P5"], "plateformes": ["Facebook", "Instagram"]},
    "PIL6": {"nom": "Coulisses & Expertise B2B", "objectif": "Expertise/B2B",
             "personas": ["P5", "P2"], "plateformes": ["LinkedIn", "Facebook"]},
}

# Nombre de contenus par pilier (≈ répartition de la stratégie, somme = 180)
QUOTAS = {"PIL1": 54, "PIL2": 36, "PIL3": 27, "PIL4": 36, "PIL5": 18, "PIL6": 9}

PERSONAS = {
    "P1": "Awa, la maman prévoyante",
    "P2": "Koffi, le pro hyperconnecté",
    "P3": "Tante Mariam, la presbyte active",
    "P4": "Yann, le jeune stylé",
    "P5": "M. Diallo, le décideur B2B",
}

FORMATS = {
    "PIL1": ["Carrousel pédagogique", "Reel explicatif", "Infographie", "Vidéo face caméra"],
    "PIL2": ["Carrousel produit", "Reel essayage", "Photo studio", "Story collection"],
    "PIL3": ["Témoignage vidéo", "Carrousel avant/après", "Photo + citation", "Story avis"],
    "PIL4": ["Visuel CTA", "Story RDV", "Reel offre", "Carrousel offre"],
    "PIL5": ["Photo lifestyle", "Carrousel communauté", "Story locale", "Reel ambiance"],
    "PIL6": ["Article LinkedIn", "Carrousel expertise", "Vidéo coulisses", "Infographie pro"],
}

# Angles pour différencier les sujets réutilisés (garantit l'unicité des titres)
ANGLES = ["", " (édition Yopougon)", " : le guide", " — ce qu'il faut savoir",
          " expliqué simplement", " : nos conseils d'expert", " (cas réel)",
          " — questions/réponses", " : le vrai du faux"]

CTA = {
    "Notoriété/Expertise": "Enregistrez ce post et partagez-le à un proche concerné. 👀",
    "Vente": "Passez nous voir pour l'essayer, ou écrivez-nous sur WhatsApp. 👓",
    "Confiance/Conversion": "Vous aussi ? Écrivez-nous « VUE » sur WhatsApp pour votre bilan. 💬",
    "RDV/Vente": "📲 Réservez votre bilan en 2 clics : écrivez « RDV » sur WhatsApp.",
    "Notoriété locale": "Suivez-nous et taguez un voisin de Yopougon ! 🏘️",
    "Expertise/B2B": "Contactez-nous en message privé pour une offre entreprise. 🤝",
}

HASHTAGS = {
    "Instagram": "#LaGrandeVision #Yopougon #Abidjan225 #SantéVisuelle #Opticien #Lunettes "
                 "#Vue #CôteDIvoire #Optique #VoirLaVieEnGrand",
    "TikTok": "#santévisuelle #yopougon #abidjan #lunettes #opticien #cotedivoire225 #vue #fyp",
    "Facebook": "#LaGrandeVision #Yopougon #Abidjan #SantéVisuelle #Opticien #Optique",
    "LinkedIn": "#SantéVisuelle #Optique #Entreprise #BienÊtreAuTravail #CôteDIvoire #Abidjan",
    "WhatsApp Business": "#LaGrandeVision #Yopougon #RDV",
}

# --------------------------------------------------------------------------- #
# Construction de la liste ordonnée des 180 contenus
# --------------------------------------------------------------------------- #
def construire_sujets():
    """Retourne une liste de (pilier, titre) de longueur QUOTAS[pilier] par pilier,
    en réutilisant les sujets avec un angle distinct si nécessaire (titres uniques)."""
    out = {}
    for pil, quota in QUOTAS.items():
        pool = BANQUE[pil]
        items, vus = [], set()
        i = 0
        while len(items) < quota:
            base = pool[i % len(pool)]
            tour = i // len(pool)
            titre = base + ANGLES[tour % len(ANGLES)]
            if titre in vus:                 # collision improbable -> angle suivant
                titre = base + ANGLES[(tour + 1) % len(ANGLES)] + f" #{i}"
            vus.add(titre)
            items.append((pil, titre))
            i += 1
        out[pil] = items
    return out


def planifier():
    """Interleave pondéré : répartit les 180 contenus dans le temps en évitant
    les longues séries d'un même pilier. Renvoie la liste ordonnée (pilier, titre)."""
    par_pilier = construire_sujets()
    curseur = {p: 0 for p in QUOTAS}
    restant = dict(QUOTAS)
    sequence = []
    # Ordre de priorité d'alternance (gros piliers d'abord pour bien étaler)
    ordre = ["PIL1", "PIL4", "PIL2", "PIL3", "PIL5", "PIL6"]
    while len(sequence) < TOTAL:
        progres = False
        for p in ordre:
            # densité : on sert un pilier proportionnellement à son quota
            cible = QUOTAS[p] / TOTAL
            deja = sum(1 for s in sequence if s[0] == p)
            if restant[p] > 0 and (deja + 1) <= round(cible * (len(sequence) + 1)) + 1:
                pil_items = par_pilier[p]
                sequence.append(pil_items[curseur[p]])
                curseur[p] += 1
                restant[p] -= 1
                progres = True
                if len(sequence) >= TOTAL:
                    break
        if not progres:  # filet de sécurité : vider ce qui reste
            for p in ordre:
                while restant[p] > 0 and len(sequence) < TOTAL:
                    sequence.append(par_pilier[p][curseur[p]])
                    curseur[p] += 1
                    restant[p] -= 1
    return sequence


# --------------------------------------------------------------------------- #
# Fabrique d'un contenu complet à partir de (index, pilier, titre)
# --------------------------------------------------------------------------- #
def hook_pour(titre, objectif):
    t = titre.rstrip("?.!")
    if "?" in titre:
        return titre
    if objectif in ("RDV/Vente",):
        return f"Et si aujourd'hui était le bon jour pour {t.lower()} ?"
    if objectif in ("Vente",):
        return f"Vous hésitez encore ? {titre} 👇"
    return f"Saviez-vous que... {t.lower()} ? On vous explique. 👇"


def fabriquer(index, pil, titre):
    meta = PILIERS[pil]
    objectif = meta["objectif"]
    persona_id = meta["personas"][index % len(meta["personas"])]
    persona = PERSONAS[persona_id]
    plateforme = meta["plateformes"][index % len(meta["plateformes"])]
    fmt = FORMATS[pil][index % len(FORMATS[pil])]
    hook = hook_pour(titre, objectif)
    cta = CTA[objectif]
    htags = HASHTAGS[plateforme]

    spec = spec_visuel(plateforme, fmt)
    court = titre_court(titre)

    # --- Textes par plateforme ------------------------------------------------
    accroche = hook
    corps = (
        f"À La Grande Vision, votre cabinet d'optique à Yopougon, nous prenons soin "
        f"de la santé visuelle de toute la famille. {titre} — un sujet qui compte pour "
        f"votre confort au quotidien."
    )
    texte_fb = f"{accroche}\n\n{corps}\n\n{cta}\n\n📍 Yopougon, Abidjan · 📲 WhatsApp Business\n{HASHTAGS['Facebook']}"
    texte_ig = f"{accroche}\n\n{corps}\n\n{cta}\n\n{HASHTAGS['Instagram']}"
    texte_li = (
        f"{titre}\n\n{corps}\n\nChez La Grande Vision, l'expertise au service de votre vue. "
        f"{CTA['Expertise/B2B'] if objectif=='Expertise/B2B' else cta}\n\n{HASHTAGS['LinkedIn']}"
    )
    desc_tiktok = f"{accroche} {('— ' + titre) if titre not in accroche else ''}\n{HASHTAGS['TikTok']}"

    # --- Légende + description PRÊTE À COPIER (plateforme de destination) ------
    legende = legende_pour(plateforme, accroche, corps, cta, titre, objectif)
    description = f"{legende}\n\n{htags}"   # légende + hashtags, prêt à coller

    # --- Prompt visuel optimisé pour la PLATEFORME DE DESTINATION -------------
    # (texte minimaliste, illustration en avant, format natif, charte stricte)
    prompt_canva = (
        f"[Visuel {plateforme} · {spec['px']} ({spec['ratio']})] "
        f"Charte: fond Bleu Nuit #0A1F44 (dominante), accents Bleu Ciel #4BA3FF, détails & bouton en Gold #D4AF37, texte blanc. "
        f"Typographie: titre Montserrat ExtraBold, texte Poppins. "
        f"{STYLE_VISUEL} "
        f"Illustration mise en avant: scène/élément en lien avec « {titre} » "
        f"({recommander_visuel(pil).lower()}), pictogrammes ligne fine. "
        f"Incrustation texte (minimal): titre court « {court} » + petit label « La Grande Vision · Yopougon ». "
        f"Bouton Gold: « {cta_court(objectif)} ». Logo discret en bas. Rendu premium, médical, épuré."
    )
    prompt_mj = (
        f"Editorial illustration/photograph for {plateforme}, topic « {titre} » — {CHARTE_PROMPT}. "
        f"Illustration-forward, single strong focal subject (people, eyewear, eye, screen or clinic as relevant), "
        f"minimal on-image text, generous negative space for a short headline overlay. "
        f"Premium healthcare, soft natural light, 50mm look, clean composition. "
        f"--ar {spec['ar']} --stylize 250"
    )
    prompt_gpt = (
        f"Photographie professionnelle réaliste pour {plateforme} ({spec['px']}, {spec['ratio']}), compatible publicité Meta, sujet « {titre} ». "
        f"Sujet visuel mis en avant, texte minimal, espace négatif pour un titre court. "
        f"Cabinet d'optique premium à Abidjan (personnes, lunettes, ambiance médicale moderne). "
        f"Couleurs Bleu Nuit #0A1F44 / Bleu Ciel #4BA3FF / touches Gold #D4AF37, lumière douce, qualité studio."
    )

    visuel_reco = recommander_visuel(pil)
    kpi = kpi_pour(objectif)

    return {
        "index": index + 1,
        "pilier": pil, "pilier_nom": meta["nom"], "objectif": objectif,
        "persona_id": persona_id, "persona": persona, "plateforme": plateforme,
        "format": fmt, "ratio": spec["ratio"], "px": spec["px"],
        "titre": titre, "hook": hook, "cta": cta, "hashtags": htags,
        "texte_fb": texte_fb, "texte_ig": texte_ig, "texte_li": texte_li,
        "desc_tiktok": desc_tiktok, "legende": legende, "description": description,
        "prompt_canva": prompt_canva,
        "prompt_mj": prompt_mj, "prompt_gpt": prompt_gpt,
        "visuel": visuel_reco, "kpi": kpi,
    }


def legende_pour(plateforme, accroche, corps, cta, titre, objectif):
    """Légende (caption) sans hashtags, adaptée à la plateforme de destination."""
    if plateforme == "LinkedIn":
        cta_li = CTA["Expertise/B2B"] if objectif == "Expertise/B2B" else cta
        return (f"{titre}\n\n{corps}\n\nChez La Grande Vision, l'expertise au service de "
                f"votre vue. {cta_li}")
    if plateforme == "TikTok":
        return f"{accroche}\n{titre}"
    if plateforme == "Facebook":
        return f"{accroche}\n\n{corps}\n\n{cta}\n\n📍 Yopougon, Abidjan · 📲 WhatsApp Business"
    if plateforme == "WhatsApp Business":
        return (f"{accroche}\n\n{corps}\n\n{cta}\n\n📍 La Grande Vision · Yopougon, Abidjan")
    # Instagram (défaut)
    return f"{accroche}\n\n{corps}\n\n{cta}"


def cta_court(objectif):
    return {"RDV/Vente": "Prendre RDV", "Vente": "Voir en boutique",
            "Confiance/Conversion": "Écrire « VUE »", "Notoriété/Expertise": "En savoir plus",
            "Notoriété locale": "Nous suivre", "Expertise/B2B": "Nous contacter"}[objectif]


def recommander_visuel(pil):
    return {
        "PIL1": "Infographie/carrousel pédagogique, icônes ligne fine sur fond Bleu Nuit.",
        "PIL2": "Photo studio de montures sur fond neutre, lumière premium, détails Gold.",
        "PIL3": "Portrait client souriant + citation, ambiance chaleureuse et authentique.",
        "PIL4": "Visuel CTA fort, bouton Gold, mention WhatsApp bien visible.",
        "PIL5": "Photo lifestyle locale (Yopougon, famille), ambiance proximité.",
        "PIL6": "Visuel corporate sobre, coulisses du cabinet, technologie de mesure.",
    }[pil]


def kpi_pour(objectif):
    return {
        "Notoriété/Expertise": "Portée + enregistrements (sauvegardes) + partages",
        "Vente": "Clics profil + messages produit + visites boutique",
        "Confiance/Conversion": "Messages WhatsApp entrants + taux de confiance (avis)",
        "RDV/Vente": "Nombre de RDV générés via WhatsApp",
        "Notoriété locale": "Portée locale + abonnés + mentions/taggs",
        "Expertise/B2B": "Leads B2B + connexions/MP LinkedIn qualifiés",
    }[objectif]


# --------------------------------------------------------------------------- #
# Écriture des livrables
# --------------------------------------------------------------------------- #
def date_heure(i):
    jour = i // POSTS_PAR_JOUR
    d = DATE_DEBUT + timedelta(days=jour)
    h = HEURE_MATIN if i % POSTS_PAR_JOUR == 0 else HEURE_SOIR
    return d.isoformat(), h


def ecrire_calendrier(contenus):
    chemin = os.path.join(RACINE, "02-calendrier-editorial", "calendrier-editorial.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Date", "Heure", "Plateforme", "Objectif", "Persona", "Pilier",
                    "Sujet", "Titre", "Hook", "CTA", "Format", "Prompt Visuel",
                    "Prompt Video", "Statut"])
        for c in contenus:
            d, h = date_heure(c["index"] - 1)
            prompt_video = "Voir 04-scripts-video/" if c["index"] <= 60 else "—"
            w.writerow([c["index"], d, h, c["plateforme"], c["objectif"],
                        f'{c["persona_id"]} {c["persona"]}', f'{c["pilier"]} {c["pilier_nom"]}',
                        c["pilier_nom"], c["titre"], c["hook"], c["cta"], c["format"],
                        c["prompt_canva"][:80] + "…", prompt_video, "À produire"])
    return chemin


def ecrire_contenus(contenus):
    chemin = os.path.join(RACINE, "03-contenus", "contenus.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("# Les 180 contenus — La Grande Vision\n\n")
        f.write("> Généré automatiquement par `_generateur/generer.py`. "
                "Ne pas éditer à la main : modifier le générateur ou `sujets.py`.\n\n")
        f.write("Chaque fiche est directement exploitable (textes par plateforme, CTA, "
                "hashtags, prompts visuels, KPI).\n\n---\n\n")
        for c in contenus:
            d, h = date_heure(c["index"] - 1)
            f.write(f"## Contenu #{c['index']:03d} — {c['titre']}\n\n")
            f.write(f"- **Date/Heure :** {d} à {h}\n")
            f.write(f"- **Plateforme :** {c['plateforme']}\n")
            f.write(f"- **Objectif :** {c['objectif']}\n")
            f.write(f"- **Persona :** {c['persona_id']} — {c['persona']}\n")
            f.write(f"- **Pilier :** {c['pilier']} — {c['pilier_nom']}\n")
            f.write(f"- **Format recommandé :** {c['format']} — cible **{c['px']} ({c['ratio']})** pour {c['plateforme']}\n")
            f.write(f"- **Visuel recommandé :** {c['visuel']}\n")
            f.write(f"- **KPI attendu :** {c['kpi']}\n\n")
            f.write(f"**Hook :** {c['hook']}\n\n")
            f.write(f"### 📝 Description du post — prête à copier ({c['plateforme']})\n\n")
            f.write(f"```\n{c['description']}\n```\n\n")
            f.write(f"### 📸 Prompt visuel — {c['plateforme']} ({c['px']}, {c['ratio']}) "
                    f"· texte minimaliste, illustration en avant, charte\n\n")
            f.write(f"**Prompt Canva**\n\n```\n{c['prompt_canva']}\n```\n\n")
            f.write(f"**Prompt Midjourney**\n\n```\n{c['prompt_mj']}\n```\n\n")
            f.write(f"**Prompt GPT Image**\n\n```\n{c['prompt_gpt']}\n```\n\n")
            f.write("<details><summary>Textes pour les autres plateformes</summary>\n\n")
            f.write(f"**Facebook**\n\n```\n{c['texte_fb']}\n```\n\n")
            f.write(f"**Instagram**\n\n```\n{c['texte_ig']}\n```\n\n")
            f.write(f"**LinkedIn**\n\n```\n{c['texte_li']}\n```\n\n")
            f.write(f"**TikTok**\n\n```\n{c['desc_tiktok']}\n```\n\n")
            f.write("</details>\n\n")
            f.write("---\n\n")
    return chemin


def ecrire_scoring(contenus):
    """CSV prêt pour Google Sheets : colonnes de mesure vides + formules de score.
    Les formules sont écrites en syntaxe Google Sheets (lignes à partir de 2)."""
    chemin = os.path.join(RACINE, "08-scoring", "scoring.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Titre", "Plateforme", "Objectif",
                    "Portee", "Engagement", "Partages", "Commentaires", "Messages", "RDV",
                    "Score Engagement", "Score Portee", "Score Conversion", "Score RDV",
                    "Score Global", "Note", "Recommandation"])
        for c in contenus:
            r = c["index"] + 1  # ligne tableur (en-tête = ligne 1)
            # Pondérations : engagement = (eng+partages+comm)/portée
            score_eng = f"=IFERROR(ROUND(((F{r}+G{r}+H{r})/MAX(E{r},1))*100,1),0)"
            score_por = f"=IFERROR(ROUND((E{r}/MAX(MAX($E$2:$E${TOTAL+1}),1))*100,1),0)"
            score_conv = f"=IFERROR(ROUND((I{r}/MAX(E{r},1))*100,1),0)"
            score_rdv = f"=IFERROR(ROUND((J{r}/MAX(I{r},1))*100,1),0)"
            # Score global pondéré (engagement 30, portée 20, conversion 25, rdv 25)
            score_glob = f"=ROUND(K{r}*0.3+L{r}*0.2+M{r}*0.25+N{r}*0.25,1)"
            note = (f'=IFS(O{r}>=80,"A",O{r}>=60,"B",O{r}>=40,"C",O{r}>=20,"D",TRUE,"E")')
            reco = (f'=IFS(P{r}="A","À reproduire",OR(P{r}="B",P{r}="C"),'
                    f'"À optimiser",TRUE,"À abandonner")')
            w.writerow([c["index"], c["titre"], c["plateforme"], c["objectif"],
                        "", "", "", "", "", "",
                        score_eng, score_por, score_conv, score_rdv,
                        score_glob, note, reco])
    return chemin


def ecrire_json(contenus):
    """Données structurées consommées par l'outil de revue des visuels
    (outils/revue-visuels). Inclut prompts + aperçus Canva connus."""
    dossier = os.path.join(RACINE, "_donnees")
    os.makedirs(dossier, exist_ok=True)
    items = []
    for c in contenus:
        d, h = date_heure(c["index"] - 1)
        items.append({
            "id": c["index"], "date": d, "heure": h,
            "plateforme": c["plateforme"], "objectif": c["objectif"],
            "persona": f'{c["persona_id"]} — {c["persona"]}',
            "pilier": c["pilier"], "pilier_nom": c["pilier_nom"],
            "titre": c["titre"], "hook": c["hook"], "cta": c["cta"],
            "format": c["format"], "ratio": c["ratio"], "px": c["px"],
            "visuel": c["visuel"], "kpi": c["kpi"],
            "hashtags": c["hashtags"],
            "legende": c["legende"], "description": c["description"],
            "prompt_canva": c["prompt_canva"],
            "prompt_mj": c["prompt_mj"],
            "prompt_gpt": c["prompt_gpt"],
            "apercus": CANVA_VISUELS.get(c["index"], {}).get("apercus", []),
            "image": CANVA_VISUELS.get(c["index"], {}).get("image", ""),
            "statut": "Validé" if c["index"] in CANVA_VISUELS else "À produire",
        })
    meta = {
        "client": "La Grande Vision",
        "secteur": "Cabinet d'optique",
        "lieu": "Yopougon, Abidjan — Côte d'Ivoire",
        "charte": {"bleu_nuit": "#0A1F44", "bleu_ciel": "#4BA3FF", "gold": "#D4AF37"},
        "total": len(items),
        "contenus": items,
    }
    chemin = os.path.join(dossier, "campagne.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return chemin


# --------------------------------------------------------------------------- #
# Scripts vidéo (60) — basés sur PIL1 (pédagogie) et PIL2 (produits)
# --------------------------------------------------------------------------- #
# Réseaux vidéo : hashtags + format de couverture/miniature (vidéo verticale)
VIDEO_RESEAUX = {
    "Reel Instagram": {"reseau": "Instagram", "tags": HASHTAGS["Instagram"]},
    "TikTok":         {"reseau": "TikTok",    "tags": HASHTAGS["TikTok"]},
    "Short YouTube":  {"reseau": "YouTube Shorts",
                       "tags": "#Shorts #SantéVisuelle #Yopougon #Abidjan #Lunettes #Opticien #Vue #CôteDIvoire225"},
}
COVER_PX, COVER_RATIO = "1080x1920", "9:16"   # couverture verticale (Reel/TikTok/Short)


def legende_video(sujet, cta):
    """Légende courte (style vidéo sociale), sans hashtags."""
    return f"{accroche_video(sujet)}\n{sujet}\n\n{cta}\n📍 La Grande Vision · Yopougon"


def prompt_cover_canva(sujet, reseau):
    return (
        f"[Couverture/miniature {reseau} · {COVER_PX} ({COVER_RATIO}), vidéo verticale] "
        f"Charte: fond Bleu Nuit #0A1F44, accents Bleu Ciel #4BA3FF, détails Gold #D4AF37, texte blanc. "
        f"Typographie: Montserrat ExtraBold. {STYLE_VISUEL} "
        f"Illustration en avant: visage expressif (regard caméra) ou scène en lien avec « {sujet} », énergie, "
        f"forte lisibilité en petite taille (contraste élevé). "
        f"Accroche courte (≤4 mots) en haut: « {titre_court(sujet)} » + petit label « La Grande Vision ». "
        f"Style premium médical, hook visuel qui donne envie de cliquer."
    )


def prompt_cover_mj(sujet, reseau):
    return (
        f"Vertical 9:16 short-video cover thumbnail for {reseau}, topic « {sujet} » — {CHARTE_PROMPT}. "
        f"Expressive person looking straight at camera, bold simple illustration-forward composition, "
        f"minimal text space at top, very high contrast for small preview. "
        f"--ar 9:16 --stylize 250"
    )


def ecrire_scripts_video():
    sujets = [("PIL1", s) for s in BANQUE["PIL1"]] + [("PIL2", s) for s in BANQUE["PIL2"]]
    sujets = sujets[:60]
    chemin = os.path.join(RACINE, "04-scripts-video", "scripts-video.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("# 60 Scripts Vidéo courts — La Grande Vision\n\n")
        f.write("> Généré par `_generateur/generer.py`. Format Reels / TikTok / Shorts, "
                "30–60 s. Structure : Hook → Problème → Démonstration → Solution → CTA.\n\n")
        f.write("Charte respectée : incrustations en Montserrat/Poppins, couleurs "
                "Bleu Nuit / Bleu Ciel / Gold. Chaque script embarque sa **description prête à "
                "copier** et son **prompt de couverture/miniature** à la charte (vertical 9:16, "
                "texte minimaliste, illustration en avant).\n\n---\n\n")
        formats = ["Reel Instagram", "TikTok", "Short YouTube"]
        for i, (pil, sujet) in enumerate(sujets, 1):
            fmt = formats[i % 3]
            res = VIDEO_RESEAUX[fmt]
            persona = PERSONAS[PILIERS[pil]["personas"][i % len(PILIERS[pil]["personas"])]]
            cta = CTA["RDV/Vente"] if pil == "PIL1" else CTA["Vente"]
            description = f"{legende_video(sujet, cta)}\n\n{res['tags']}"
            f.write(f"## Script #{i:02d} — {sujet}\n\n")
            f.write(f"- **Format :** {fmt} · **Durée :** 30–60 s · **Couverture cible :** "
                    f"{COVER_PX} ({COVER_RATIO}) · **Pilier :** {pil} "
                    f"({PILIERS[pil]['nom']}) · **Persona :** {persona}\n\n")
            f.write("| Temps | Bloc | Voix off / Texte | À l'écran |\n|---|---|---|---|\n")
            f.write(f"| 0–3 s | **Hook** | « {accroche_video(sujet)} » | Gros titre Montserrat sur fond Bleu Nuit |\n")
            f.write(f"| 3–10 s | **Problème** | « {probleme_video(sujet)} » | Plan rapproché, ambiance quotidienne |\n")
            f.write(f"| 10–35 s | **Démonstration** | « {demo_video(sujet)} » | Démonstration au cabinet / à l'écran |\n")
            f.write(f"| 35–50 s | **Solution** | « À La Grande Vision, on vous propose un bilan et la solution adaptée. » | Opticien souriant, montures, détails Gold |\n")
            f.write(f"| 50–60 s | **CTA** | « {cta} » | Bandeau Gold + logo + WhatsApp |\n\n")
            f.write(f"**Incrustations :** titre « {sujet} » · « Voir la vie en grand » · « 📲 WhatsApp »\n\n")
            f.write(f"### 📝 Description du post — prête à copier ({res['reseau']})\n\n")
            f.write(f"```\n{description}\n```\n\n")
            f.write(f"### 📸 Prompt de couverture/miniature — {res['reseau']} ({COVER_PX}, {COVER_RATIO}) "
                    f"· texte minimaliste, illustration en avant, charte\n\n")
            f.write(f"**Prompt Canva**\n\n```\n{prompt_cover_canva(sujet, res['reseau'])}\n```\n\n")
            f.write(f"**Prompt Midjourney**\n\n```\n{prompt_cover_mj(sujet, res['reseau'])}\n```\n\n")
            f.write("---\n\n")
    return chemin


def accroche_video(s):
    if "?" in s:
        return s
    return f"Stop ! Si vous vous demandez « {s.lower()} », regardez ça."


def probleme_video(s):
    return ("Beaucoup de gens à Yopougon vivent avec ce problème sans le savoir : "
            "fatigue, vision floue, maux de tête...")


def demo_video(s):
    return (f"Voici ce qu'il faut comprendre sur « {s.lower()} » — en clair, "
            "sans jargon, avec un exemple concret.")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    sequence = planifier()
    assert len(sequence) == TOTAL, f"{len(sequence)} != {TOTAL}"
    contenus = [fabriquer(i, pil, titre) for i, (pil, titre) in enumerate(sequence)]

    c1 = ecrire_calendrier(contenus)
    c2 = ecrire_contenus(contenus)
    c3 = ecrire_scoring(contenus)
    c4 = ecrire_scripts_video()
    c5 = ecrire_json(contenus)

    # petit récapitulatif de répartition
    rep = {}
    for c in contenus:
        rep[c["pilier"]] = rep.get(c["pilier"], 0) + 1
    print("✅ Génération terminée.")
    print(f"   Calendrier : {c1}")
    print(f"   Contenus   : {c2}")
    print(f"   Scoring    : {c3}")
    print(f"   Scripts    : {c4}")
    print(f"   Données    : {c5}")
    print(f"   Total contenus : {len(contenus)}")
    print(f"   Répartition par pilier : {rep}")


if __name__ == "__main__":
    main()
