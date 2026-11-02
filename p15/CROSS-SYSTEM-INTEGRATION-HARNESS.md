# Synthetic P12–P15 Cross-System Seam Harness

**Status:** synthetic in-memory integration-style test; not a production system test.

## Run

```bash
python -m unittest discover -s p15 -p 'test_*.py' -v
```

The harness combines simplified concepts from:
- **P12:** idempotent request replay and duplicate tool dispatch
- **P13:** parent/child delegated grant and tenant/action scope
- **P14:** reservation-before-dispatch and shared budget accounting
- **P15:** parent stop, child grant revocation, dispatch denial and containment status

## Scenarios

- Authorized child operation and retry replay create one synthetic effect.
- Tenant mismatch is denied.
- Parent stop revokes child authorization and blocks subsequent dispatch.
- A simulated late provider result after stop is reported as requiring reconciliation—not as provider cancellation.
- Concurrent duplicate reservations/dispatches produce one synthetic effect.
- Retry after stop does not resurrect the task.
- Audit event order captures reservation, dispatch, and stop.

## Limits / non-claims

This harness uses process-local memory and a lock. It does not integrate the separately maintained P12/P13/P14 libraries or P15 controller as imported dependencies; it composes **contract-like synthetic behaviors** in one small model. It does not test distributed synchronization, real queues, provider cancellation, actual billing, identity/token cryptography, persistence, or deployed policy enforcement. Late external effects may still occur after local containment. Passing this suite is not production readiness, a security certification, or evidence that real-world exactly-once execution is achievable.

Maintainer: Robert Huffman (MrCakes931).
