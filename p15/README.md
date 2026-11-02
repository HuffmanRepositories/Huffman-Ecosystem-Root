# P15 — User-Controlled Emergency Stop Reference Fixtures

**Status:** synthetic reference model and unit tests; not a production deployment.

This package turns the P15 test plan into an executable, deterministic in-memory reference model. It covers user/task ownership, tenant boundaries, descendant containment, queued work, grant revocation, idempotency, fail-closed dispatch, truthful residual-risk reporting, and the 20 USTOP scenario identifiers.

## Run locally

```bash
python -m unittest discover -s p15 -p 'test_*.py' -v
```

No third-party packages, network access, real identities, credentials, or production data are required.

## Important limitations

- This model is not an API server, user interface, identity provider, policy gateway, credential revoker, queue/scheduler integration, runtime supervisor, or hosted kill switch.
- Tests validate the model's behavior, not a vendor's or deployer's implementation.
- Accessibility, distributed concurrency, real credential invalidation, third-party cancellation, and infrastructure isolation require separate integration and adversarial tests.
- A successful local test run is not a security certification or production-readiness claim.

Maintainer: Robert Huffman (MrCakes931).
