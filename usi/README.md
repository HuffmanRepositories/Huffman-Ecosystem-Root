# USI Draft Package

This folder contains early, review-only artifacts for Universal Semantic Interoperability (USI).

- [USI 0.1 semantic contract](USI-0.1-SEMANTIC-CONTRACT.md)
- [Draft message-envelope JSON Schema](schemas/usi-envelope.schema.json)
- [Tool invocation payload schema](schemas/usi-tool-invoke-payload.schema.json)
- [Result payload schema](schemas/usi-result-payload.schema.json)
- [Stop request payload schema](schemas/usi-stop-payload.schema.json)
- [Capabilities response payload schema](schemas/usi-capabilities-payload.schema.json)
- [Stop acknowledgement payload schema](schemas/usi-stop-ack-payload.schema.json)
- [Envelope golden vectors](fixtures/usi-envelope-vectors.json)\n- [Python envelope vector validator](tools/validate_vectors.py)\n- [Validator dependency](requirements.txt)

## Current state

**Draft only.** This is not a released standard, production API, SDK, or security certification. A small Python envelope-vector validator now exists; it is not a complete USI runtime or semantic validator. The envelope schema checks only the outer message shape; it does not validate operation-specific payloads, authorization, or semantics.

## Suggested next steps

1. Review and approve scope, terminology, license, and governance.
2. Stabilize envelope and versioning rules.
3. Complete operation-specific schemas and review lifecycle/error semantics.
4. Run the Python golden-vector validator: `python -m pip install -r usi/requirements.txt && python usi/tools/validate_vectors.py`.
5. Implement Python and TypeScript bindings against shared conformance tests.
6. Conduct independent interoperability and security review before release claims.

Do not deploy this draft to control production tools or agents.
