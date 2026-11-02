# USI Draft Package

This folder contains early, review-only artifacts for Universal Semantic Interoperability (USI).

- [USI 0.1 semantic contract](USI-0.1-SEMANTIC-CONTRACT.md)
- [Draft message-envelope JSON Schema](schemas/usi-envelope.schema.json)
- [Tool invocation payload schema](schemas/usi-tool-invoke-payload.schema.json)
- [Result payload schema](schemas/usi-result-payload.schema.json)
- [Stop request payload schema](schemas/usi-stop-payload.schema.json)\n- [Capabilities response payload schema](schemas/usi-capabilities-payload.schema.json)\n- [Stop acknowledgement payload schema](schemas/usi-stop-ack-payload.schema.json)\n- [Envelope golden vectors](fixtures/usi-envelope-vectors.json)

## Current state

**Draft only.** This is not a released standard, production API, SDK, validator, or security certification. The envelope schema checks only the outer message shape; it does not validate operation-specific payloads, authorization, or semantics.

## Suggested next steps

1. Review and approve scope, terminology, license, and governance.
2. Stabilize envelope and versioning rules.
3. Add operation-specific schemas for capabilities, tool invocation, result, and stop.
4. Add valid/invalid golden vectors and a reference validator.
5. Implement Python and TypeScript bindings against the same tests.
6. Conduct independent interoperability and security review before release claims.

Do not deploy this draft to control production tools or agents.
