"""Invariant : _entrees() ne rassemble QUE les fichiers présents (skip gracieux des manquants)."""
import json
import os
import tempfile
import unittest

from tests.util import charger

ra = charger("scripts/run-agent.py", "ra_test")


class TestEntrees(unittest.TestCase):
    def test_ne_prend_que_les_fichiers_presents(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "reseaux.json"), "w", encoding="utf-8") as f:
                json.dump({"global": {"abonnes": 10}}, f)
            ctx, dispo = ra._entrees({"entrees": ["reseaux", "memoire", "campagne"]}, d)
            self.assertIn("reseaux", ctx)
            self.assertNotIn("memoire", ctx)
            self.assertEqual(dispo, ["reseaux.json"])

    def test_rien_disponible(self):
        with tempfile.TemporaryDirectory() as d:
            ctx, dispo = ra._entrees({"entrees": ["reseaux"]}, d)
            self.assertEqual(ctx, {})
            self.assertEqual(dispo, [])

    def test_entrees_vides(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(ra._entrees({"entrees": []}, d), ({}, []))


class TestContexteJson(unittest.TestCase):
    def test_toujours_json_valide_et_petites_entrees_entieres(self):
        ctx = {"memoire": {"ton": "chaleureux"}, "reseaux": {"abonnes": 100}}
        out = json.loads(ra._contexte_json(ctx, budget=24000))  # ne doit jamais lever
        self.assertEqual(out["memoire"]["ton"], "chaleureux")
        self.assertEqual(out["reseaux"]["abonnes"], 100)

    def test_entree_trop_grosse_est_bornee_sans_casser_le_json(self):
        # Régression (audit) : l'ancien [:12000] coupait en plein JSON → mémoire/campagne éjectées.
        ctx = {"memoire": {"ton": "chaleureux"}, "campagne": {"gros": "x" * 50000}}
        out = json.loads(ra._contexte_json(ctx, budget=2000))  # JSON toujours valide malgré l'énorme entrée
        self.assertEqual(out["memoire"]["ton"], "chaleureux")   # la petite entrée prioritaire est préservée
        self.assertTrue(out["campagne"].get("_tronque"))        # la grosse est bornée, pas coupée


if __name__ == "__main__":
    unittest.main()
