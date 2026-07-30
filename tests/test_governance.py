from __future__ import annotations

import base64
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
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

VALID_ONE_PIXEL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
    "+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class GovernanceTests(unittest.TestCase):
    def test_project_relative_paths_are_portable_and_cannot_escape(self) -> None:
        self.assertEqual(
            governance.normalize_project_relative(r"artifacts\ui.png"),
            "artifacts/ui.png",
        )
        self.assertEqual(
            governance.normalize_project_relative("artifacts/../ui.png"),
            "ui.png",
        )
        with self.assertRaisesRegex(ValueError, "project-relative"):
            governance.normalize_project_relative("C:/outside/file.png")
        with self.assertRaisesRegex(ValueError, "escapes project root"):
            governance.normalize_project_relative("../outside.png")

    def test_init_is_additive_and_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("AGENTS.md").write_text("user-owned\n", encoding="utf-8")
            root.joinpath(".gitignore").write_text("build/\n", encoding="utf-8")

            self.assertEqual(governance.initialize(root, "minimal", False), 0)
            self.assertEqual(root.joinpath("AGENTS.md").read_text(encoding="utf-8"), "user-owned\n")
            self.assertTrue(root.joinpath(".agent-governance.json").exists())
            self.assertIn(
                ".agent-evidence/",
                root.joinpath(".gitignore").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "build/",
                root.joinpath(".gitignore").read_text(encoding="utf-8"),
            )

            findings, metrics = governance.audit(root)
            self.assertIn("adapter.stale", {f.code for f in findings})

            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))
            self.assertFalse(governance.generate_adapters(root, config, True, True))
            findings, metrics = governance.audit(root)
            self.assertFalse([f for f in findings if f.severity == "error"])
            self.assertGreater(metrics["authority_count"], 0)

    def test_full_init_adds_current_valid_agent_roles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            self.assertEqual(governance.initialize(root, "full", False), 0)
            config = governance.tomllib.loads(
                root.joinpath(".codex/config.toml").read_text(encoding="utf-8")
            )
            self.assertEqual(
                config["agents"],
                {
                    "max_concurrent_threads_per_session": 4,
                    "interrupt_message": True,
                },
            )

            findings, metrics = governance.audit(root)
            role_errors = [
                finding
                for finding in findings
                if finding.code.startswith("codex.")
            ]
            self.assertEqual(role_errors, [])
            self.assertEqual(metrics["agent_role_count"], 3)
            self.assertEqual(
                metrics["agent_roles"],
                ["architect", "verifier", "worker"],
            )
            self.assertEqual(metrics["agent_model_override_count"], 0)
            self.assertEqual(metrics["agent_reasoning_override_count"], 0)

    def test_audit_rejects_invalid_codex_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "full", False)
            root.joinpath(".codex/agents/worker.toml").write_text(
                (
                    'name = "worker"\n'
                    'description = "Implementation worker."\n'
                ),
                encoding="utf-8",
            )

            findings, metrics = governance.audit(root)

            self.assertIn(
                "codex.role-field",
                {finding.code for finding in findings},
            )
            self.assertEqual(metrics["agent_role_count"], 2)

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

    def test_context_maps_capability_owners_and_rejects_stale_maps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            source = root / "src"
            source.mkdir()
            source.joinpath("draft.py").write_text(
                "def draft():\n    pass\n",
                encoding="utf-8",
            )
            source.joinpath("build.py").write_text(
                "def build():\n    pass\n",
                encoding="utf-8",
            )
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["capabilities"] = [
                {
                    "id": "draft",
                    "purpose": "Author legal draft transitions.",
                    "terms": ["draft"],
                    "paths": ["src/draft.py"],
                    "owners": ["src/draft.py"],
                    "depends_on": ["build"],
                },
                {
                    "id": "build",
                    "purpose": "Resolve immutable build identities.",
                    "terms": ["build identity"],
                    "paths": ["src/build.py"],
                    "owners": ["src/build.py"],
                    "depends_on": [],
                },
            ]
            config["capability_tests"] = [
                {
                    "id": "draft-context",
                    "task": "add a draft choice",
                    "paths": ["src/draft.py"],
                    "expect_capabilities": ["draft", "build"],
                    "expect_owners": [
                        "src/draft.py",
                        "src/build.py",
                    ],
                }
            ]
            config_path.write_text(
                json.dumps(config, indent=2),
                encoding="utf-8",
            )

            details = governance.context_details(
                config,
                "add a draft choice",
                ["src/draft.py"],
            )
            self.assertEqual(
                [item["id"] for item in details["capabilities"]],
                ["draft", "build"],
            )
            self.assertTrue(details["capabilities"][0]["direct"])
            self.assertFalse(details["capabilities"][1]["direct"])
            self.assertEqual(
                details["owners"],
                ["src/draft.py", "src/build.py"],
            )
            findings, metrics = governance.audit(root)
            self.assertFalse(
                [
                    finding
                    for finding in findings
                    if finding.code.startswith("capability")
                ],
                findings,
            )
            self.assertEqual(metrics["capability_count"], 2)
            self.assertFalse(governance.capability_test_findings(config))
            self.assertTrue(governance.coverage_report(config)["complete"])

            config["capabilities"][0]["owners"] = ["src/missing.py"]
            config["capabilities"][0]["depends_on"] = ["missing"]
            config_path.write_text(
                json.dumps(config, indent=2),
                encoding="utf-8",
            )
            findings, _ = governance.audit(root)
            codes = {finding.code for finding in findings}
            self.assertIn("capability.owner-missing", codes)
            self.assertIn("capability.unknown-dependency", codes)

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
            self.assertIn(
                "visual",
                {route["id"] for route in migrated["routes"]},
            )
            self.assertEqual(migrated["visual_validation"]["routes"], ["visual"])
            self.assertEqual(migrated["authorities"], config["authorities"])

    def test_upgrade_from_v3_adds_visual_enforcement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config = json.loads(root.joinpath(".agent-governance.json").read_text(encoding="utf-8"))
            config["version"] = 3
            config.pop("visual_validation")
            config["routes"] = [
                route for route in config["routes"] if route["id"] != "visual"
            ]
            config["route_tests"] = [
                test for test in config["route_tests"] if test["id"] != "visual-route"
            ]
            config["validation"]["profiles"].pop("visual")

            migrated = governance.migrate_config(config)

            self.assertEqual(migrated["version"], governance.CURRENT_VERSION)
            self.assertIn(
                "visual",
                {route["id"] for route in migrated["routes"]},
            )
            self.assertEqual(migrated["visual_validation"]["routes"], ["visual"])
            self.assertTrue(migrated["visual_validation"]["require_surface"])
            self.assertIn(
                "visual-route",
                {test["id"] for test in migrated["route_tests"]},
            )

    def test_malformed_numeric_limits_are_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["limits"]["entrypoint_max_lines"] = "many"
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)

            self.assertIn(
                "limits.entrypoint-max-lines",
                {finding.code for finding in findings},
            )

    def test_mcp_development_interface_requires_safe_activation_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            executable = str(Path(sys.executable))
            config["validation"]["profiles"]["fast"]["commands"] = [
                {
                    "run": f'"{executable}" -c "print(123)"',
                    "proves": (
                        "MCP disabled, enabled, parity, lifecycle, performance, "
                        "and release contracts hold"
                    ),
                }
            ]
            config["development_interfaces"] = [
                {
                    "id": "editor-mcp",
                    "protocol": "mcp",
                    "activation_flag": "--enable-editor-mcp",
                    "default_enabled": False,
                    "production_allowed": False,
                    "guard_profiles": {
                        "disabled": ["fast"],
                        "enabled": ["fast"],
                        "parity": ["fast"],
                        "lifecycle": ["fast"],
                        "performance": ["fast"],
                        "release": ["fast"],
                    },
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

            config["validation"]["profiles"]["fast"]["commands"][0]["proves"] = (
                "The configured MCP check executes"
            )
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            findings, _ = governance.audit(root)
            self.assertIn(
                "development-interface.unproven-category",
                {finding.code for finding in findings},
            )
            config["validation"]["profiles"]["fast"]["commands"][0]["proves"] = (
                "MCP disabled, enabled, parity, lifecycle, performance, and "
                "release contracts hold"
            )
            config["development_interfaces"][0]["activation_flag"] = ""
            config["development_interfaces"][0]["default_enabled"] = True
            config["development_interfaces"][0]["guard_profiles"]["release"] = [
                "missing"
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)
            codes = {finding.code for finding in findings}
            self.assertIn("development-interface.activation-flag", codes)
            self.assertIn("development-interface.default-enabled", codes)
            self.assertIn("development-interface.unknown-profile", codes)

    def test_mcp_development_interface_rejects_empty_proof_profiles(self) -> None:
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
                    "guard_profiles": {
                        "disabled": ["fast"],
                        "enabled": ["fast"],
                        "parity": ["fast"],
                        "lifecycle": ["fast"],
                        "performance": ["fast"],
                        "release": ["fast"],
                    },
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)

            self.assertIn(
                "development-interface.empty-proof",
                {finding.code for finding in findings},
            )

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
            artifact.write_bytes(VALID_ONE_PIXEL_PNG)
            with self.assertRaisesRegex(ValueError, "acceptance surface"):
                governance.verify(
                    root,
                    config,
                    "inspect UI layout",
                    [],
                    "UI is readable",
                    [],
                    False,
                    ["artifacts/ui.png"],
                    ["No clipping at the target viewport"],
                    "pass",
                )
            with self.assertRaisesRegex(ValueError, "concrete inspected property"):
                governance.verify(
                    root,
                    config,
                    "inspect UI layout",
                    [],
                    "UI is readable",
                    [],
                    False,
                    ["artifacts/ui.png"],
                    ["looks good"],
                    "pass",
                    "Rendered application window at 1280x720",
                )
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
                "Rendered application window at 1280x720",
            )

            self.assertEqual(status, 0)
            self.assertIsNotNone(receipt)
            self.assertEqual(payload["visual_evidence"]["verdict"], "pass")
            self.assertEqual(
                payload["visual_evidence"]["artifacts"][0]["path"],
                "artifacts/ui.png",
            )
            self.assertEqual(
                payload["visual_evidence"]["artifacts"][0]["width"],
                1,
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

    def test_visual_evidence_rejects_invalid_and_stale_images(self) -> None:
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
            artifact = root / "artifacts" / "ui.png"
            artifact.parent.mkdir()
            artifact.write_bytes(b"\x89PNG\r\n\x1a\nrendered-test")

            with self.assertRaisesRegex(ValueError, "not a valid png"):
                governance.verify(
                    root,
                    config,
                    "inspect UI layout",
                    [],
                    "UI is readable",
                    [],
                    False,
                    ["artifacts/ui.png"],
                    ["No clipping at the target viewport"],
                    "pass",
                    "Rendered application window",
                )

            artifact.write_bytes(VALID_ONE_PIXEL_PNG)
            stale = time.time() - 7200
            os.utime(artifact, (stale, stale))
            with self.assertRaisesRegex(ValueError, "stale"):
                governance.verify(
                    root,
                    config,
                    "inspect UI layout",
                    [],
                    "UI is readable",
                    [],
                    False,
                    ["artifacts/ui.png"],
                    ["No clipping at the target viewport"],
                    "pass",
                    "Rendered application window",
                )

    def test_visual_evidence_rejects_signature_only_video_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_mp4 = root / "fake.mp4"
            fake_mp4.write_bytes(b"\x00\x00\x00\x0cftypisom")
            fake_webm = root / "fake.webm"
            fake_webm.write_bytes(b"\x1a\x45\xdf\xa3not-a-rendered-video")

            with self.assertRaisesRegex(ValueError, "not a valid mp4"):
                governance.inspect_visual_artifact(fake_mp4)
            with self.assertRaisesRegex(ValueError, "not a valid webm"):
                governance.inspect_visual_artifact(fake_webm)

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
            codes = {finding.code for finding in findings}
            self.assertIn("rule.source-authority", codes)
            self.assertIn("rule.empty-guard", codes)

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
            self.assertEqual(
                receipt_payload["schema"],
                "project-agent-toolkit.evidence.v2",
            )
            self.assertEqual(receipt_payload["claim"], "verification works")
            self.assertEqual(receipt_payload["results"][0]["exit_code"], 0)

    def test_git_worktree_digest_changes_with_dirty_file_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "agent@example.invalid"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Agent Test"],
                cwd=root,
                check=True,
            )
            tracked = root / "tracked.txt"
            tracked.write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "--quiet", "-m", "base"],
                cwd=root,
                check=True,
            )

            tracked.write_text("first dirty value\n", encoding="utf-8")
            first = governance.git_state(root)
            tracked.write_text("second dirty value\n", encoding="utf-8")
            second = governance.git_state(root)

            self.assertEqual(first["status_sha256"], second["status_sha256"])
            self.assertNotEqual(first["worktree_sha256"], second["worktree_sha256"])

    def test_verify_fails_if_guard_mutates_project_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            mutable = root / "mutable.txt"
            mutable.write_text("before\n", encoding="utf-8")
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            executable = str(Path(sys.executable))
            config["validation"]["profiles"]["fast"]["commands"] = [
                {
                    "run": (
                        f'"{executable}" -c "from pathlib import Path; '
                        "Path('mutable.txt').write_text('after', encoding='utf-8')\""
                    ),
                    "proves": "Mutation detection is exercised",
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            status, payload, receipt = governance.verify(
                root,
                config,
                "summarize",
                [],
                "Guard execution preserves the tested source state",
                [],
                True,
            )

            self.assertEqual(status, 1)
            self.assertFalse(payload["state_stable"])
            self.assertFalse(payload["passed"])
            self.assertIsNotNone(receipt)

    def test_receipt_requires_git_ignored_evidence_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            governance.initialize(root, "minimal", False)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            config_path = root / ".agent-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["evidence"]["directory"] = "receipts"
            executable = str(Path(sys.executable))
            config["validation"]["profiles"]["fast"]["commands"] = [
                {
                    "run": f'"{executable}" -c "print(123)"',
                    "proves": "The configured command executes",
                }
            ]
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

            findings, _ = governance.audit(root)
            evidence_findings = [
                finding
                for finding in findings
                if finding.code == "evidence.not-ignored"
            ]
            self.assertEqual(len(evidence_findings), 1)
            self.assertEqual(evidence_findings[0].severity, "error")
            with self.assertRaisesRegex(ValueError, "must be ignored by Git"):
                governance.verify(
                    root,
                    config,
                    "summarize",
                    [],
                    "Receipt does not mutate the validated source state",
                    [],
                    True,
                )


if __name__ == "__main__":
    unittest.main()
