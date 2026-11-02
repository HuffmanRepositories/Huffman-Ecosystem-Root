# Agent Compromise, Rogue-Behavior, and Incident Response Protocol

**Status:** Draft operational protocol for review  
**Maintainer:** Robert Huffman (MrCakes931)  
**Prepared:** 2026-11-02

## 1. Terminology

"Rogue behavior" is an operational label for observable behavior outside approved authority, policy, scope, or safety constraints. It does not assert consciousness, intent, sentience, or independent motive.

Treat an agent as potentially compromised or unsafe when its actions, tool calls, delegated tasks, outputs, memory, or runtime integrity violate defined boundaries, regardless of whether the cause is prompt injection, model error, malicious content, compromised tools, stolen credentials, configuration drift, or human misuse.

## 2. Incident classes

- **C0 — Anomaly:** unusual but non-impacting behavior; observe and record.
- **C1 — Policy violation:** attempted or completed low-impact out-of-scope action; restrict relevant tool.
- **C2 — Security event:** unauthorized access attempt, unexpected delegation, policy bypass, or sensitive-data exposure risk; suspend affected capabilities and investigate.
- **C3 — Active compromise or material impact:** confirmed unauthorized data access/exfiltration, destructive action, privilege escalation, continued actions after revocation, or integrity compromise; revoke, isolate, and activate incident command.
- **C4 — Critical safety event:** imminent risk of serious harm, critical infrastructure disruption, broad compromise, or uncontrolled high-impact actions; invoke emergency stop and applicable human emergency procedures.

Severity should reflect impact, reachability, persistence, and confidence in evidence. Escalate when uncertain and consequences may be severe.

## 3. Detection signals

Monitor independently verifiable events:
- Tool calls not on an approved allowlist or outside task scope.
- Access attempts against resources not granted to the agent.
- New or modified credentials, policies, tools, plugins, callbacks, or delegation grants.
- Attempts to disable logs, monitoring, authorization, rate limits, or stop controls.
- Unusual outbound traffic, data volume, destinations, or secret access.
- Child-agent creation or delegation outside an approved graph.
- Repeated denials, retries, recursion, unexpected spend, or concurrency spikes.
- Memory or state changes that alter permissions, identity, or safety configuration.
- Actions after a revocation or stop event.
- Integrity mismatches in deployed artifacts, tool definitions, policy bundles, or audit records.

Behavioral anomaly detection is a signal for review, not proof of malicious intent. Correlate with trusted identity, policy, network, and execution logs.

## 4. Response workflow

1. **Triage:** assign incident ID and severity; preserve the first observed event.
2. **Contain:** apply the appropriate independent stop level; block new grants and delegation.
3. **Revoke:** invalidate credentials, sessions, leases, and grants for the affected identity and descendants.
4. **Isolate:** quarantine runtime, tool gateway, worker pool, or affected integration; maintain separate forensic access.
5. **Scope:** identify all agents, identities, tool calls, data stores, queues, scheduled jobs, webhooks, and external services touched.
6. **Preserve evidence:** retain relevant logs, policy versions, tool schemas, prompts and outputs where lawful and necessary, model/build identifiers, configuration, memory diffs, artifact hashes, and timestamps.
7. **Assess impact:** determine data accessed, altered, disclosed, deleted, or transmitted; identify human and downstream consequences.
8. **Notify:** escalate to system owner, security, privacy, legal, and affected parties according to incident plan and applicable law/contract.
9. **Eradicate and recover:** patch root cause, rotate secrets, rebuild trusted workloads, restore verified data, reconcile external side effects, and test.
10. **Review:** publish an appropriately redacted post-incident report and track corrective actions.

## 5. Delegation and supply-chain containment

Every agent and delegated worker should have a distinct identity, accountable owner, bounded task, explicit permission set, expiry, and traceable parent/child relationship. Maintain a delegation ledger. On containment, traverse the delegation graph and revoke descendants, active sessions, and pending jobs. Verify independently with downstream service logs; do not assume a parent stop cascades.

Third-party tools, MCP servers, plugins, skills, model endpoints, and packages are separate trust boundaries. Pin and review versions, minimize scopes, verify provenance, and provide a way to disable each integration independently.

## 6. Data and privacy handling

Use synthetic fixtures for tests. During incidents, collect only evidence necessary to establish scope and impact. Restrict access, encrypt evidence, record chain of custody, set retention/deletion deadlines, and consult privacy/legal owners before collecting or sharing personal, biometric, health, financial, or children's data.

## 7. Prohibited responses

Do not:
- Let an agent autonomously retaliate, attack, scan, or disrupt suspected attacker systems.
- Allow an agent to erase logs, destroy evidence, or conceal activity.
- Rely on the affected agent to certify its own shutdown or recovery.
- Automatically restore broad privileges after a stop.
- Publish credentials, personal data, exploit details, or sensitive incident evidence.
- Treat a model refusal, apology, or self-description as proof of containment.

## 8. Readiness exercises and metrics

Exercise tabletop and technical scenarios at least annually and after material architecture changes:
- Prompt injection through retrieved content or tool output.
- Compromised tool/plugin or malicious tool description.
- Stolen or overprivileged agent credential.
- Parent-child delegation chain with active jobs.
- Agent continues after stop request.
- Exfiltration attempt through approved and unapproved channels.
- Runaway retries, recursion, token use, or cost.
- Logging/control-plane outage.
- Recovery from compromised model, tool, memory, or configuration artifact.

Track detection time, stop-request-to-last-action time, credential-revocation time, descendant containment coverage, queued-job cancellation coverage, evidence completeness, recovery time, and recurrence rate.

## 9. Legal and governance

This protocol does not determine legal obligations. Incident owners must assess applicable privacy, breach-notification, contractual, employment, sector-specific, and law-enforcement requirements with qualified counsel. For Colorado operations, consider the Colorado Privacy Act and C.R.S. 6-1-716 where personal data and covered entities are involved. Do not claim compliance merely because this protocol exists.

## 10. Relationship to companion documents

- [Emergency Stop and Independent Containment Profile](KILLSWITCH-AND-CONTAINMENT.md)
- [Safe Use and Security](SAFE-USE-AND-SECURITY.md)
- [Governance](GOVERNANCE.md)
- [Compliance and Legal Review](COMPLIANCE-AND-LEGAL-REVIEW.md)

**Attribution:** Original protocol authored for the HuffmanRepositories ecosystem by Robert Huffman (MrCakes931). Third-party contributions and sources must be separately attributed.
