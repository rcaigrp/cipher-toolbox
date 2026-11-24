import json
import unittest
from unittest.mock import patch

from preflight import preflight


class TestPreflight(unittest.TestCase):
    def test_clear_prompt(self):
        result = preflight("Hello world", "approved-example", {"approved-example"})
        self.assertEqual(result["decision"], "clear")
        self.assertEqual(result["findings"], [])

    def test_blocked_provider(self):
        result = preflight("Hello world", "blocked-example", {"approved-example"})
        self.assertEqual(result["decision"], "review")
        self.assertIn("provider_not_allowed", result["findings"])

    def test_secret_in_prompt(self):
        result = preflight(
            "My password is secret123",
            "approved-example",
            {"approved-example"}
        )
        self.assertEqual(result["decision"], "review")
        self.assertIn("possible_secret_assignment", result["findings"])

    def test_restricted_data_label(self):
        result = preflight(
            "Classification: restricted\nHello world",
            "approved-example",
            {"approved-example"}
        )
        self.assertEqual(result["decision"], "review")
        self.assertIn("restricted_data_label", result["findings"])

    @patch("preflight.semantic_review")
    def test_semantic_review(self, mock_semantic):
        mock_semantic.return_value = "review"
        result = preflight(
            "Hello world",
            "approved-example",
            {"approved-example"}
        )
        self.assertEqual(result["decision"], "review")
        self.assertIn("model_flagged_sensitive_context", result["findings"])

    @patch("preflight.semantic_review")
    def test_semantic_unavailable(self, mock_semantic):
        mock_semantic.return_value = "unavailable"
        result = preflight(
            "Hello world",
            "approved-example",
            {"approved-example"}
        )
        self.assertEqual(result["decision"], "clear")
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main()