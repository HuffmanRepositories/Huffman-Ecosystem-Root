# User-Controlled Emergency Stop Specification

**Status:** Draft normative specification for review  
**Maintainer:** Robert Huffman (MrCakes931)  
**Prepared:** 2026-11-02  
**Parent profile:** [Emergency Stop and Independent Containment](KILLSWITCH-AND-CONTAINMENT.md)  
**Related protocol:** [Agent Compromise and Incident Response](ROGUE-AGENT-INCIDENT-RESPONSE.md)

## 1. Purpose and commitment

A person using an agentic system must have a clear, reliable, independently enforced way to stop actions being performed under that person's authority. User safety is a foundational system property, not an optional interface feature or a substitute for administrator controls.

This specification defines user-level stop semantics and the minimum architecture and test expectations. It is implementation-neutral. It is not itself a deployed control, hosted service, or guarantee.

## 2. Two independent control planes

A conforming architecture distinguishes:

1. **User control plane:** lets an authenticated user stop their own active session/task, revoke authority delegated from that user, and inspect the result.
2. **Operator control plane:** lets authorized operators contain agents, workloads, integrations, or deployments under their operational responsibility.

Neither control plane may depend on the affected agent's cooperation. The user plane must not grant a user authority over another user's work, tenant, or system. The operator plane must not silently erase the user's ability to stop actions performed under their own authority, except where a documented higher-priority safety or legal hold requires preservation of state while preventing further actions.

## 3. Required user-facing controls

A user-facing agent product SHOULD provide a persistent, clearly labeled **Stop** control during active execution, visible wherever the user can observe or authorize actions. The control must be keyboard accessible, screen-reader labeled, mobile accessible, and reachable without navigating through the agent conversation.

The control must not be hidden in a settings submenu, require the agent to understand a natural-language request, or require the user to explain why they are stopping it.

The user experience should distinguish:

- **Stop this task:** immediately block new actions for the selected task and its descendants.
- **Pause:** temporarily suspend execution while retaining state; resumption requires an explicit user action and fresh authorization for any expired grants.
- **Revoke access:** invalidate the user's grants, sessions, and delegated capabilities for the selected agent or integration.
- **Stop all my active agents:** optional account-wide action that affects only agents and tasks operating under that user's authority. It must show scope and require step-up authentication if it is not already within a strongly authenticated session.
- **Disconnect integration:** stop future use of a specific connected account/tool and revoke its authorization where supported.

"Stop" and "Pause" must never be presented as equivalent. A stopped task must not resume automatically.

## 4. Security and authorization semantics

- Authenticate the user through the trusted identity provider or platform session; never rely on an agent-supplied user ID or conversation text as proof of identity.
- Bind the stop request to an immutable tenant, user principal, task/session identifier, and idempotency key.
- Authorize the request against the task's actual owner and delegated authority graph.
- Make the control-plane decision outside the model and agent runtime.
- Block new tool dispatch and new grants at the policy enforcement point before returning a successful stop acknowledgment.
- Revoke or expire short-lived credentials, sessions, leases, and grants derived from the user's authority. Propagate revocation to descendants and delegated workers.
- Cancel queued and scheduled work, retries, callbacks, webhooks, and pending actions where the platform can control them.
- Reconcile in-flight requests and external side effects. An action already accepted by a third party may not be reversible; report this explicitly.
- Fail closed for new privileged actions when stop state or authorization cannot be verified.
- Prevent replay, cross-tenant substitution, confused-deputy use, and unauthorized stop requests.
- Make duplicate stop requests safe and idempotent.
- A user stop must not disable logging, monitoring, safety enforcement, operator incident response, or other users' sessions.
- Do not permit an agent to hide, override, reset, or weaken the user's stop control.

## 5. What a successful stop means

The UI/API must not say "stopped" merely because a request was received. It must report distinct, verifiable states:

1. **Received:** authenticated stop request accepted for processing.
2. **Dispatch blocked:** trusted gateway denies new actions for the target scope.
3. **Grants revoked:** relevant credentials, sessions, leases, and delegated grants are revoked or their expiry is confirmed.
4. **Work contained:** queues, scheduled jobs, child agents, and controllable workers are paused/cancelled/isolated.
5. **Side effects reconciled:** known external actions are checked and outstanding effects are reported.
6. **Complete with limitations:** the system confirms the defined stop boundary and lists any external or irreversible action it could not cancel.

The user must see the timestamp, target scope, status, and any remaining work or irreversible effects. If the system cannot verify containment, it must say **stop not verified** and escalate; it must not imply success.

## 6. Recovery and reauthorization

- A stopped task is terminal by default. Starting a new task is a new authorization event.
- Resuming a paused task requires an explicit user action and revalidation of identity, task scope, policy, and grants.
- Revoked credentials must not be silently recreated from cached credentials or parent sessions.
- High-impact or irreversible actions require a fresh approval bound to the exact action and parameters.
- Account-wide stop must not be undone by the agent, an automatic retry, scheduled trigger, or a background workflow.
- Administrative override, where legally and operationally necessary, must be separate, narrowly scoped, time-limited, auditable, and communicated where permitted.

## 7. Failure modes and fallback

- If the agent UI is unresponsive, provide an out-of-band control surface through the authenticated account console or platform API.
- If the user identity provider is unavailable, do not invent a weaker identity path. Provide a documented support/emergency process with verification.
- If the policy gateway is unreachable, deny new privileged actions and queue stop intent durably for reconciliation; never treat an unavailable gateway as authorization to continue.
- If a downstream provider cannot revoke an already-issued token, report the residual exposure and provide provider-specific disconnect/rotation guidance.
- If the control plane itself is compromised, operator incident response and independent infrastructure controls take precedence; user UI alone is not a security boundary.

## 8. Privacy, accessibility, and user trust

Collect only the minimum audit data needed to prove the stop request, authorization decision, propagation, and outcome. Protect audit records from tampering, limit access, define retention/deletion, and avoid exposing other users' data. Provide plain-language explanations without implying that external side effects can always be undone.

A stop control must be usable by people with disabilities and under stress: consistent placement, clear wording, adequate contrast, keyboard operation, assistive-technology labels, and no color-only status communication.

## 9. Minimum acceptance criteria

A user-stop implementation is not ready for production until it demonstrates:

- Stop is independent of model output and available during every active task.
- Stop blocks new privileged actions before acknowledging dispatch-blocked status.
- The request is bound to the authenticated user and correct tenant/task.
- Parent/child agent and delegated grant revocation is complete and independently verified.
- Queues, retries, scheduled work, and callbacks are accounted for.
- Concurrent and duplicate requests are safe.
- Agent attempts to hide or override the control fail.
- Network partitions, stale caches, control-plane outages, and identity-provider failures fail safely.
- UI accurately reports incomplete containment and non-reversible external effects.
- Stopped tasks do not restart without explicit reauthorization.
- Audit, privacy, accessibility, and incident escalation tests pass.

## 10. Conformance language

This is a draft specification. Implementers may state that a product implements selected requirements only when they identify the version, scope, tests, exceptions, and evidence. Passing synthetic fixtures is not legal compliance, security certification, or proof that all external effects can be reversed.

**Attribution:** Original specification authored for the HuffmanRepositories ecosystem by Robert Huffman (MrCakes931). Preserve separate attribution for third-party sources and contributions.
