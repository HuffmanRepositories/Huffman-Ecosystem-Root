# USI 0.1 — Normative Semantic Contract (Draft)

**Status:** Working draft. Not a finalized standard, stable API, production runtime, or certification.  
**Date:** 2026-11-02  
**Companion:** [Architecture proposal](../UNIVERSAL-SEMANTIC-INTEROPERABILITY-PROPOSAL.md)

This document begins the normative contract for the Universal Semantic Interoperability (USI) proposal. “MUST”, “MUST NOT”, “SHOULD”, “SHOULD NOT”, and “MAY” are used in their conventional RFC-style sense. Because this is an early draft, requirements remain subject to maintainer review.

## 1. Scope

USI defines language-neutral operation semantics and a portable message envelope. It does not define a particular transport, runtime, AI model, or user interface.

Initial operation families:

- `usi.capabilities` — describe supported operations and constraints.
- `usi.tool.invoke` — request a tool/action execution.
- `usi.result` — represent success or failure.
- `usi.agent.stop` — request stop/cancellation of a run.
- `usi.memory.export` — request a portable memory export (future MVP candidate; sensitive by nature).

A conformant implementation MUST declare exactly which operations and contract versions it supports. This draft does not require all listed operations to be implemented.

## 2. Versioning and identifiers

- The draft contract identifier is `usi/0.1`.
- Operation identifiers are lowercase, stable, ASCII strings in reverse-domain-like namespace form: `usi.capabilities`, `usi.tool.invoke`, etc.
- Operation IDs, field names, enum values, and machine error codes MUST NOT be localized.
- A message MUST include `spec` and `operation`.
- Breaking semantic changes require a new major contract version. Additive optional fields may be introduced only if old implementations can safely ignore them.
- Unknown required features MUST cause an explicit error; implementations MUST NOT silently pretend they support them.
- Unknown optional fields MAY be ignored if doing so cannot change security or operation semantics.

## 3. Portable envelope

The initial encoding is JSON. A message MUST be a JSON object with these fields:

| Field | Required | Meaning |
|---|---|---|
| `spec` | yes | Contract identifier, e.g. `usi/0.1` |
| `operation` | yes | Stable operation ID |
| `request_id` | yes | Caller-generated opaque correlation identifier |
| `issued_at` | no | RFC 3339 timestamp in UTC |
| `deadline` | no | Absolute RFC 3339 UTC deadline |
| `locale` | no | BCP 47 language tag for human-facing text |
| `trace` | no | Non-sensitive trace metadata |
| `payload` | operation-dependent | Operation data |

Implementations MUST reject malformed required fields, invalid types, and invalid operation payloads. A request ID is for correlation, not authorization, idempotency, or proof of identity.

### JSON parsing rules

- UTF-8 encoding is required for interchange.
- Duplicate object keys MUST be rejected by conformant strict parsers.
- Non-finite numbers (NaN, Infinity) MUST be rejected.
- Numeric ranges and precision MUST be defined by the operation schema; receivers MUST reject values outside them.
- Security-sensitive identifiers and monetary/budget values MUST NOT rely on floating-point rounding.
- Canonical JSON byte representation is not yet specified in 0.1. Implementations MUST NOT assume raw JSON byte equality means semantic equality.

## 4. Capability declaration — `usi.capabilities`

### Request

```json
{
  "spec": "usi/0.1",
  "operation": "usi.capabilities",
  "request_id": "cap-req-01",
  "payload": {}
}
```

### Response payload

```json
{
  "contract_versions": ["usi/0.1"],
  "operations": [
    {
      "id": "usi.tool.invoke",
      "version": "0.1",
      "status": "experimental",
      "constraints": {
        "max_payload_bytes": 65536
      }
    }
  ],
  "features": [],
  "limits": {}
}
```

The responder MUST list only operations it actually supports. `status` values are `experimental`, `supported`, or `deprecated`. A capability response is informational and MUST NOT be treated as authentication, authorization, attestation, or proof that a remote implementation is trustworthy.

## 5. Tool invocation — `usi.tool.invoke`

### Payload

```json
{
  "tool_id": "vendor.namespace.tool",
  "arguments": {},
  "idempotency_key": "optional-client-key",
  "authorization_context": {
    "scope_ref": "opaque-reference"
  }
}
```

Requirements:

- `tool_id` MUST be a stable, namespaced identifier selected from a trusted/authorized tool registry.
- `arguments` MUST conform to the tool's separately declared schema.
- A receiver MUST authorize the caller, tool, arguments, and requested side effects before execution.
- The message itself MUST NOT grant authority. A `scope_ref` is a reference to external authorization state, not a bearer credential by default.
- Tool calls with side effects SHOULD use an idempotency key. The receiver MUST document key scope, retention, and replay behavior.
- Retries MUST NOT be assumed safe unless the tool's idempotency semantics are declared.
- The receiver MUST enforce its own resource, timeout, and budget limits.

This draft does not standardize tool discovery, credential transport, or vendor-specific tool schemas.

## 6. Result — `usi.result`

### Payload

```json
{
  "request_id": "req-01",
  "status": "success",
  "result": {},
  "error": null
}
```

`status` MUST be one of `success`, `failure`, or `partial`.

Failure example:

```json
{
  "request_id": "req-01",
  "status": "failure",
  "result": null,
  "error": {
    "code": "usi.permission_denied",
    "message": {
      "text": "The requested action is not permitted.",
      "language": "en"
    },
    "retryable": false
  }
}
```

- Machine-readable `error.code` MUST be stable and nonlocalized.
- Human-readable message text MAY be localized.
- `retryable` is advisory; clients MUST still apply their own retry policy and MUST NOT retry side effects blindly.
- Implementations MUST NOT return secrets, credentials, or sensitive internal data in errors.

## 7. Stop request — `usi.agent.stop`

### Payload

```json
{
  "run_id": "opaque-run-id",
  "reason_code": "user_requested",
  "requested_by": "opaque-principal-reference"
}
```

Requirements:

- A stop request MUST be authenticated and authorized against the target run and principal.
- `run_id` MUST identify the intended run within the receiver's declared namespace.
- `reason_code` is a stable machine enum; human-readable reason text is optional and localizable.
- The receiver MUST return an explicit acknowledgement state: `accepted`, `already_stopped`, `not_found`, or `denied`.
- `accepted` means the stop request was accepted for processing, not necessarily that every external side effect has already ceased.
- Implementations MUST document stop propagation limits, timeout behavior, and handling of in-flight side effects.
- A stop message MUST NOT be treated as a substitute for access revocation, process isolation, or independent emergency controls.

## 8. Localization and human text

- `locale` and message `language` fields SHOULD use BCP 47 language tags.
- Machine operation IDs, error codes, schema property names, authorization scopes, and enum values MUST NOT be translated.
- Human text SHOULD retain its source language when translation is uncertain or legally/safety significant.
- Localization MUST NOT change authorization, policy, or operation selection.
- Translation provenance and review metadata belong in catalog/resource files, not in machine operation IDs.

## 9. Security requirements

- Receivers MUST validate schema, authorization, policy, resource limits, and operation-specific preconditions independently.
- A valid schema MUST NOT imply that a request is safe or authorized.
- Implementations MUST fail closed for missing required authorization or unsupported required security features.
- Credentials MUST NOT be embedded in example payloads, logs, fixtures, or error messages.
- Logs SHOULD minimize personal and sensitive data and define retention/access controls.
- Implementations MUST protect against replay where replay could cause harmful or duplicate side effects.
- Version negotiation MUST NOT silently downgrade security requirements.
- Adapter claims are not trust proofs; deployments need separate identity, trust, and integrity mechanisms.

## 10. Conformance claim

A conformant implementation MUST:
1. identify its contract version and supported operation set;
2. validate envelope and operation payloads;
3. preserve stable IDs and declared semantics;
4. reject malformed or unsupported required behavior explicitly;
5. implement relevant authorization and security requirements;
6. pass the versioned test suite for each claimed operation;
7. publish known limitations and any lossy mappings.

Passing conformance tests does not imply secure deployment, regulatory compliance, production readiness, or interoperability with undeclared features.

## 11. Open issues for 0.1 review

- Canonical JSON profile and Unicode normalization policy.
- Request/result correlation and async lifecycle.
- Exact error registry and operation schemas.
- Capability negotiation and downgrade prevention.
- Stop acknowledgement model and in-flight effects.
- Authentication, identity, and authorization profiles (likely separate specs).
- Memory export consent, privacy, and data minimization.
- Formal license, governance, and specification change process.

## 12. Status

This is a first contract draft for discussion. Do not use it as a production API or make compatibility/certification claims until versioned schemas, test vectors, review, and governance are approved.
