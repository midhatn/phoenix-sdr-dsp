"""Host-only static checks for release-maintenance materials."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "validate_clean_clone.ps1"
ACTIVATE_SCRIPT = REPO / "scripts" / "activate_ironenv.ps1"
RUNNER = REPO / "run_all_silicon_tests.py"
ARCHIVED_MARKDOWN_ROOTS = (REPO / "docs" / "history", REPO / "third_party")
EXPECTED_RUNNER_SHA256 = (
    "742591321ac5dc3069a51ded4e198905367f8dc6261df8c3ebae20b5e333fbad"
)


class ReleaseMaterialsContractTests(unittest.TestCase):
    def test_clean_clone_script_keeps_default_path_host_safe(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8-sig")
        self.assertEqual(source.count("{"), source.count("}"))
        self.assertIn("[switch]$RunSilicon", source)
        self.assertIn("[switch]$InstallHostDependencies", source)
        self.assertIn("if ($RunSilicon)", source)
        self.assertIn("accesses the NPU", source)
        self.assertIn("numpy==$requiredNumpyVersion", source)
        self.assertIn('"2.5.2"', source)
        self.assertIn("Re-run with -InstallHostDependencies", source)
        self.assertIn("Compile maintained Python", source)
        self.assertIn("Run host-only contracts", source)
        self.assertIn(EXPECTED_RUNNER_SHA256, source)

    def test_canonical_runner_identity_is_unchanged(self) -> None:
        import hashlib

        self.assertEqual(
            hashlib.sha256(RUNNER.read_bytes()).hexdigest(),
            EXPECTED_RUNNER_SHA256,
        )

    def test_ironenv_activation_is_checkout_local_and_documented(self) -> None:
        source = ACTIVATE_SCRIPT.read_text(encoding="utf-8-sig")
        self.assertIn("$PSScriptRoot", source)
        self.assertIn("PEANO_INSTALL_DIR", source)
        self.assertIn(r"third_party\mlir-aie\ironenv\Scripts\Activate.ps1", source)
        self.assertNotIn(r"C:\phoenix-sdr-dsp", source)
        self.assertNotIn(r"C:\Xilinx\XRT", source)

        for path in (REPO / "README.md", REPO / "docs" / "SETUP_WINDOWS.md"):
            with self.subTest(path=path.relative_to(REPO)):
                text = path.read_text(encoding="utf-8-sig")
                self.assertIn(r".\scripts\activate_ironenv.ps1", text)

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
        self.assertIn("-InstallHostDependencies", checklist)
        self.assertIn("-RunSilicon", checklist)

    def test_maintained_markdown_uses_supported_math_notation(self) -> None:
        offending = []
        for path in REPO.rglob("*.md"):
            if any(root in path.parents for root in ARCHIVED_MARKDOWN_ROOTS):
                continue
            if "\\operatorname" in path.read_text(encoding="utf-8"):
                offending.append(path.relative_to(REPO).as_posix())
        self.assertEqual(offending, [])

    def test_current_setup_materials_prefer_the_extensionless_launcher(self) -> None:
        current_guidance = [
            REPO / "README.md",
            REPO / "CONTRIBUTING.md",
            REPO / "docs" / "README.md",
            REPO / "docs" / "SETUP_WINDOWS.md",
            REPO / "docs" / "PQC_COMPLETE_V1.md",
            REPO / "requirements" / "toolchain-versions.md",
        ]
        for path in current_guidance:
            with self.subTest(path=path.relative_to(REPO)):
                text = path.read_text(encoding="utf-8")
                self.assertIn(r"py .\install", text)
                self.assertNotIn(r"py .\install.py", text)

        workflow = (REPO / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python install --self-test", workflow)
        self.assertNotIn("python install.py --self-test", workflow)


if __name__ == "__main__":
    unittest.main()
