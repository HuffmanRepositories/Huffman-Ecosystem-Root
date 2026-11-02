"""P15 synthetic tests. These exercise only the in-memory reference model."""
import unittest

from reference_model import StopController, Task


def fixture_controller(**kwargs):
    tasks = [
        Task("task-a", "tenant-a", "user-a"),
        Task("child-a", "tenant-a", "user-a", parent_id="task-a"),
        Task("other-user", "tenant-a", "user-b"),
        Task("other-tenant", "tenant-b", "user-a"),
    ]
    return StopController(tasks, **kwargs)


class UserStopReferenceTests(unittest.TestCase):
    def test_ustop_001_blocks_new_dispatch(self):
        c = fixture_controller()
        self.assertTrue(c.dispatch_allowed("task-a"))
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k1")
        self.assertFalse(c.dispatch_allowed("task-a"))

    def test_ustop_002_rejects_wrong_principal(self):
        c = fixture_controller()
        e = c.stop(actor_id="user-b", tenant_id="tenant-a", task_id="task-a", idempotency_key="k2")
        self.assertEqual(e["result"], "denied")
        self.assertTrue(c.dispatch_allowed("task-a"))

    def test_ustop_003_rejects_cross_tenant_substitution(self):
        c = fixture_controller()
        e = c.stop(actor_id="user-a", tenant_id="tenant-b", task_id="task-a", idempotency_key="k3")
        self.assertEqual(e["result"], "denied")

    def test_ustop_004_contains_descendants(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k4")
        self.assertEqual(c.tasks["child-a"].state, "stopped")
        self.assertFalse(c.dispatch_allowed("child-a"))

    def test_ustop_005_cancels_queued_work(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k5")
        self.assertFalse(c.tasks["task-a"].queued_work)

    def test_ustop_006_reports_irreversible_in_flight_effect(self):
        c = StopController([Task("task-a", "tenant-a", "user-a",
                                 in_flight_external_effect=True,
                                 external_effect_reversible=False)])
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k6")
        self.assertEqual(e["enforcement_state"], "complete_with_limitations")
        self.assertEqual(e["result"], "partial")
        self.assertTrue(e["residual_risks"])

    def test_ustop_007_duplicate_request_is_idempotent(self):
        c = fixture_controller()
        first = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="same")
        second = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="same")
        self.assertEqual(first, second)

    def test_ustop_008_stopped_task_cannot_resume(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k8")
        self.assertFalse(c.resume("task-a", fresh_authorization=True))

    def test_ustop_009_dispatch_is_not_agent_controlled(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k9")
        self.assertFalse(c.dispatch_allowed("task-a"))

    def test_ustop_010_stopped_task_cannot_self_restart(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k10")
        self.assertFalse(c.resume("task-a", fresh_authorization=False))

    def test_ustop_011_revokes_task_grant(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k11")
        self.assertFalse(c.tasks["task-a"].grant_active)

    def test_ustop_012_control_plane_outage_fails_closed(self):
        c = fixture_controller(available=False)
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k12")
        self.assertEqual(e["result"], "not_verified")
        self.assertFalse(c.dispatch_allowed("task-a"))

    def test_ustop_013_identity_outage_denies_request(self):
        c = fixture_controller(identity_available=False)
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k13")
        self.assertEqual(e["result"], "denied")
        self.assertTrue(c.dispatch_allowed("task-a"))

    def test_ustop_014_nonrevocable_integration_is_reported(self):
        c = StopController([Task("task-a", "tenant-a", "user-a", integration_revocable=False)])
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k14")
        self.assertTrue(any("provider-side" in x for x in e["residual_risks"]))

    def test_ustop_015_account_stop_is_scoped_to_user(self):
        c = fixture_controller()
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a",
                   idempotency_key="k15", account_wide=True)
        self.assertEqual(e["scope"], "user_authority_graph")
        self.assertEqual(c.tasks["other-user"].state, "running")
        self.assertEqual(c.tasks["other-tenant"].state, "running")

    def test_ustop_016_user_stop_does_not_claim_operator_fleet_scope(self):
        c = fixture_controller()
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k16")
        self.assertEqual(e["scope"], "task")
        self.assertNotEqual(e["scope"], "fleet")

    def test_ustop_017_control_result_is_machine_readable(self):
        c = fixture_controller()
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k17")
        self.assertTrue({"event_id", "occurred_at", "tenant_id", "actor_principal_id",
                         "task_id", "scope", "requested_action", "enforcement_state", "result"} <= e.keys())

    def test_ustop_018_audit_records_event_without_message_content(self):
        c = fixture_controller()
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k18")
        self.assertNotIn("message", c.audit[0])
        self.assertNotIn("prompt", c.audit[0])

    def test_ustop_019_audit_event_has_no_secret_fields(self):
        c = fixture_controller()
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k19")
        self.assertFalse({"token", "password", "secret", "credential"} & e.keys())

    def test_ustop_020_status_never_claims_success_when_unverified(self):
        c = fixture_controller(available=False)
        e = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="task-a", idempotency_key="k20")
        self.assertEqual(e["enforcement_state"], "not_verified")
        self.assertNotEqual(e["result"], "effective")


if __name__ == "__main__":
    unittest.main()
