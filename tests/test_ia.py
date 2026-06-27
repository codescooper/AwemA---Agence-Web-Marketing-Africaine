"""Invariant : sélection de fournisseur IA agnostique + résolution du modèle (sans réseau)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import awema_ai  # noqa: E402

AI_VARS = ["AWEMA_AI_PROVIDER", "AWEMA_AI_MODEL", "GROQ_API_KEY", "GEMINI_API_KEY",
           "OPENROUTER_API_KEY", "CEREBRAS_API_KEY", "MISTRAL_API_KEY", "GITHUB_MODELS_TOKEN",
           "TOGETHER_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]


class TestIA(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in AI_VARS}
        for k in AI_VARS:
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_selection_explicite(self):
        os.environ["AWEMA_AI_PROVIDER"] = "anthropic"
        os.environ["ANTHROPIC_API_KEY"] = "x"
        pid, cfg = awema_ai.actif()
        self.assertEqual(pid, "anthropic")
        self.assertEqual(cfg["type"], "anthropic")

    def test_auto_detection(self):
        os.environ["GROQ_API_KEY"] = "x"     # Groq est en tête du registre → auto-détecté
        self.assertEqual(awema_ai.actif()[0], "groq")
        self.assertTrue(awema_ai.disponible())

    def test_resolution_modele(self):
        # Anthropic : on garde le modèle claude tuné par l'agent
        os.environ["AWEMA_AI_PROVIDER"] = "anthropic"
        os.environ["ANTHROPIC_API_KEY"] = "x"
        self.assertEqual(awema_ai.modele_actif("claude-opus-4-8"), "claude-opus-4-8")
        # Fournisseur non-Claude : le hint claude est ignoré → modèle par défaut du fournisseur
        os.environ["AWEMA_AI_PROVIDER"] = "groq"
        os.environ["GROQ_API_KEY"] = "x"
        self.assertEqual(awema_ai.modele_actif("claude-opus-4-8"), "llama-3.3-70b-versatile")
        # Surcharge globale
        os.environ["AWEMA_AI_MODEL"] = "mon-modele"
        self.assertEqual(awema_ai.modele_actif("claude-opus-4-8"), "mon-modele")

    def test_override_modele_anthropic(self):
        os.environ["AWEMA_AI_PROVIDER"] = "anthropic"
        os.environ["ANTHROPIC_API_KEY"] = "x"
        os.environ["AWEMA_AI_MODEL"] = "claude-sonnet-4-6"
        # hint non-claude (ex. d'un agent mal configuré) → on retombe sur la surcharge globale
        self.assertEqual(awema_ai.modele_actif("gpt-4o"), "claude-sonnet-4-6")


if __name__ == "__main__":
    unittest.main()
