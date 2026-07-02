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

    def test_partiel_passe_en_echec_apres_max_tentatives(self):
        # Régression (audit) : un post partiel (1 réseau ok, 1 en échec réel) était re-tenté
        # indéfiniment car MAX_TENTATIVES ne s'appliquait qu'à la branche « zéro succès ».
        it = post(reseaux=["facebook", "linkedin"], tentatives=publisher.MAX_TENTATIVES - 1,
                  resultats={"facebook": {"ok": True, "url": "f"}})
        it = publisher.publier_item(it, REF, publish=self.faux_publish(
            {"linkedin": {"ok": False, "error": "scope"}}))
        self.assertEqual(it["statut"], "echec")
        self.assertTrue(it["resultats"]["facebook"]["ok"])  # le succès facebook n'est pas perdu
        self.assertFalse(publisher.est_du(it, REF))  # ne sera plus re-sélectionné

    def test_video_differee_va_en_attente_sans_boucle(self):
        # Un post 100 % vidéo différée sort de la file (attente_video) au lieu de boucler tous les crons.
        it = post(reseaux=["youtube"], tentatives=publisher.MAX_TENTATIVES)
        it = publisher.publier_item(it, REF, publish=self.faux_publish(
            {"youtube": {"ok": False, "differe": True, "error": "à venir"}}))
        self.assertEqual(it["statut"], "attente_video")
        self.assertFalse(publisher.est_du(it, REF))  # plus de re-tentative en boucle

    def test_erreur_reseau_brute_ne_crashe_pas(self):
        # Régression (audit) : http() renvoie {"error": "<chaîne>"} sur timeout → les connecteurs
        # faisaient .get("message") sur une chaîne (AttributeError) et avortaient tout le run.
        self.assertEqual(publisher.msg_erreur({"error": "timeout"}), "timeout")
        self.assertEqual(publisher.msg_erreur({"error": {"message": "scope manquant"}}), "scope manquant")
        self.assertIsInstance(publisher.msg_erreur({}), str)

    def test_exception_connecteur_isolee_par_reseau(self):
        # Un réseau qui lève une exception ne doit pas faire perdre le réseau déjà publié du même item.
        def pub(reseau, item, med):
            if reseau == "linkedin":
                raise RuntimeError("boom")
            return {"ok": True, "url": "f"}
        it = post(reseaux=["facebook", "linkedin"])
        it = publisher.publier_item(it, REF, publish=pub)
        self.assertTrue(it["resultats"]["facebook"]["ok"])
        self.assertFalse(it["resultats"]["linkedin"]["ok"])
        self.assertIn("boom", it["resultats"]["linkedin"]["error"])


class TestMediasUrls(unittest.TestCase):
    def test_extrait_les_urls_presentes(self):
        item = {"media": [{"type": "image", "url": "u1"}, {"type": "video"}, {"url": "u2"}]}
        self.assertEqual(publisher.medias_urls(item), ["u1", "u2"])

    def test_sans_media_donne_liste_vide(self):
        self.assertEqual(publisher.medias_urls({}), [])


if __name__ == "__main__":
    unittest.main()
