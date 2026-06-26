"""Invariant : la consolidation somme correctement les réseaux et calcule l'engagement."""
import unittest

from tests.util import charger

cr = charger("scripts/connect-reseaux.py", "cr")


class TestConsolidation(unittest.TestCase):
    def test_sommes_multi_reseaux(self):
        data = cr._vide()
        data["par_reseau"]["facebook"].update({"abonnes": 100, "posts": 10, "likes": 30, "commentaires": 5})
        data["par_reseau"]["tiktok"].update({"abonnes": 400, "posts": 20, "likes": 200})
        cr._consolider(data)
        g = data["global"]
        self.assertEqual(g["audience"], 500)
        self.assertEqual(g["posts"], 30)
        self.assertEqual(g["likes"], 230)
        self.assertEqual(g["commentaires"], 5)

    def test_engagement_par_abonne(self):
        data = cr._vide()
        # 10 posts, 100 abonnés, (likes+comm+partages) = 50 → (50/10)/100*100 = 5.0 %
        data["par_reseau"]["facebook"].update(
            {"abonnes": 100, "posts": 10, "likes": 40, "commentaires": 8, "partages": 2})
        cr._consolider(data)
        self.assertEqual(data["global"]["engagement_taux"], 5.0)

    def test_connecte_si_un_reseau_a_des_abonnes(self):
        data = cr._vide()
        self.assertFalse(data.get("connecte") or False)
        data["par_reseau"]["youtube"]["abonnes"] = 12
        cr._consolider(data)
        self.assertTrue(data["connecte"])


if __name__ == "__main__":
    unittest.main()
