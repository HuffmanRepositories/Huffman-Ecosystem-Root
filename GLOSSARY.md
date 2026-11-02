# Glossary and Acronym Register

This defines portfolio-specific terms, not every ordinary word. Add entries when a term has specialized meaning or affects interpretation.

| Term | Definition | Use case |
|---|---|---|
| Agent | Software that performs tasks using model reasoning, tools, or delegation. | Identify the actor. |
| Agent handshake | Declared workflow for identity claims, capabilities, scope, approval, work, reporting, and closeout. | Coordinate work; not authentication. |
| Compatibility | Documented relationship between features of two systems, including transformations, constraints, losses, and evidence. | Assess interoperability. |
| Conformance | Satisfaction of stated requirements under a defined test method and scope. | Make bounded claims. |
| Delegation | Assignment of bounded work or authority to another actor. | Review child-agent boundaries. |
| Evidence | Information supporting a claim, with source, context, and limitations. | Separate observation from assumption. |
| Fixture | Small, controlled, reproducible input and expected outcome. | Make edge cases inspectable. |
| Idempotency | Operation contract where repeating an identified operation does not create additional unintended effects. | Review retry behavior. |
| Interoperability | Ability of distinct systems to exchange information or coordinate under stated conditions. | Identify integration needs. |
| Oracle | Independent source of truth used to judge an evaluation outcome. | Review scorer integrity. |
| Portability | Transfer of data/behavior while preserving specified meaning and metadata. | Review migration. |
| Provenance | Origin, authorship, version, transformations, and custody record. | Preserve attribution. |
| Scope | Permitted targets, data, actions, time, and authority. | Prevent unapproved work. |
| Synthetic data | Artificial data that does not reproduce real personal/customer records. | Safe fixture authoring. |
| Unknown outcome | Operation may have taken effect, but caller lacks evidence to know. | Avoid blind retries. |
| Validation | A defined check of structure or selected rules. | State exactly what was checked. |

## Acronyms
- HAH — Huffman Agent Handshake (proposed coordination workflow).
- HAV — Huffman Archive Verification (private archive versioning; private details are excluded).
- OAC — Open Agent Compatibility.
- OARMI — Open Agent Run Metrics Interop.
- P10 — Agent Memory Portability Tests.
- P11 — Agent Evaluation Oracle Integrity Fixtures.
- P12 — Agent Tool Retry Idempotency Fixtures.
- P13 — Agent Delegation Scope Boundary Fixtures.
- P14 — Agent Delegated Budget Enforcement Fixtures.
- E0–E4 — OAC evidence levels; the OAC methodology is authoritative.

Expand acronyms on first use. Preserve official project names and schema keys. Do not silently redefine terms; record deprecated aliases.