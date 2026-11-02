# Failure-Test Execution Log — 2026-11-02

## Execution scope
This records synthetic reference-model tests and GitHub Actions checks. No live production agent, user credential, third-party integration, production repository deletion, or account recovery process was exercised.

## P15 reference suite
- Source: `p15/reference_model.py` and `p15/test_reference_model.py`.
- Initial local run before the added regression test: **20 tests; 16 passed; 4 skipped**.
- After the idempotency-key regression test: **21 tests; 17 passed; 4 skipped**.
- After adding USTOP-021 for multi-level delegated descendants: **22 tests; 18 passed; 4 skipped** (local rerun).
- Skipped tests:
  - USTOP-008: distributed stop/resume concurrency race
  - USTOP-009: real UI tampering / stop control visibility
  - USTOP-017: accessibility integration
  - USTOP-018: tamper-evident external audit storage
- The 4 skipped tests are integration gaps, not passing tests.

## Defect found
The adversarial probe reused an idempotency key for a different task under the same principal. The original reference model returned the prior task's cached “effective” stop event while leaving the new target running. This could mislead a caller that failed to bind the response to the requested task.

## Remediation
- Store a request signature alongside each cached idempotency result: tenant, task target, and account-wide scope.
- Return the cached event only when the incoming request signature matches.
- Deny a reused idempotency key when it refers to a different stop request.
- Add regression test `test_ustop_007b_reused_key_for_different_target_is_denied`.

Additional regression:
- USTOP-021 tests a root → child → grandchild → great-grandchild chain and verifies stopped state, grant revocation, queued-work cancellation, and dispatch denial at every level.
- Test commit: `117913bc478ed82c77c3a092b74ff339ee8ff486`.

Commits:
- Model fix: `5df297b70fe1e638f49e8e1718ab102fc0b305d1`
- Regression test: `e09462cf9fcd582e6a1f60b38b30bbaae6f2658f`

## CI evidence
For commit `e09462cf9fcd582e6a1f60b38b30bbaae6f2658f`:
- [P15 validation — passed](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41502945562)
- [Full-history secret scan — passed](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41502945632)
- [CodeQL — pending at the latest check](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41502945549)

## Portfolio workflow snapshot
A read-only review of the latest five workflow runs for each of the 12 public repositories found successful secret scans, validation/fixture CI, and CodeQL runs where those workflows existed in the sampled run window. The root CodeQL run for commit `e09462c` was still in progress. This is not a complete all-history audit or security certification.

## Scope of failure testing
| Scenario | Current evidence | Status |
|---|---|---|
| BAD-05: descendant containment | Synthetic nested descendant probe passed; existing USTOP-004 covers direct child containment | Partial; no distributed runtime |
| BAD-06: control-plane outage | USTOP-012 fail-closed model test passed | Model only |
| BAD-07: identity outage / stale authorization | USTOP-013 denial/fail-closed model test passed | Model only; no real token expiry/revocation |
| BAD-08: runaway delegation / budget | Not represented as a live budget-enforcement integration in P15 | Not tested |
| BAD-01: compromised credential | No real credential exercise | Not tested |
| BAD-03 / BAD-11: root repo compromise / destructive recovery | No isolated restore exercise | Not tested |

## Next actions
1. Add explicit tests for replay/retry after stop and for deeper descendant chains.
2. Extend the model or add a separate test harness for delegation depth, fan-out, budget exhaustion, and queue/callback resurrection.
3. Perform distributed concurrency tests with a dedicated multi-process harness.
4. Perform disposable-credential revocation tests in an isolated GitHub test repository.
5. Test backup restoration from independently verified snapshots.
6. Poll CodeQL for the latest commit and record the final result.
7. Keep production deployment and release claims blocked until integration evidence exists.
