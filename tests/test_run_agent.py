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


if __name__ == "__main__":
    unittest.main()
