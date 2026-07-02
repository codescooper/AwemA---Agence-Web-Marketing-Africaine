"""Invariant : build.py n'embarque les contenus d'une campagne dans le registre que si son
campagne.json reste sous SEUIL_CAMPAGNE ; au-delà → {"total", "differe": true} (chargé à la
demande par les pages). Sans réseau, sur une arborescence temporaire."""
import json
import os
import tempfile
import unittest

from tests.util import charger


def _client(base, slug, campagne=None):
    d = os.path.join(base, "modules", "marketing", "clients", slug, "_donnees")
    os.makedirs(d)
    with open(os.path.join(d, "client.json"), "w", encoding="utf-8") as f:
        json.dump({"id": slug, "nom": slug.title()}, f)
    if campagne is not None:
        with open(os.path.join(d, "campagne.json"), "w", encoding="utf-8") as f:
            json.dump(campagne, f, ensure_ascii=False)


class TestSeuilCampagne(unittest.TestCase):
    def _registre(self, tmp):
        b = charger("outils/_data/build.py", "build_test")
        b.RACINE = tmp
        b.ICI = os.path.join(tmp, "out")
        os.makedirs(b.ICI, exist_ok=True)
        b.main()
        t = open(os.path.join(b.ICI, "agence.js"), encoding="utf-8").read()
        return {c["id"]: c for c in json.loads(t.split("=", 1)[1].rstrip().rstrip(";"))["clients"]}

    def test_petite_campagne_embarquee_grosse_differee(self):
        with tempfile.TemporaryDirectory() as tmp:
            _client(tmp, "petit", {"total": 2, "contenus": [{"titre": "a"}, {"titre": "b"}]})
            _client(tmp, "gros", {"total": 3, "contenus": [{"titre": "x" * 30000}] * 3})  # > 64 Ko
            _client(tmp, "sans", None)
            reg = self._registre(tmp)
            # petite : contenus embarqués tels quels
            self.assertEqual(len(reg["petit"]["campagne"]["contenus"]), 2)
            self.assertNotIn("differe", reg["petit"]["campagne"])
            # grosse : résumé seulement (total conservé, pas de contenus, marqueur differe)
            self.assertTrue(reg["gros"]["campagne"]["differe"])
            self.assertEqual(reg["gros"]["campagne"]["total"], 3)
            self.assertNotIn("contenus", reg["gros"]["campagne"])
            # sans campagne : null, comme avant
            self.assertIsNone(reg["sans"]["campagne"])


if __name__ == "__main__":
    unittest.main()
