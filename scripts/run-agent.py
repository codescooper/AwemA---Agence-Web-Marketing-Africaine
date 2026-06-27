#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exécute un agent IA AWEMA sur un client (ou tous) et écrit sa sortie JSON additive.

Lit le manifeste `scripts/agents.json`, rassemble les entrées du client (reseaux.json,
memoire.json, campagne.json), appelle Claude via `awema_ai`, valide la sortie contre
l'enveloppe commune, puis écrit `_donnees/_agents/<agent>.json`. **Additif** : ne modifie
jamais les données réelles existantes. **Skip gracieux** sans clé IA.

Usage :
  python3 scripts/run-agent.py <agent> <slug-client>
  python3 scripts/run-agent.py <agent> --all
  python3 scripts/run-agent.py --list
"""
import glob
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)
import awema_ai  # noqa: E402

MANIFEST = os.path.join(ICI, "agents.json")


def _agents():
    return (json.load(open(MANIFEST, encoding="utf-8")) or {}).get("agents", {})


def _lire(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def _clients():
    motif = os.path.join(RACINE, "departements", "*", "clients", "*", "_donnees", "client.json")
    out = []
    for cj in sorted(glob.glob(motif)):
        out.append((json.load(open(cj, encoding="utf-8")), os.path.dirname(cj)))
    return out


def _entrees(defn, donnees):
    """Rassemble les entrées déclarées par l'agent (fichiers existants seulement)."""
    dispo, ctx = [], {}
    mapping = {"reseaux": "reseaux.json", "memoire": "memoire.json", "campagne": "campagne.json"}
    for e in defn.get("entrees", []):
        d = _lire(os.path.join(donnees, mapping.get(e, e + ".json")))
        if d is not None:
            ctx[e] = d
            dispo.append(mapping.get(e, e + ".json"))
    return ctx, dispo


def _executer(nom, defn, client, donnees):
    ctx, fichiers = _entrees(defn, donnees)
    if not ctx:
        return None, "aucune entrée disponible (rien à analyser)"
    prompt = (f"{defn.get('instruction','')}\n\n"
              f"Client : {client.get('nom')} ({client.get('secteur','')}).\n"
              f"Données disponibles (JSON) :\n{json.dumps(ctx, ensure_ascii=False)[:12000]}")
    schema_hint = defn.get("schema_hint") or '{"items":[{"titre":"...","explication":"..."}]}'
    try:
        rep = awema_ai.chat(prompt, system=defn.get("systeme"),
                            schema_hint=schema_hint, model=defn.get("modele"))
    except Exception as e:
        return None, f"appel IA échoué : {e}"
    if rep is None:
        return None, "skip (pas de clé IA)"
    liste = defn.get("liste", "items")                       # clé de la liste principale
    if isinstance(rep, list):
        items = rep
        extra = {}
    elif isinstance(rep, dict):
        items = rep.get(liste, rep.get("items", []))
        extra = {k: rep[k] for k in defn.get("champs_sortie", []) if k in rep}
    else:
        items, extra = [], {}
    env = awema_ai.enveloppe(
        nom, items if isinstance(items, list) else [], awema_ai.modele_actif(defn.get("modele")),
        {"client": client.get("id"), "fichiers": fichiers, "genere_par": "run-agent.py"})
    env.update(extra)                                        # champs structurés en plus d'items
    ok, err = awema_ai.valider_enveloppe(env, defn.get("item_requis"))
    if not ok:
        return None, "sortie invalide : " + " ; ".join(err[:3])
    return env, None


def aggreger_actions(reseaux, agents):
    """Agrège les « actions du jour » : alertes DÉTERMINISTES (sans IA) depuis reseaux.json
    + meilleures propositions des agents si déjà générées. Fonction PURE (testable).
    Chaque item : {priorite(1-3), type, titre, detail, source, action:{label, kind, target}}."""
    items, r = [], (reseaux or {})
    cad = r.get("cadence") or {}
    jd = cad.get("jours_depuis")
    if jd is not None and jd > 7:
        if jd > 90:        # dégradation gracieuse : au-delà de 90 j, la donnée est peu fiable
            titre, detail = "Aucune publication récente détectée", "Relance la production de contenu."
        else:
            titre, detail = f"Cadence en retard — {jd} j sans publier", "La régularité nourrit l'algorithme. Publie aujourd'hui."
        items.append({"priorite": 1, "type": "alerte", "titre": titre, "detail": detail,
                      "source": "cadence", "action": {"label": "Voir la présence", "kind": "view", "target": "reseaux"}})
    ar = r.get("a_repondre") or {}
    if ar.get("total"):
        items.append({"priorite": 1, "type": "inbox", "titre": f"{ar['total']} commentaire(s) à répondre",
                      "detail": "Réponds vite pour entretenir la communauté.",
                      "source": "a_repondre", "action": {"label": "Répondre", "kind": "view", "target": "reseaux"}})
    ev = r.get("evolution_audience") or []
    if (len(ev) >= 2 and isinstance(ev[-1].get("valeur"), (int, float))
            and isinstance(ev[-2].get("valeur"), (int, float)) and ev[-1]["valeur"] < ev[-2]["valeur"]):
        items.append({"priorite": 2, "type": "alerte", "titre": "Audience en baisse",
                      "detail": f"{ev[-2]['valeur']} → {ev[-1]['valeur']} abonnés.",
                      "source": "evolution_audience", "action": {"label": "Analyser", "kind": "view", "target": "reseaux"}})
    tc = r.get("types_contenu") or {}
    if tc:
        best = max(tc.items(), key=lambda kv: (kv[1] or {}).get("engagement_moyen", 0))
        if best[1] and best[1].get("engagement_moyen"):
            items.append({"priorite": 3, "type": "opportunite", "titre": f"Ton format gagnant : {best[0]}",
                          "detail": f"Engagement moyen {best[1]['engagement_moyen']} — reproduis-le.",
                          "source": "types_contenu", "action": {"label": "Idées créatives", "kind": "view", "target": "overview"}})
    ag = agents or {}
    recos = [i for i in ((ag.get("analyste") or {}).get("items") or []) if i.get("type") == "reco"]
    if recos:
        it = recos[0]
        items.append({"priorite": 2, "type": "reco", "titre": it.get("titre", ""),
                      "detail": it.get("action") or it.get("explication", ""),
                      "source": "analyste", "action": {"label": "Voir l'analyse", "kind": "view", "target": "reseaux"}})
    plan = (ag.get("stratege") or {}).get("items") or []
    if plan:
        p = plan[0]
        items.append({"priorite": 2, "type": "plan", "titre": f"Publie : {p.get('angle', '')}",
                      "detail": f"{p.get('reseau', '')} · {p.get('format', '')}" + (f" · {p.get('jour')}" if p.get("jour") else ""),
                      "source": "stratege", "action": {"label": "Voir le plan", "kind": "view", "target": "overview"}})
    idees = (ag.get("creatif") or {}).get("items") or []
    if idees:
        it = idees[0]
        items.append({"priorite": 3, "type": "creatif", "titre": f"Idée prête : {it.get('hook', '')}",
                      "detail": f"{it.get('reseau', '')} · {it.get('format', '')}",
                      "source": "creatif", "action": {"label": "Voir les idées", "kind": "view", "target": "overview"}})
    items.sort(key=lambda x: x.get("priorite", 9))
    return items[:6]


def _actions_du_jour(client, donnees):
    reseaux = _lire(os.path.join(donnees, "reseaux.json"))
    ag = {}
    for n in ("analyste", "stratege", "creatif"):
        d = _lire(os.path.join(donnees, "_agents", n + ".json"))
        if d:
            ag[n] = d
    items = aggreger_actions(reseaux, ag)
    return awema_ai.enveloppe("actions-du-jour", items, "agrégation (sans IA)",
                              {"client": client.get("id"), "genere_par": "run-agent.py"})


def _ecrire(donnees, nom, env):
    d = os.path.join(donnees, "_agents")
    os.makedirs(d, exist_ok=True)
    json.dump(env, open(os.path.join(d, nom + ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def main():
    a = sys.argv[1:]
    agents = _agents()
    if not a or a[0] == "--list":
        print("Agents disponibles :")
        for k, v in agents.items():
            print(f"  • {k:14} {v.get('role','')}")
        print(f"  • {'actions-du-jour':14} Agrège alertes + propositions → « 3 choses à faire » (SANS clé IA requise)")
        print("\nClé IA :", "✅ présente" if awema_ai.disponible()
              else "❌ absente → agents IA en skip gracieux ; actions-du-jour fonctionne quand même")
        return
    nom = a[0]
    # Agrégateur proactif : déterministe, ne nécessite PAS de clé IA
    if nom == "actions-du-jour":
        cibles = _clients()
        if "--all" not in a:
            slug = a[1] if len(a) > 1 else None
            cibles = [(c, d) for c, d in cibles if c.get("id") == slug]
            if not cibles:
                sys.exit(f"❌ client introuvable : {slug}")
        n = 0
        for client, donnees in cibles:
            env = _actions_du_jour(client, donnees)
            if env["items"]:                                  # n'écrit que s'il y a des actions
                _ecrire(donnees, "actions-du-jour", env)
                n += 1
                print(f"  ✓ actions-du-jour · {client.get('id')} — {len(env['items'])} action(s)")
            else:
                print(f"  · actions-du-jour · {client.get('id')} — rien à signaler")
        print(f"✅ actions-du-jour : {n} client(s) avec des actions. Régénère : python3 outils/_data/build.py")
        return
    if nom not in agents:
        sys.exit(f"❌ agent inconnu : {nom} (voir --list)")
    if not awema_ai.disponible():
        print(f"ℹ️ Pas de clé IA → agent « {nom} » ignoré (skip gracieux). Aucune écriture.")
        return
    cibles = _clients()
    if "--all" not in a:
        slug = a[1] if len(a) > 1 else None
        cibles = [(c, d) for c, d in cibles if c.get("id") == slug]
        if not cibles:
            sys.exit(f"❌ client introuvable : {slug}")
    n = 0
    for client, donnees in cibles:
        env, erreur = _executer(nom, agents[nom], client, donnees)
        if env:
            _ecrire(donnees, nom, env)
            n += 1
            print(f"  ✓ {nom} · {client.get('id')} — {len(env['items'])} item(s)")
        else:
            print(f"  · {nom} · {client.get('id')} — {erreur}")
    print(f"✅ {nom} : {n} client(s). Régénère le registre : python3 outils/_data/build.py")


if __name__ == "__main__":
    main()
