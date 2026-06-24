#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""awema — opérateur de connexions multi-plateformes (CLI + agent /awema).

Gère les identifiants (clés / tokens / mots de passe) de chaque plateforme :
  • garde le DERNIER identifiant courant + un HISTORIQUE (liste) dans un fichier LOCAL
    .awema/credentials.json (gitignoré — JAMAIS poussé) ;
  • connaît les identifiants requis par plateforme (scripts/awema-connectors.json) ;
  • lance la procédure de connexion d'une plateforme avec ces identifiants ;
  • « incrémente » (rotation) un identifiant : le nouveau devient courant, l'ancien part en historique.

Conçu pour être piloté en langage naturel par la commande /awema (l'agent ne demande QUE
les valeurs inconnues à l'utilisateur), ou utilisé directement en CLI.

Commandes :
  awema list                         plateformes connues + état (identifiants présents ?)
  awema needs <plat> [--json]        identifiants requis + lesquels manquent
  awema set  <plat> KEY=VAL ...      enregistre/incrémente des identifiants (rotation + historique)
  awema set  <plat> KEY --stdin      lit la valeur (secrète) sur l'entrée standard
  awema get  <plat> [--reveal]       métadonnées (valeurs masquées) + taille d'historique
  awema env  <plat>                  lignes export/set pour utiliser les identifiants stockés
  awema connect <plat>               lance la connexion (avec les identifiants stockés)
  awema rotate  <plat> KEY=VAL       incrémente un identifiant (garde l'ancien en historique)
  awema history <plat> [--reveal]    historique des identifiants (masqué par défaut)
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(RACINE, "scripts", "awema-connectors.json")
STORE_DIR = os.path.join(RACINE, ".awema")
STORE = os.path.join(STORE_DIR, "credentials.json")
HIST_MAX = 10


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def manifest():
    return json.load(open(MANIFEST, encoding="utf-8")).get("platforms", {})


def load():
    try:
        return json.load(open(STORE, encoding="utf-8"))
    except FileNotFoundError:
        return {"platforms": {}}


def save(store):
    os.makedirs(STORE_DIR, exist_ok=True)
    gi = os.path.join(STORE_DIR, ".gitignore")          # filet de sécurité : ce dossier ne se versionne pas
    if not os.path.exists(gi):
        open(gi, "w").write("*\n")
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(STORE, 0o600)
    except Exception:
        pass


def mask(v):
    if v is None:
        return "—"
    s = str(v)
    return s if len(s) <= 6 else s[:3] + "…" + s[-3:]


def plat_or_die(p):
    m = manifest()
    if p not in m:
        sys.exit(f"❌ plateforme inconnue : {p}. Connues : {', '.join(m)}")
    return m[p]


def current(store, p):
    return store["platforms"].get(p, {}).get("current", {})


def known_value(store, p, key):
    cur = current(store, p)
    v = cur.get(key)
    return v if v not in (None, "") else os.environ.get(key)


def cmd_list():
    m = manifest()
    store = load()
    for p, info in m.items():
        cur = current(store, p)
        req = [k["name"] for k in info["keys"] if not k.get("optional") and not k.get("managed")]
        have = sum(1 for k in req if known_value(store, p, k))
        etat = (f"maj {cur.get('_set_at', '')[:10]}" if cur.get("_set_at") else "vide")
        print(f"• {p:11} {info['label']:30} identifiants {have}/{len(req)} · {etat}")


def cmd_needs(p, as_json):
    info = plat_or_die(p)
    store = load()
    out = []
    for k in info["keys"]:
        val = known_value(store, p, k["name"])
        out.append({"key": k["name"], "present": bool(val), "secret": k.get("secret", False),
                    "optional": k.get("optional", False), "managed": k.get("managed", False),
                    "prompt": k.get("prompt", ""), "github": k.get("github")})
    if as_json:
        print(json.dumps({"platform": p, "label": info["label"], "keys": out}, ensure_ascii=False))
        return
    print(f"{info['label']} — identifiants :")
    for k in out:
        tag = "✅" if k["present"] else ("(optionnel)" if k["optional"] else "❌ manquant")
        print(f"  {k['key']:26} {tag}  {k['prompt']}")
    miss = [k["key"] for k in out if not k["present"] and not k["optional"] and not k["managed"]]
    print("À fournir :", ", ".join(miss) if miss else "— tout est là")


def _archive_set(store, p, newvals):
    pl = store["platforms"].setdefault(p, {"current": {}, "history": []})
    cur = dict(pl.get("current", {}))
    change = any(cur.get(k) != v for k, v in newvals.items())
    if change and any(k != "_set_at" for k in cur):     # archive l'ancienne version si elle change
        snap = dict(cur)
        snap["_archived_at"] = _now()
        pl.setdefault("history", []).insert(0, snap)
        pl["history"] = pl["history"][:HIST_MAX]
    cur.update(newvals)
    cur["_set_at"] = _now()
    pl["current"] = cur


def cmd_set(p, pairs, stdin_key=None):
    plat_or_die(p)
    store = load()
    vals = {}
    for kv in pairs:
        if "=" not in kv:
            sys.exit(f"❌ format attendu KEY=VALUE (reçu : {kv})")
        k, v = kv.split("=", 1)
        vals[k] = v
    if stdin_key:
        vals[stdin_key] = sys.stdin.read().strip()
    if not vals:
        sys.exit("❌ rien à enregistrer.")
    _archive_set(store, p, vals)
    save(store)
    n = len(store["platforms"][p].get("history", []))
    print(f"✅ {p} : {', '.join(vals)} enregistré(s). Historique : {n} version(s) précédente(s).")


def cmd_rotate(p, pairs):
    cmd_set(p, pairs)
    print("↻ rotation effectuée — l'ancienne valeur est conservée en historique (awema history "
          + p + ").")


def cmd_get(p, reveal):
    info = plat_or_die(p)
    store = load()
    pl = store["platforms"].get(p, {})
    cur = pl.get("current", {})
    print(f"{info['label']} — courant (maj {cur.get('_set_at', '—')}) :")
    for k in info["keys"]:
        v = cur.get(k["name"]) or os.environ.get(k["name"])
        src = " (env)" if (not cur.get(k["name"]) and os.environ.get(k["name"])) else ""
        disp = (v if (reveal or not k.get("secret")) else mask(v)) if v else "—"
        print(f"  {k['name']:26} {disp}{src}")
    print(f"Historique : {len(pl.get('history', []))} version(s).")


def cmd_env(p):
    info = plat_or_die(p)
    store = load()
    cur = current(store, p)
    win = os.name == "nt"
    for k in info["keys"]:
        v = cur.get(k["name"]) or os.environ.get(k["name"])
        if v:
            print((f"set {k['name']}={v}") if win else (f"export {k['name']}={v}"))


def cmd_history(p, reveal):
    info = plat_or_die(p)
    store = load()
    hist = store["platforms"].get(p, {}).get("history", [])
    if not hist:
        print("Aucun historique pour " + p + ".")
        return
    for i, h in enumerate(hist):
        line = f"#{i + 1} archivé {h.get('_archived_at', '')[:19]} :"
        for k in info["keys"]:
            if k["name"] in h:
                v = h[k["name"]]
                line += f" {k['name']}={v if reveal or not k.get('secret') else mask(v)}"
        print(line)


def cmd_connect(p):
    info = plat_or_die(p)
    store = load()
    miss = [k["name"] for k in info["keys"]
            if not k.get("optional") and not k.get("managed") and not known_value(store, p, k["name"])]
    if miss:
        print("❌ identifiants manquants :", ", ".join(miss))
        print("   → fournis-les :  awema set " + p + " " + " ".join(f"{m}=…" for m in miss))
        sys.exit(2)
    cmds = info.get("commands", {})
    cmd = cmds.get("connect") or cmds.get("onboard")
    if not cmd:
        print("ℹ️ Pas de commande de connexion directe pour " + p + ". Voir :", info.get("doc", ""))
        return
    env = dict(os.environ)
    for k in info["keys"]:
        v = known_value(store, p, k["name"])
        if v:
            env[k["name"]] = v
    print("▶", cmd)
    sys.exit(subprocess.call(cmd, shell=True, cwd=RACINE, env=env))


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    c = a[0]
    try:
        if c == "list":
            cmd_list()
        elif c == "needs" and len(a) >= 2:
            cmd_needs(a[1], "--json" in a)
        elif c == "set" and len(a) >= 3 and "--stdin" in a:
            key = [x for x in a[2:] if x != "--stdin"][0]
            cmd_set(a[1], [], stdin_key=key)
        elif c == "set" and len(a) >= 3:
            cmd_set(a[1], [x for x in a[2:] if "=" in x])
        elif c == "rotate" and len(a) >= 3:
            cmd_rotate(a[1], [x for x in a[2:] if "=" in x])
        elif c == "get" and len(a) >= 2:
            cmd_get(a[1], "--reveal" in a)
        elif c == "env" and len(a) >= 2:
            cmd_env(a[1])
        elif c == "history" and len(a) >= 2:
            cmd_history(a[1], "--reveal" in a)
        elif c == "connect" and len(a) >= 2:
            cmd_connect(a[1])
        else:
            print(__doc__)
            sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        sys.exit(f"❌ {e}")


if __name__ == "__main__":
    main()
