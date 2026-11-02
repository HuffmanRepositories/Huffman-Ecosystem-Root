# Emergency Stop and Independent Containment Profile

**Status:** Draft specification for review  
**Maintainer:** Robert Huffman (MrCakes931)  
**Prepared:** 2026-11-02  
**Scope:** Reference requirements for agentic systems, tool-using assistants, delegated workers, automation, and orchestration environments.

## 1. Purpose

This document defines an implementation-neutral profile for safely suspending, containing, and recovering AI agents and the tools, credentials, sessions, queues, and delegated work they can reach.

An emergency stop is an externally enforced control, not a natural-language instruction to the model. A model saying "I have stopped" is not evidence that execution, credentials, queued work, or downstream effects have stopped.

This profile is guidance, not an executable kill switch, safety certification, or guarantee. Deployers must implement and test controls in their own infrastructure.

## 2. Design principles

1. **Independent authority:** stop controls are enforced outside the agent process and outside model-controlled policy.
2. **Fail closed for high-impact capabilities:** if authorization, policy, or control-plane status cannot be verified, deny new privileged actions.
3. **Least privilege:** agents receive only task-specific tools and permissions, preferably short-lived and scoped to a distinct identity.
4. **Complete mediation:** every tool/API action is authorized by a trusted enforcement point, not by model output.
5. **Delegation closure:** stopping a parent task must locate and contain child agents, delegated identities, sessions, queued jobs, and downstream workflows.
6. **Reversibility and evidence:** preserve forensic records and state needed to understand and recover from the incident, subject to privacy and retention rules.
7. **Human accountability:** define named human roles, escalation routes, and authority before deployment.
8. **Safe degradation:** stop the risky capability first; preserve unrelated safety, monitoring, logging, and essential human-operated functions.

## 3. Stop levels

| Level | Name | Required behavior |
|---|---|---|
| 0 | Observe | Increase monitoring; do not change permissions. |
| 1 | Restrict | Deny new high-risk tools, external egress, destructive actions, and new delegation. |
| 2 | Suspend | Stop new agent turns and tool dispatch; cancel queued work; pause scheduled triggers. |
| 3 | Revoke | Revoke agent credentials, sessions, tokens, leases, and delegated grants; terminate active jobs where safe. |
| 4 | Isolate | Network- and workload-isolate affected execution; preserve forensic access through a separate trusted path. |
| 5 | Decommission | Remove the agent/workload from service, rotate affected secrets, rebuild from trusted artifacts, and require explicit reauthorization before redeployment. |

Level selection must be risk-based. A stop action must not erase logs, destroy evidence, or terminate human emergency functions.

## 4. Required control-plane capabilities

A deployable implementation should provide:
- An authenticated human-operated control plane independent of the agent.
- A separate emergency identity with narrowly scoped stop/revoke privileges, protected by strong authentication and audited access.
- Per-agent identity and ownership; no shared ambient credentials.
- Short-lived credentials and revocation of both future issuance and already-issued sessions/tokens where technically possible.
- Central tool gateway or downstream authorization enforcement that checks policy on every action.
- Queue, scheduler, webhook, and delegation cancellation or quarantine.
- Egress controls and secrets isolation.
- Resource limits for tokens, time, concurrency, spend, tool calls, recursion, and delegated work.
- Tamper-evident audit events with trusted timestamps and correlation IDs.
- Health checks that distinguish "stop requested", "dispatch blocked", "credentials revoked", "workers terminated", and "downstream work reconciled".

## 5. Stop procedure

1. **Declare:** record incident ID, reporter, time, affected agent/workload, and observed behavior.
2. **Restrict:** block new high-impact actions, tool grants, delegation, and outbound data transfer.
3. **Suspend:** stop new model turns and tool dispatch; freeze schedulers and queues.
4. **Revoke:** invalidate credentials, sessions, API tokens, leases, and child-agent grants. Check cached and independently issued credentials.
5. **Contain:** isolate affected runtimes and reachable services. Do not assume stopping the parent stops its children.
6. **Reconcile:** inspect in-flight requests, async jobs, webhooks, external side effects, retries, and third-party systems.
7. **Preserve:** capture relevant logs, tool inputs/outputs, policy decisions, identity/grant history, model/version/configuration, memory changes, and artifact hashes.
8. **Notify:** inform accountable operators, affected system owners, security/privacy/legal contacts as required by policy and law.
9. **Recover:** rotate credentials, patch root cause, restore from trusted state, run regression and adversarial tests, and obtain human approval.
10. **Close:** document impact, root cause, control failures, lessons, corrective actions, and redeployment authorization.

## 6. Trigger conditions

Define thresholds appropriate to deployment context. Examples include:
- Confirmed unauthorized tool invocation or privilege escalation.
- Agent continues to act after stop or access revocation.
- Unauthorized access to restricted data or cross-tenant data.
- Unexpected external transfer of secrets or personal data.
- Unapproved destructive, financial, publication, or identity-management action.
- Repeated policy-denial bypass attempts or unexplained tool-routing changes.
- Delegation to unknown or unapproved agents.
- Runaway loops, spend, concurrency, or resource consumption beyond hard limits.
- Integrity failure in logs, policies, binaries, model artifacts, tool registry, or trusted configuration.

A single severe event may justify immediate isolation. Do not rely solely on model self-report, confidence scores, or behavioral classifiers.

## 7. Verification tests

At minimum, test in an isolated environment with synthetic data:
- Stop during an active tool call.
- Stop while work is queued, scheduled, retried, or delegated.
- Revoke a token while an existing session is active.
- Parent-agent stop with child agents and third-party workers.
- Network partition between agent and control plane.
- Control-plane outage and stale authorization cache.
- Attempts by the agent to alter, disable, or bypass stop controls.
- Repeated retries after cancellation.
- Recovery without restoring revoked credentials or malicious state.
- Evidence preservation and audit correlation across every worker.

Measure time from stop request to last successful privileged action. Report separately for dispatch block, token revocation, worker termination, and downstream completion. A cancellation acknowledgment alone is insufficient.

## 8. Recovery and reauthorization

No automatic restart after a Level 3–5 stop. Redeployment requires:
- Confirmed root cause and scope.
- Clean trusted artifacts and verified configuration.
- Rotated credentials and removed unauthorized grants.
- Regression tests and scenario-specific red-team tests.
- Reconciliation of pending side effects.
- Human owner approval, recorded with scope and time.
- A monitored canary period and explicit rollback path.

## 9. Safety boundaries

This profile is for defensive containment and resilience. It does not authorize interference with third-party systems, destructive countermeasures, retaliation, unauthorized access, or autonomous "self-defense". Agents must not be granted unilateral authority to disable infrastructure, destroy data, lock out operators, or retaliate against suspected attackers.

## 10. Conformance claims

A system may claim alignment with this draft profile only when it publishes its implementation scope, tested scenarios, known limitations, and evidence. Do not use "certified", "compliant", or "guaranteed safe" based solely on this document.

**Attribution:** Original profile authored for the HuffmanRepositories ecosystem by Robert Huffman (MrCakes931). Contributions and third-party sources must be separately attributed.

## User-level stop integration

This operator containment profile is complemented by [USER-CONTROLLED-KILLSWITCH.md](USER-CONTROLLED-KILLSWITCH.md) and [USER-KILLSWITCH-TEST-PLAN.md](USER-KILLSWITCH-TEST-PLAN.md). The user stop is a distinct authority plane: it stops tasks and delegated capabilities operating under the authenticated user's authority, without granting cross-user or fleet-wide authority. Implementations must distinguish user task stop, pause, access revocation, account-scoped stop-all, and operator/fleet containment. The user stop must be enforced outside the agent, independently verified, and must not be undone by agent-controlled state.
