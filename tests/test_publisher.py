"""Invariant : le moteur de publication sélectionne les posts dus, reste idempotent,
et calcule correctement les transitions de statut (ADR-010). Aucun appel réseau."""
import os
import sys
import unittest
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import publisher  # noqa: E402

REF = datetime(2026, 7, 2, 18, 0, 0, tzinfo=timezone.utc)


def post(**kw):
    base = {"reseaux": ["facebook"], "publier_le": "2026-07-02T17:00:00Z", "statut": "programme",
            "contenu": {"texte": "bonjour"}, "resultats": {}}
    base.update(kw)
    return base


class TestEstDu(unittest.TestCase):
    def test_du_quand_heure_passee_et_programme(self):
        self.assertTrue(publisher.est_du(post(), REF))

    def test_pas_du_si_futur(self):
        self.assertFalse(publisher.est_du(post(publier_le="2026-07-02T19:00:00Z"), REF))

    def test_pas_du_si_deja_publie(self):
        self.assertFalse(publisher.est_du(post(statut="publie"), REF))

    def test_pas_du_si_brouillon(self):
        self.assertFalse(publisher.est_du(post(statut="brouillon"), REF))

    def test_partiel_est_repris(self):
        self.assertTrue(publisher.est_du(post(statut="partiel"), REF))

    def test_date_invalide_pas_du(self):
        self.assertFalse(publisher.est_du(post(publier_le="n'importe quoi"), REF))


class TestPublierItem(unittest.TestCase):
    def faux_publish(self, mapping):
        return lambda reseau, item, med: mapping.get(reseau, {"ok": False, "error": "x"})

    def test_tous_ok_donne_publie(self):
        it = post(reseaux=["facebook", "linkedin"])
        it = publisher.publier_item(it, REF, publish=self.faux_publish(
            {"facebook": {"ok": True, "url": "f"}, "linkedin": {"ok": True, "url": "l"}}))
        self.assertEqual(it["statut"], "publie")
        self.assertTrue(it["resultats"]["facebook"]["ok"])

    def test_un_seul_ok_donne_partiel(self):
        it = post(reseaux=["facebook", "linkedin"])
        it = publisher.publier_item(it, REF, publish=self.faux_publish(
            {"facebook": {"ok": True}, "linkedin": {"ok": False, "error": "scope"}}))
        self.assertEqual(it["statut"], "partiel")

    def test_idempotent_ne_republie_pas(self):
        # facebook déjà ok : le connecteur ne doit PAS être rappelé pour lui.
        appels = []

        def pub(reseau, item, med):
            appels.append(reseau)
            return {"ok": True}
        it = post(reseaux=["facebook", "linkedin"], resultats={"facebook": {"ok": True, "url": "f"}})
        publisher.publier_item(it, REF, publish=pub)
        self.assertEqual(appels, ["linkedin"])  # facebook sauté

    def test_echec_apres_max_tentatives(self):
        it = post(reseaux=["facebook"], tentatives=publisher.MAX_TENTATIVES - 1)
        it = publisher.publier_item(it, REF, publish=self.faux_publish({"facebook": {"ok": False, "error": "x"}}))
        self.assertEqual(it["statut"], "echec")

    def test_echec_temporaire_reste_programme(self):
        it = post(reseaux=["facebook"], tentatives=0)
        it = publisher.publier_item(it, REF, publish=self.faux_publish({"facebook": {"ok": False, "error": "x"}}))
        self.assertEqual(it["statut"], "programme")
        self.assertEqual(it["tentatives"], 1)

    def test_dry_run_marque_ok_sans_appel(self):
        appels = []
        it = post(reseaux=["facebook", "tiktok"])
        publisher.publier_item(it, REF, publish=lambda *a: appels.append(a) or {"ok": False}, dry=True)
        self.assertEqual(appels, [])
        self.assertEqual(it["statut"], "publie")

    def test_video_differee_ne_passe_pas_en_echec(self):
        it = post(reseaux=["youtube"], tentatives=publisher.MAX_TENTATIVES)
        it = publisher.publier_item(it, REF, publish=self.faux_publish(
            {"youtube": {"ok": False, "differe": True, "error": "à venir"}}))
        self.assertEqual(it["statut"], "programme")  # différé ≠ échec définitif


if __name__ == "__main__":
    unittest.main()
