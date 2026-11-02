# Ecosystem System Test Matrix and Missing-Detail Review

**Review date:** 2026-11-02  
**Status:** planning / gap review; not a runtime certification  
**Scope:** public technical projects P10–P15, interoperability/metrics fixtures, GitHub CI and repository control plane.

> The ecosystem consists of specifications, fixture sets, validation scripts, documentation, and a P15 in-memory reference model. No unified production agent runtime has been implemented or tested. A green fixture validator means fixture/schema/semantic checks passed—not that an agent product conforms or that a live security control is enforced.

## Test-level vocabulary

- **L0 — static/schema:** JSON, schema, repository structure, lint, policy/doc consistency.
- **L1 — fixture/semantic:** synthetic fixture validator checks documented input/output relationships.
- **L2 — model/unit:** deterministic reference-model or harness behavior.
- **L3 — component integration:** real services/adapters wired in an isolated test environment.
- **L4 — system/E2E:** multiple agents, queues, identity, policy, storage, tools, budgets and UI together.
- **L5 — adversarial/operational:** fault injection, race/partition, credential revocation, restore, incident drills.

L0/L1/L2 do not imply L3/L4/L5.

## System-by-system coverage and missing evidence

| System | Current evidence / known tests | What remains untested or under-specified | Recommended next test |
|---|---|---|---|
| P10 — Memory portability | Synthetic fixtures and validator CI | Semantic preservation across real vendor formats; unknown-field retention; privacy/consent; deletion/expiry; conflict resolution; migration rollback | Round-trip fixtures through at least 2 independent adapters; compare normalized meaning, provenance, metadata, loss report and deletion behavior |
| P11 — Evaluation/oracle integrity | Synthetic fixture validator and CI | Oracle provenance, version pinning, contamination/leakage, evaluator disagreement, mutation/tampering, false pass/fail calibration | Mutation suite that corrupts labels, references, evaluator identity/version, hidden-test boundaries and expected output; verify fail-closed detection |
| P12 — Tool retry/idempotency | Fixture semantic validator and CI; **new SQLite synthetic harness** tests crash-before-commit rollback, post-commit response-loss replay after process-object restart, concurrent 12-thread duplicate requests, payload conflict, and key scope isolation | Real side-effecting provider semantics; multi-host/distributed races; key expiry; provider reconciliation; ledger durability under actual host failure; external effects not sharing transaction | Extend into provider adapter harness with durable outbox/inbox/reconciliation; keep unknown outcome explicit. [Harness doc](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures/blob/main/docs/synthetic-idempotency-harness.md) |
| P13 — Delegation scope boundaries | Fixture validator and CI plus **new synthetic policy model** testing action/resource attenuation, tenant/issuer mismatch, expiry, ancestor revocation and actor binding | Actual token/capability propagation, identity provider, wildcard/resource hierarchy policy semantics, revocation latency, confused deputy, real tenant isolation | Parent/child agent integration harness: scoped tokens, provider identity, cross-tenant attempts, fan-out, and P15 stop propagation. [Synthetic model boundaries](https://github.com/HuffmanRepositories/Agent-Delegation-Scope-Boundary-Fixtures/blob/main/docs/synthetic-delegation-model.md) |
| P14 — Delegated budget enforcement | Fixture semantic validator and CI; previous six synthetic probes; **new SQLite hierarchical ledger model** tests sibling concurrent reservations, nested caps, reserve replay, settlement, release, revoked ancestor and over-limit actual usage | Distributed ledger, provider usage reconciliation, late charges, currency/unit normalization, budget-window rollover, external billing and production enforcement | Multi-worker shared-ledger + provider reconciliation integration; delayed/late usage, crash/recovery, cross-region coordination. [Synthetic ledger limits](https://github.com/HuffmanRepositories/Agent-Delegated-Budget-Enforcement-Fixtures/blob/main/docs/synthetic-budget-ledger.md) |
| P15 — User emergency stop | In-memory reference model + **7-test synthetic P12–P15 seam harness** (P12 idempotency, P13 tenant/action delegation, P14 budget reservation, P15 stop/revoke/late provider response); latest CI: 34 total tests, 30 passed, 4 skipped | Real identity/token enforcement, multi-process/distributed races, real queue/scheduler/callback cancellation, provider-side cancellation, durable audit, UI/accessibility, actual billing/usage reconciliation | Replace the seam model with adapters to independent service components in a disposable L3/L4 environment; add durable provider reconciliation and multi-host stop races. [Harness limits](p15/CROSS-SYSTEM-INTEGRATION-HARNESS.md) |
| OAC — compatibility mapping | Validation and CodeQL/secret scan workflows | Real cross-provider compatibility tests, capability negotiation, semantic mismatch and fallback safety | Implement adapter contract tests using independently maintained provider mocks and mismatch fixtures |
| OAC Fixtures | Fixture validation CI | Fixture interoperability with independent implementations; version compatibility matrix; expected outcome provenance | Validate fixture corpus against at least two independent consumers; track false positives/negatives and version-specific behavior |
| OARMI — run metrics | Fixture validation CI | Metric semantic equivalence, aggregation correctness, units, missing values, privacy, cardinality and clock skew | Cross-implementation round-trip and aggregation tests with missing/duplicate/late/out-of-order data |

## Cross-cutting system tests missing

### Authorization and identity
- Identity provider unavailable, delayed, stale cache, token expiry, revocation propagation and replay.
- Principal/tenant/task mismatch and confused-deputy paths.
- Explicit capability scope attenuation; child cannot expand parent privileges.
- Credential rotation and stale-session rejection with fake/disposable credentials.

### Concurrency and state transitions
- Stop vs resume, dispatch vs stop, reserve vs spend, retry vs commit, revoke vs authorize.
- Multi-process and distributed locking—not only in-process threads.
- Crash after an external side effect but before response persistence.
- Idempotency key reuse with same request, different target, different payload, expired key and concurrent requests.

### Queue / scheduler / agent lifecycle
- Child agents, retries, callbacks, delayed jobs, scheduled tasks, worker leases and queue replay.
- Stop during tool execution and after the provider accepted the request.
- Task graph cycles, missing parent references, stale parent state and partial graph visibility.
- No automatic resurrection after stop, revocation, crash recovery or retry.

### Budget and accounting
- Shared parent/child budgets, fan-out limits, currency/units, provider-specific usage.
- Concurrent reserve, commit, release, refund, late usage and over-settlement.
- Ledger persistence, reconciliation, rounding, negative/overflow values, and ledger unavailable.
- Independent hard limit enforcement that the model/agent cannot override.

### Observability / audit / privacy
- Correlation IDs for parent-child tasks, tool calls, retries, grants, budgets and stop events.
- Clock skew, duplicate/out-of-order events, dropped logs, partial audit store, tampering.
- Data minimization and secret/PII redaction without losing required forensic evidence.
- Honest state transitions: requested, accepted, dispatch blocked, child contained, provider cancellation requested, externally confirmed, residual action unresolved.

### Repository and supply-chain controls
- Required branch rules and status checks actually enforced, not merely recommended.
- Workflow token permissions minimum by job; external PR approval and fork isolation.
- Third-party actions pinned to immutable commit SHA and reviewed update process.
- CodeQL for Actions/workflow language where available; add workflow linting (e.g. actionlint/zizmor) as a defense-in-depth check.
- Dependency alerts, SBOM/provenance and release signing/attestation if/when releases are produced.
- Backups and restore verification with a separate trust boundary.

GitHub guidance emphasizes pinning workflow actions to verified commits and limiting permissions; OWASP additionally recommends workflow scanning, external PR approval, and least-privilege `GITHUB_TOKEN`. See [GitHub Actions security](https://docs.github.com/en/actions/how-tos/secure-your-work) and the [OWASP GitHub Actions Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html).

## Proposed execution order

1. **P12 durable idempotency crash/replay harness** — comparatively bounded and central to tool safety.
2. **P13 authorization/delegation harness** — fake principals, tenants, scoped capabilities, nested child agents.
3. **P14 concurrent budget ledger** — independent shared ledger and provider reconciliation.
4. **P15 distributed stop test harness** — multi-worker, queue, scheduler, identity and audit components.
5. **P10/P11 interoperability/accuracy matrix** — independent adapter/evaluator implementations.
6. **Portfolio-wide CI and settings verification** — branch rules, workflow permissions, Actions security, dependency alerts, releases and backup restoration.

For each test, record: test ID, fixture/spec revision, harness commit, environment, injected fault, expected result, actual result, timestamps, evidence links, severity, owner, remediation, and retest. A test with missing evidence or skipped integration steps is **not passed**.

## Release / maturity gate

Do not label a subsystem production-ready until:
- relevant L3/L4 tests exist and pass in an isolated environment;
- critical L5 security/recovery cases have evidence;
- independent review and remediation retests are complete;
- documentation distinguishes supported behavior from assumptions and known limits;
- deployment-specific credentials, user data and external services are tested only with explicit authorization and safe boundaries.

## Current conclusion

The current portfolio has a useful and increasingly adversarial **fixture/model validation base**. The main missing step is not “more README checks”; it is a shared, isolated system-test harness that joins identity, delegated authority, idempotency, budget, task lifecycle, stop control, metrics and audit persistence. Keep these systems modular but test the seams between them.
