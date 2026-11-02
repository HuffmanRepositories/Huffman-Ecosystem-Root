"""Synthetic P12-P15 seam harness. No network, credentials, or real provider effects."""
from __future__ import annotations

import threading
import unittest


class SyntheticSeam:
    """Tiny in-memory composition model; NOT a production implementation."""

    def __init__(self, budget=10):
        self.parent_active = True
        self.child_active = True
        self.parent_grant = {"tenant": "t1", "actions": {"tool:write"}, "budget": budget}
        self.child_grant = {"tenant": "t1", "actions": {"tool:write"}, "budget": budget}
        self.budget_total = budget
        self.reserved = 0
        self.spent = 0
        self.requests = {}
        self.effects = []
        self.audit = []
        self.lock = threading.RLock()
        self.provider_cancel_requested = False

    def authorize(self, tenant, action):
        return (self.parent_active and self.child_active
                and self.parent_grant["tenant"] == tenant
                and self.child_grant["tenant"] == tenant
                and action in self.parent_grant["actions"]
                and action in self.child_grant["actions"])

    def reserve(self, request_id, amount):
        with self.lock:
            if request_id in self.requests:
                return self.requests[request_id]["reservation"]
            if amount < 0 or self.spent + self.reserved + amount > self.budget_total:
                raise ValueError("budget denied")
            self.reserved += amount
            self.requests[request_id] = {
                "reservation": amount, "status": "reserved", "effect": None
            }
            self.audit.append(("budget_reserved", request_id, amount))
            return amount

    def dispatch(self, request_id, tenant="t1", action="tool:write"):
        with self.lock:
            if not self.authorize(tenant, action):
                self.audit.append(("dispatch_denied", request_id))
                return False
            entry = self.requests.get(request_id)
            if entry is None:
                raise KeyError("reserve budget before dispatch")
            if entry["effect"] is not None:
                self.audit.append(("idempotent_replay", request_id))
                return entry["effect"]
            effect_id = "effect:" + request_id
            self.effects.append(effect_id)
            entry["effect"] = effect_id
            entry["status"] = "in_flight"
            self.audit.append(("tool_dispatched", request_id, effect_id))
            return effect_id

    def stop_parent(self):
        with self.lock:
            self.parent_active = False
            self.child_active = False
            self.provider_cancel_requested = True
            for entry in self.requests.values():
                if entry["status"] in ("reserved", "in_flight"):
                    entry["status"] = "stopped_pending_reconciliation"
            self.audit.append(("parent_stop", "child_grants_revoked", "provider_cancel_requested"))

    def provider_result(self, request_id, *, charge=0):
        """Simulates an external provider returning late after stop."""
        with self.lock:
            entry = self.requests[request_id]
            if entry["status"] == "stopped_pending_reconciliation":
                entry["status"] = "late_result_requires_reconciliation"
                self.audit.append(("late_provider_result", request_id, charge,
                                   "containment_not_equivalent_to_provider_cancel"))
                return "late_result_requires_reconciliation"
            if charge < 0 or charge > entry["reservation"]:
                raise ValueError("charge exceeds reservation")
            self.reserved -= entry["reservation"]
            self.spent += charge
            entry["status"] = "settled"
            self.audit.append(("settled", request_id, charge))
            return "settled"


class P12P13P14P15IntegrationTests(unittest.TestCase):
    def test_authorized_child_tool_dispatch_and_retry_is_idempotent(self):
        model = SyntheticSeam()
        model.reserve("req-1", 4)
        first = model.dispatch("req-1")
        replay = model.dispatch("req-1")
        self.assertEqual(first, replay)
        self.assertEqual(model.effects, ["effect:req-1"])
        self.assertEqual(sum(1 for e in model.audit if e[0] == "tool_dispatched"), 1)

    def test_tenant_mismatch_denied_without_effect(self):
        model = SyntheticSeam()
        model.reserve("req-tenant", 2)
        self.assertFalse(model.dispatch("req-tenant", tenant="tenant-other"))
        self.assertEqual(model.effects, [])

    def test_parent_stop_revokes_child_and_blocks_new_dispatch(self):
        model = SyntheticSeam()
        model.reserve("req-stop", 3)
        model.stop_parent()
        self.assertFalse(model.dispatch("req-stop"))
        self.assertEqual(model.effects, [])
        self.assertTrue(model.provider_cancel_requested)
        self.assertEqual(model.requests["req-stop"]["status"], "stopped_pending_reconciliation")

    def test_late_provider_result_is_not_misreported_as_cancelled(self):
        model = SyntheticSeam()
        model.reserve("req-late", 5)
        model.dispatch("req-late")
        model.stop_parent()
        state = model.provider_result("req-late", charge=2)
        self.assertEqual(state, "late_result_requires_reconciliation")
        self.assertIn("containment_not_equivalent_to_provider_cancel",
                      str(model.audit[-1]))

    def test_concurrent_duplicate_reserve_and_dispatch_has_one_effect(self):
        model = SyntheticSeam(budget=6)
        errors = []
        def worker():
            try:
                model.reserve("req-race", 3)
                model.dispatch("req-race")
            except Exception as exc:  # surfaced after thread joins
                errors.append(exc)
        threads = [threading.Thread(target=worker) for _ in range(16)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        self.assertEqual(model.reserved, 3)
        self.assertEqual(model.effects, ["effect:req-race"])

    def test_stop_then_retry_never_resurrects_child_task(self):
        model = SyntheticSeam()
        model.reserve("req-resume", 1)
        model.stop_parent()
        self.assertFalse(model.dispatch("req-resume"))
        self.assertFalse(model.authorize("t1", "tool:write"))
        self.assertEqual(model.effects, [])

    def test_audit_order_records_reservation_dispatch_then_stop(self):
        model = SyntheticSeam()
        model.reserve("req-audit", 2)
        model.dispatch("req-audit")
        model.stop_parent()
        names = [event[0] for event in model.audit]
        self.assertLess(names.index("budget_reserved"), names.index("tool_dispatched"))
        self.assertLess(names.index("tool_dispatched"), names.index("parent_stop"))


if __name__ == "__main__":
    unittest.main()
