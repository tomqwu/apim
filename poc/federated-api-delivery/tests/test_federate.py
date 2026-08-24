#!/usr/bin/env python3
"""Positive and fail-closed tests for the federated delivery reference."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "federate.py"
SPEC = importlib.util.spec_from_file_location("federate_reference", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load federate.py")
FEDERATE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FEDERATE
SPEC.loader.exec_module(FEDERATE)

SYNTHETIC_COMMIT = "0123456789abcdef0123456789abcdef01234567"


class FederatedDeliveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inputs = FEDERATE.load_inputs(ROOT)
        self.current = FEDERATE.read_json(ROOT / "fixtures" / "current-empty.json")

    def build(self):
        return FEDERATE.build_documents(self.inputs, self.current, SYNTHETIC_COMMIT)

    def approved_review(self, plan):
        return {
            "status": "approved",
            "plan_sha256": FEDERATE.digest(plan),
            "target_control_plane": self.inputs["target"]["control_plane_id"],
            "review_id": "review:synthetic-test-only",
            "reviewer_role": "independent-test-reviewer",
            "reviewed_at": "2026-08-24T00:00:00Z",
        }

    def test_reference_composes_deterministically(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(
            [FEDERATE.canonical_bytes(item) for item in first],
            [FEDERATE.canonical_bytes(item) for item in second],
        )
        config, provenance, plan, pending = first
        self.assertEqual(plan["summary"], {"create": 6, "change": 0, "delete": 0, "unchanged": 0})
        self.assertEqual(len(provenance["entities"]), 6)
        self.assertEqual(pending["plan_review"]["status"], "pending")
        self.assertFalse(pending["converged"])
        self.assertEqual(len(config["plugins"]), 4)

    def test_missing_owner_is_rejected(self) -> None:
        self.inputs["metadata"]["owner_id"] = ""
        with self.assertRaisesRegex(FEDERATE.ValidationError, "owner_id"):
            FEDERATE.validate_inputs(self.inputs)

    def test_unsafe_route_is_rejected(self) -> None:
        self.inputs["intent"]["route"]["hosts"] = ["*.example.test"]
        with self.assertRaisesRegex(FEDERATE.ValidationError, "unsafe route"):
            FEDERATE.validate_inputs(self.inputs)

    def test_prohibited_plugin_is_rejected(self) -> None:
        self.inputs["intent"]["plugins"].append({"name": "pre-function", "config": {}})
        with self.assertRaisesRegex(FEDERATE.ValidationError, "prohibited application plugin"):
            FEDERATE.validate_inputs(self.inputs)

    def test_mandatory_plugin_override_is_rejected(self) -> None:
        self.inputs["intent"]["plugins"].append({"name": "openid-connect", "config": {}})
        with self.assertRaisesRegex(FEDERATE.ValidationError, "reserved mandatory plugin"):
            FEDERATE.validate_inputs(self.inputs)

    def test_conflicting_writer_is_rejected(self) -> None:
        self.inputs["writers"]["entities"][0]["writer_id"] = "app:another-team"
        with self.assertRaisesRegex(FEDERATE.ValidationError, "conflicting writers"):
            FEDERATE.validate_inputs(self.inputs)

    def test_conflicting_active_writer_is_rejected_before_plan(self) -> None:
        config, _, _, _ = self.build()
        current = copy.deepcopy(config)
        current["services"][0]["tags"] = [
            tag if not tag.startswith("writer=") else "writer=app:another-team"
            for tag in current["services"][0]["tags"]
        ]
        with self.assertRaisesRegex(FEDERATE.ValidationError, "conflicting writers"):
            FEDERATE.build_plan(
                current,
                config,
                self.inputs["intent"]["api_id"],
                self.inputs["target"]["control_plane_id"],
            )

    def test_expired_exception_is_rejected(self) -> None:
        self.inputs["metadata"]["exception_ids"] = ["EXC-001"]
        self.inputs["exceptions"]["exceptions"] = [
            {
                "id": "EXC-001",
                "control_id": "ROUTE-NONSTANDARD",
                "status": "approved",
                "scope": {"api_id": "orders-v1"},
                "owner_id": "team:orders-api",
                "removal_owner_id": "team:orders-api",
                "reviewed_by_role": "security-governance",
                "audit_ref": "review:synthetic-expired",
                "compensating_controls": ["outside-in route monitor"],
                "expires_at": "2026-08-23",
            }
        ]
        with self.assertRaisesRegex(FEDERATE.ValidationError, "expired exception"):
            FEDERATE.validate_inputs(self.inputs)

    def test_unapproved_plan_cannot_be_attested(self) -> None:
        config, _, plan, pending = self.build()
        review = self.approved_review(plan)
        review["status"] = "pending"
        with self.assertRaisesRegex(FEDERATE.ValidationError, "not approved"):
            FEDERATE.attest_release(config, plan, pending, review, config)

    def test_active_drift_is_rejected(self) -> None:
        config, _, plan, pending = self.build()
        active = copy.deepcopy(config)
        active["services"][0]["url"] = "https://changed.backend.example.test"
        with self.assertRaisesRegex(FEDERATE.ValidationError, "configuration drift detected"):
            FEDERATE.attest_release(config, plan, pending, self.approved_review(plan), active)

    def test_approved_converged_snapshot_is_attested(self) -> None:
        config, _, plan, pending = self.build()
        result = FEDERATE.attest_release(config, plan, pending, self.approved_review(plan), config)
        self.assertTrue(result["converged"])
        self.assertEqual(result["application_commit"], SYNTHETIC_COMMIT)
        self.assertEqual(result["generated_config_sha256"], result["active_config_sha256"])
        self.assertEqual(result["target_control_plane"], "cp-synthetic-development")


if __name__ == "__main__":
    unittest.main()
