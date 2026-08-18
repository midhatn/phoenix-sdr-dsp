"""Host-only static checks for release-maintenance materials."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "validate_clean_clone.ps1"
RUNNER = REPO / "run_all_silicon_tests.py"
EXPECTED_RUNNER_SHA256 = (
    "742591321ac5dc3069a51ded4e198905367f8dc6261df8c3ebae20b5e333fbad"
)


class ReleaseMaterialsContractTests(unittest.TestCase):
    def test_clean_clone_script_keeps_default_path_host_safe(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8-sig")
        self.assertEqual(source.count("{"), source.count("}"))
        self.assertIn("[switch]$RunSilicon", source)
        self.assertIn("if ($RunSilicon)", source)
        self.assertIn("accesses the NPU", source)
        self.assertIn("Compile maintained Python", source)
        self.assertIn("Run host-only contracts", source)
        self.assertIn(EXPECTED_RUNNER_SHA256, source)

    def test_canonical_runner_identity_is_unchanged(self) -> None:
        import hashlib

        self.assertEqual(
            hashlib.sha256(RUNNER.read_bytes()).hexdigest(),
            EXPECTED_RUNNER_SHA256,
        )

    def test_publication_documents_link_to_release_controls(self) -> None:
        readiness = (REPO / "docs" / "PUBLICATION_READINESS.md").read_text(
            encoding="utf-8"
        )
        checklist = (REPO / "docs" / "JOURNAL_REPRODUCIBILITY_CHECKLIST.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("34/34 mixed-backend", readiness)
        self.assertIn("29 direct-hardware", readiness)
        self.assertIn("four host/NPU", readiness)
        self.assertIn(EXPECTED_RUNNER_SHA256, checklist)
        self.assertIn("-RunSilicon", checklist)


if __name__ == "__main__":
    unittest.main()
