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
A read-only review of recent workflow runs across the 12 public repositories showed successful scan, test, and static-analysis checks where those workflows were configured. The root CodeQL run for commit `e09462c` was still in progress. This is not a complete all-history audit or security certification.

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


## Secret-scan triage
- Gitleaks reported one `generic-api-key` match in a historical portfolio-status sentence at commit `aa27337eb1e51a7117d7cb188bf03470ad18feb4`.
- Redacted scan output identified ordinary prose, not a credential/token value. The current wording was revised to avoid repeating the triggering phrase.
- A narrowly scoped Gitleaks allowlist now requires the exact historical commit, exact file path, and matching line text; it does not disable the detector repository-wide.
- [Full-history secret scan after allowlist correction — passed](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41503704969).
- The earlier scan failures were configuration/false-positive triage, not evidence that a live credential was exposed. Keep the allowlist under review and remove it if the prose/fingerprint changes.


## Synthetic budget stress probe (isolated model)
A small standalone synthetic ledger was exercised against six explicitly defined invariants:
1. Sibling reservations cannot overcommit shared capacity.
2. A revoked actor cannot reserve new capacity.
3. Cancellation plus late usage reconciles reservation and actual usage.
4. A cancelled request cannot later commit usage a second time.
5. Settlement cannot exceed the reservation.
6. Reserved plus committed capacity remains within the configured limit.

Result: **6/6 checks passed in the synthetic model**.

This is not an integration test of the Agent-Delegated-Budget-Enforcement-Fixtures validator or any real budget service. The policy choices (especially cancellation/late-arrival reconciliation) are illustrative and require specification-level review before being treated as normative. The public budget-fixture repository currently validates fixture structure and accounting relationships; it does not simulate concurrency or enforce a runtime ledger.

## Access / verification limits (continued)
- Branch-protection endpoint reads returned HTTP 403 for the GitHub connector. Rulesets/required checks cannot be verified from this connection; user-side GitHub settings review remains required.
- No production credential revocation, account recovery, actual queue/scheduler, or real agent stop was attempted.


## Adversarial follow-up — P15 model event isolation (2026-11-02)

Latest root commit: `7b8ba5d2af66ab75f2455aacae6e8ba0e0d24fb1`.

### Newly discovered weakness and mitigation

A caller could mutate the stop event object returned by the reference model, thereby modifying the same object retained in the idempotency cache and potentially corrupting future replay results. This was a model-level defect (not a production incident).

Changes:
- Return defensive copies for cached idempotent responses.
- Keep independent copies in the cache and in the in-memory audit list.
- Serialize the model's dispatch authorization snapshot with stop transitions using the same process-local lock.
- Add tests for returned-event mutation, replay copy isolation, child dispatch denial after stop, and cyclic parent graphs failing closed.

Source change commit: `15b825e16bcc2e91a8d254b64f6fa816ef2a1c15`.  
Regression tests commit: `7b8ba5d2af66ab75f2455aacae6e8ba0e0d24fb1`.

### CI evidence on the latest commit

- [P15 validation — success](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41508203955)
- [Full-history secret scan — success](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41508203917)
- [CodeQL — still running at last poll](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41508203932)
- P15 test job output: **27 tests run; 23 passed; 4 skipped; no failures**.

The four skips remain UI tampering, accessibility, distributed stop/resume race, and tamper-evident external audit storage. The new dispatch-lock test only verifies the in-process model's snapshot behavior; it is not an atomic real-world dispatch/execute guarantee. It does not resolve multi-process or distributed races.

### Additional model caveats identified

- The reference model still has no real identity/token revocation, queue/scheduler cancellation, provider API cancellation, durable audit log, or independent stop control.
- A successful boolean dispatch check is not an execution reservation; an actual runtime needs an atomic authorization-and-dispatch boundary or a capability/gateway that can prevent TOCTOU races.
- The synthetic budget model and P15 are separate; there is no integrated parent/child budget ledger or real scheduler/runtime enforcement.
- Tests validate model invariants and deliberately malformed graph input, not deployed service behavior.


## P12 SQLite idempotency harness (2026-11-02)

Added a local synthetic SQLite tool-effect ledger to `Agent-Tool-Retry-Idempotency-Fixtures`. Its modeled side effect and operation record are stored in the same transaction. Tests:

- Response loss after commit followed by replay after constructing a fresh service object.
- Same key with different payload rejected as conflict.
- Twelve concurrent threads using one key/payload produce one modeled effect and the same replay result.
- Injected pre-commit crash rolls back the effect and ledger; retry then executes once.
- Same key under different scope does not collide.

Validation: [P12 fixture CI success](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures/actions/runs/41511873192), **7 tests total (2 existing validator tests + 5 harness tests), success**. [Secret scan success](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures/actions/runs/41511872896). CodeQL was still in progress at last poll.

Commits: harness `63dc884`, tests `447e984`, documentation `570689c`, README `89fb6f3`.

Limit: this is a same-SQLite-transaction simulation. It does not establish exactly-once behavior for external provider APIs whose side effect cannot participate in that transaction. It does not test multi-host failure, key expiry, auth isolation, provider reconciliation, or production durability. See [synthetic harness boundary notes](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures/blob/main/docs/synthetic-idempotency-harness.md).
