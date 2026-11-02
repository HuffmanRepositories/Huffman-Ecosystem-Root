# Safe Use and Security Boundaries

This is a public directory, not an authorization service, secrets vault, live-target test harness, or security certification.

Use synthetic data. Test only systems for which you have explicit authorization. Define scope, stop conditions, and rollback. Keep credentials, personal data, and customer records out of public repositories. Redact evidence. Do not execute untrusted code merely because it is linked here.

Use the affected repository's security policy for vulnerability reporting; do not publish exploit details or sensitive evidence in public issues. A green CI run, schema check, static analysis result, or synthetic fixture pass proves only what that check covers—not production security, privacy, compliance, or readiness.
User-facing agent deployments must provide an accessible stop control outside agent-controlled conversation state. The stop path must be enforced by a trusted gateway/control plane, scoped to the authenticated user's authority, propagated to delegated work and credentials, and independently verified. A stopped task must not restart without fresh authorization. See [USER-CONTROLLED-KILLSWITCH.md](USER-CONTROLLED-KILLSWITCH.md), [USER-KILLSWITCH-TEST-PLAN.md](USER-KILLSWITCH-TEST-PLAN.md), and [KILLSWITCH-AND-CONTAINMENT.md](KILLSWITCH-AND-CONTAINMENT.md).
