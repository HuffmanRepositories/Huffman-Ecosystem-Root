# Huffman Ecosystem Root
### The official public front door to the HuffmanRepositories ecosystem

**Created and directed by Robert Huffman (MrCakes931)**

Welcome. This repository is the primary locator, onboarding path, and navigation system for the public HuffmanRepositories ecosystem. A person or AI agent who discovers one project should be able to find the wider portfolio, understand each project's distinct purpose, and choose a safe next step.

> **Do not ingest everything at once.** Discover the whole ecosystem, then work through one relevant project at a time.


> **Portfolio maturity:** Open research, documentation, and synthetic test fixtures. This repository is the canonical directory and coordination front door—not a unified production agent runtime. Individual projects define their own maturity and validation limits; no ecosystem-wide certification or production release is claimed.

## Start here
0. Current ecosystem status: [Resumption status (2026-11-02)](RESUMPTION-STATUS-2026-11-02.md), [failure-test execution log](FAILURE-TEST-EXECUTION-LOG-2026-11-02.md), [Release-readiness review](RELEASE-READINESS-REVIEW.md), [release package plan](RELEASE-PACKAGE-PLAN.md), and [security policy](SECURITY.md).
1. Humans: [START-HERE.md](START-HERE.md).
2. AI agents: [AGENTS.md](AGENTS.md), then parse [ecosystem.json](ecosystem.json) and [AGENT-ROUTER.json](AGENT-ROUTER.json).
3. Project selection: [PROJECT-CATALOG.md](PROJECT-CATALOG.md) and [USE-CASE-ROUTER.md](USE-CASE-ROUTER.md).
4. Definitions: [GLOSSARY.md](GLOSSARY.md).
5. Contributions, translations, and ports: [CONTRIBUTING.md](CONTRIBUTING.md), [LOCALIZATION.md](LOCALIZATION.md), [LANGUAGE-PORTS.md](LANGUAGE-PORTS.md).
6. Safety engineering: [USER-CONTROLLED-KILLSWITCH.md](USER-CONTROLLED-KILLSWITCH.md), [USER-KILLSWITCH-TEST-PLAN.md](USER-KILLSWITCH-TEST-PLAN.md), [P15 reference fixtures and tests](p15/README.md), [KILLSWITCH-AND-CONTAINMENT.md](KILLSWITCH-AND-CONTAINMENT.md), [ROGUE-AGENT-INCIDENT-RESPONSE.md](ROGUE-AGENT-INCIDENT-RESPONSE.md), and [SAFE-USE-AND-SECURITY.md](SAFE-USE-AND-SECURITY.md), and [catastrophic failure / disaster recovery exercise](DISASTER-RECOVERY-AND-CATASTROPHIC-FAILURE-EXERCISE.md).
7. Legal and compliance issue-spotting: [COMPLIANCE-AND-LEGAL-REVIEW.md](COMPLIANCE-AND-LEGAL-REVIEW.md). This is not legal advice or a compliance certification.
8. Repository descriptions and topics: [REPOSITORY-ABOUT-METADATA.md](REPOSITORY-ABOUT-METADATA.md).

## Public projects
- [HuffmanRepositories](https://github.com/HuffmanRepositories/HuffmanRepositories) — portfolio discovery.
- [Open-Source-AI-Independence](https://github.com/HuffmanRepositories/Open-Source-AI-Independence) — mission and coordination.
- [Huffman-Ecosystem-Guide](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Guide) — human onboarding.
- [Open-Agent-Compatibility](https://github.com/HuffmanRepositories/Open-Agent-Compatibility) — compatibility mapping.
- [Open-Agent-Compatibility-Fixtures](https://github.com/HuffmanRepositories/Open-Agent-Compatibility-Fixtures) — reproducible compatibility fixtures.
- [Open-Agent-Run-Metrics-Interop](https://github.com/HuffmanRepositories/Open-Agent-Run-Metrics-Interop) — run metrics and accounting.
- [Agent-Memory-Portability-Tests](https://github.com/HuffmanRepositories/Agent-Memory-Portability-Tests) — memory portability (P10).
- [Agent-Evaluation-Oracle-Integrity-Fixtures](https://github.com/HuffmanRepositories/Agent-Evaluation-Oracle-Integrity-Fixtures) — evaluation integrity (P11).
- [Agent-Tool-Retry-Idempotency-Fixtures](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures) — retries and idempotency (P12).
- [Agent-Delegation-Scope-Boundary-Fixtures](https://github.com/HuffmanRepositories/Agent-Delegation-Scope-Boundary-Fixtures) — delegation boundaries (P13).
- [Agent-Delegated-Budget-Enforcement-Fixtures](https://github.com/HuffmanRepositories/Agent-Delegated-Budget-Enforcement-Fixtures) — delegated budgets (P14).

P15 is currently a reference-fixture package inside this root repository, not a separate repository or production service. The [P15 README](p15/README.md) documents its scope and limitations.

Private workspaces are intentionally omitted from this public directory.

## Progressive discovery
| Stage | Goal | Read |
|---|---|---|
| 0 | Orient | README, START-HERE |
| 1 | Map | PROJECT-CATALOG, ECOSYSTEM-MAP |
| 2 | Select | USE-CASE-ROUTER |
| 3 | Learn | Selected project's README, START-HERE, AGENTS |
| 4 | Extend | CONTRIBUTING, LOCALIZATION, LANGUAGE-PORTS |

This is a directory, not a monolithic software package. Each project owns its specifications, tests, releases, license, security policy, and maturity claims. A passing fixture validator does not prove production conformance or security.

## Validation
Run the P15 synthetic reference tests from the repository root:

```bash
python -m unittest discover -s p15 -p 'test_*.py' -v
```

GitHub Actions runs the same tests on pushes and pull requests. This validates the in-memory reference model only; it does not deploy or verify a live emergency-stop service.

If this directory helps, consider starring it. Fork and reuse responsibly: preserve applicable license and attribution notices, identify modifications, retain upstream provenance, and do not imply that a fork is official or endorsed.

**Created by Robert Huffman (MrCakes931).** See GOVERNANCE.md and PROVENANCE-AND-REUSE.md.
