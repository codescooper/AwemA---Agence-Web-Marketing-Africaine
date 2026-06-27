"""Invariant : registre de délivrance des licences (preuve) + validation de format."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import awema  # noqa: E402


class TestLicence(unittest.TestCase):
    def test_ledger_incremente_et_hash(self):
        led = {"licences": []}
        e1 = awema.licence_ajouter(led, "Agence A", "a@x.com", "AWEMA-1111-2222-3333", "2026-06-26T10:00:00+00:00")
        e2 = awema.licence_ajouter(led, "Agence B", "", "AWEMA-4444-5555-6666", "2026-06-26T11:00:00+00:00")
        self.assertEqual((e1["n"], e2["n"]), (1, 2))
        self.assertEqual(e1["statut"], "delivree")
        self.assertEqual(e1["agence"], "Agence A")
        self.assertEqual(len(e1["cle_hash"]), 64)           # sha256
        self.assertEqual(len(led["licences"]), 2)

    def test_format_cle(self):
        self.assertTrue(awema._licence_valide("AWEMA-18A7-2D12-3336"))
        self.assertFalse(awema._licence_valide("pas-bon"))
        self.assertFalse(awema._licence_valide(""))


if __name__ == "__main__":
    unittest.main()
