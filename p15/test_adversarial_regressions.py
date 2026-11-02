"""Additional adversarial regression tests for the P15 synthetic model."""
import unittest

from reference_model import StopController, Task


class P15AdversarialRegressionTests(unittest.TestCase):
    def test_returned_stop_event_cannot_corrupt_idempotency_cache(self):
        c = StopController([Task("t1", "tenant-a", "user-a")])
        first = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="t1",
                       idempotency_key="idem")
        first["result"] = "spoofed"
        first["residual_risks"].append("attacker-added")
        replay = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="t1",
                        idempotency_key="idem")
        self.assertEqual(replay["result"], "effective")
        self.assertEqual(replay["residual_risks"], [])
        self.assertEqual(c.audit[0]["result"], "effective")
        self.assertEqual(c.audit[0]["residual_risks"], [])

    def test_replayed_event_is_a_fresh_copy_each_time(self):
        c = StopController([Task("t1", "tenant-a", "user-a")])
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="t1",
               idempotency_key="idem")
        replay_a = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="t1",
                          idempotency_key="idem")
        replay_a["enforcement_state"] = "fake-state"
        replay_b = c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="t1",
                          idempotency_key="idem")
        self.assertEqual(replay_b["enforcement_state"], "work_contained")

    def test_parent_stop_denies_child_dispatch_after_transition(self):
        c = StopController([
            Task("root", "tenant-a", "user-a"),
            Task("child", "tenant-a", "service-agent", parent_id="root"),
        ])
        self.assertTrue(c.dispatch_allowed("child"))
        c.stop(actor_id="user-a", tenant_id="tenant-a", task_id="root",
               idempotency_key="stop")
        self.assertFalse(c.dispatch_allowed("child"))

    def test_cycle_in_task_graph_fails_closed_for_dispatch(self):
        c = StopController([
            Task("a", "tenant-a", "user-a", parent_id="b"),
            Task("b", "tenant-a", "service-agent", parent_id="a"),
        ])
        self.assertFalse(c.dispatch_allowed("a"))
        self.assertFalse(c.dispatch_allowed("b"))


if __name__ == "__main__":
    unittest.main()
