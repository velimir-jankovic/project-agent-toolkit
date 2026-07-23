from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "project-agent-toolkit"
    / "scripts"
    / "governance.py"
)
SPEC = importlib.util.spec_from_file_location("governance", SCRIPT)
assert SPEC and SPEC.loader
governance = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = governance
SPEC.loader.exec_module(governance)


class GovernanceTests(unittest.TestCase):
    def test_init_is_additive_and_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("AGENTS.md").write_text("user-owned\n", encoding="utf-8")

            self.assertEqual(governance.initialize(root, "minimal", False), 0)
            self.assertEqual(root.joinpath("AGENTS.md").read_text(encoding="utf-8"), "user-owned\n")
            self.assertTrue(root.joinpath(".agent-governance.json").exists())

            findings, metrics = governance.audit(root)
            self.assertIn("adapter.stale", {f.code for f in findings})

            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))
            self.assertFalse(governance.generate_adapters(root, config, True, True))
            findings, metrics = governance.audit(root)
            self.assertFalse([f for f in findings if f.severity == "error"])
            self.assertGreater(metrics["authority_count"], 0)

    def test_broken_authority_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["authorities"][0]["path"] = "docs/MISSING.md"
            config_path.write_text(json.dumps(config), encoding="utf-8")

            findings, _ = governance.audit(root)
            self.assertIn("document.missing", {finding.code for finding in findings})

    def test_route_uses_terms_then_falls_back(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)

            documents, routes = governance.route_documents(root, "change public API design", [])
            self.assertIn("architecture", routes)
            self.assertIn("docs/ARCHITECTURE.md", documents)

            documents, routes = governance.route_documents(root, "answer a question", [])
            self.assertEqual(routes, ["default"])
            self.assertEqual(documents, ["RULES.md", "docs/WORKFLOW.md"])

            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))
            details = governance.route_details(config, "build service", [])
            self.assertIn("implementation", details["routes"])
            self.assertNotIn("visual", details["routes"])

    def test_tooling_pollution_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            runtime = root / ".codex" / "cache" / "state.db"
            runtime.parent.mkdir(parents=True)
            runtime.write_bytes(b"runtime")

            findings, _ = governance.audit(root)
            self.assertIn("tooling.pollution", {finding.code for finding in findings})

    def test_cpp_lambda_is_not_treated_as_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            architecture = root / "docs" / "ARCHITECTURE.md"
            architecture.write_text(
                "callback([](const Value& value) { return value.ok(); });\n",
                encoding="utf-8",
            )

            findings, _ = governance.audit(root)
            self.assertNotIn("link.missing", {finding.code for finding in findings})

    def test_route_contract_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["route_tests"][0]["expect_routes"] = ["default"]

            findings = governance.route_test_findings(config)
            self.assertIn("route-test.failed", {finding.code for finding in findings})

    def test_upgrade_preserves_existing_policy_and_adds_current_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))
            config["version"] = 1
            config.pop("project")
            config.pop("adapters")
            config.pop("route_tests")
            config.pop("rules")
            config.pop("evidence")
            for route in config["routes"]:
                route.pop("validation")
            config["validation"] = {"commands": ["python -V"]}

            migrated = governance.migrate_config(config)
            self.assertEqual(migrated["version"], governance.CURRENT_VERSION)
            self.assertEqual(migrated["authorities"], config["authorities"])
            self.assertIn("adapters", migrated)
            self.assertEqual(migrated["development_interfaces"], [])
            self.assertEqual(len(migrated["route_tests"]), len(config["routes"]))
            self.assertFalse(governance.route_test_findings(migrated))
            self.assertEqual(
                migrated["validation"]["profiles"]["fast"]["commands"][0]["run"],
                "python -V",
            )

    def test_upgrade_from_v2_adds_development_interfaces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))
            config["version"] = 2
            config.pop("development_interfaces")

            migrated = governance.migrate_config(config)

            self.assertEqual(migrated["version"], governance.CURRENT_VERSION)
            self.assertEqual(migrated["development_interfaces"], [])
            self.assertEqual(migrated["authorities"], config["authorities"])

    def test_mcp_development_interface_requires_safe_activation_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["development_interfaces"] = [
                {
                    "id": "editor-mcp",
                    "protocol": "mcp",
                    "activation_flag": "--enable-editor-mcp",
                    "default_enabled": False,
                    "production_allowed": False,
                    "guard_profiles": ["fast"],
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, metrics = governance.audit(root)
            self.assertFalse(
                [
                    finding
                    for finding in findings
                    if finding.code.startswith("development-interface.")
                ],
                findings,
            )
            self.assertEqual(metrics["development_interface_count"], 1)

            config["development_interfaces"][0]["activation_flag"] = ""
            config["development_interfaces"][0]["default_enabled"] = True
            config["development_interfaces"][0]["guard_profiles"] = ["missing"]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)
            codes = {finding.code for finding in findings}
            self.assertIn("development-interface.activation-flag", codes)
            self.assertIn("development-interface.default-enabled", codes)
            self.assertIn("development-interface.unknown-profile", codes)

    def test_visual_route_requires_rendered_and_reviewed_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            executable = str(Path(sys.executable))
            config["validation"]["profiles"]["fast"]["commands"] = [
                {
                    "run": f'"{executable}" -c "print(123)"',
                    "proves": "The configured command executes",
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "rendered artifact"):
                governance.verify(
                    root,
                    config,
                    "inspect UI layout",
                    [],
                    "UI is readable",
                    [],
                    False,
                )

            artifact = root / "artifacts" / "ui.png"
            artifact.parent.mkdir()
            artifact.write_bytes(b"\x89PNG\r\n\x1a\nrendered-test")
            status, payload, receipt = governance.verify(
                root,
                config,
                "inspect UI layout",
                [],
                "UI is readable",
                [],
                True,
                ["artifacts/ui.png"],
                ["No clipping at the target viewport"],
                "pass",
            )

            self.assertEqual(status, 0)
            self.assertIsNotNone(receipt)
            self.assertEqual(payload["visual_evidence"]["verdict"], "pass")
            self.assertEqual(
                payload["visual_evidence"]["artifacts"][0]["path"],
                "artifacts/ui.png",
            )

    def test_visual_policy_cannot_disable_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["visual_validation"]["require_review"] = False
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)
            self.assertIn(
                "visual-validation.review",
                {finding.code for finding in findings},
            )

    def test_invalid_adapter_shape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["adapters"]["outputs"].append(
                {"kind": "unknown", "path": ""}
            )
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)
            codes = {finding.code for finding in findings}
            self.assertIn("adapter.kind", codes)
            self.assertIn("adapter.path", codes)

    def test_rule_source_must_belong_to_declared_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["rules"] = [
                {
                    "id": "wrong-owner",
                    "authority": "rules",
                    "source": "docs/WORKFLOW.md#wrong-owner",
                    "guard": "fast",
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)
            self.assertIn(
                "rule.source-authority",
                {finding.code for finding in findings},
            )

    def test_coverage_reports_complete_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))

            report = governance.coverage_report(config)
            self.assertTrue(report["complete"], report)

    def test_verify_writes_revision_bound_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            executable = str(Path(sys.executable))
            config["validation"]["profiles"]["fast"]["commands"] = [
                {
                    "run": f'"{executable}" -c "print(123)"',
                    "proves": "The configured command executes",
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            status, payload, receipt = governance.verify(
                root,
                config,
                "summarize",
                [],
                "verification works",
                [],
                True,
            )
            self.assertEqual(status, 0)
            self.assertTrue(payload["passed"])
            self.assertIsNotNone(receipt)
            receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(receipt_payload["claim"], "verification works")
            self.assertEqual(receipt_payload["results"][0]["exit_code"], 0)


if __name__ == "__main__":
    unittest.main()
