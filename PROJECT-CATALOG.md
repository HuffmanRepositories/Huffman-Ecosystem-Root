# Public Project Catalog

| Project | Purpose | Not for |
|---|---|---|
| [HuffmanRepositories](https://github.com/HuffmanRepositories/HuffmanRepositories) | Portfolio discovery | Technical implementation |
| [Open-Source-AI-Independence](https://github.com/HuffmanRepositories/Open-Source-AI-Independence) | Mission and coordination | Production agent runtime |
| [Huffman-Ecosystem-Guide](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Guide) | Human onboarding | Replacement for specifications |
| [Open-Agent-Compatibility](https://github.com/HuffmanRepositories/Open-Agent-Compatibility) | Version-scoped compatibility mapping | Proof of runtime interoperability |
| [OAC Fixtures](https://github.com/HuffmanRepositories/Open-Agent-Compatibility-Fixtures) | Synthetic compatibility cases | Live conformance suite |
| [OARMI](https://github.com/HuffmanRepositories/Open-Agent-Run-Metrics-Interop) | Usage/accounting representation | Billing engine |
| [P10](https://github.com/HuffmanRepositories/Agent-Memory-Portability-Tests) | Memory migration/loss cases | Universal memory protocol |
| [P11](https://github.com/HuffmanRepositories/Agent-Evaluation-Oracle-Integrity-Fixtures) | Evaluation/oracle integrity | Benchmark certification |
| [P12](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures) | Retry and uncertain outcomes | Exactly-once guarantee |
| [P13](https://github.com/HuffmanRepositories/Agent-Delegation-Scope-Boundary-Fixtures) | Delegated authority boundaries | Authorization engine |
| [P14](https://github.com/HuffmanRepositories/Agent-Delegated-Budget-Enforcement-Fixtures) | Delegated budget scenarios | Production budget manager |
| P15 (in this root) | User-stop reference model, USTOP scenario tests, and synthetic P12–P15 seam harness | Deployed kill switch, production control plane, or true cross-service integration |

## Cross-cutting security workstream

The [User-Controlled Emergency Stop specification](USER-CONTROLLED-KILLSWITCH.md) defines the user-facing stop contract. Its [verification plan](USER-KILLSWITCH-TEST-PLAN.md) is now accompanied by an executable [P15 in-memory reference model and test suite](p15/README.md). The tests are synthetic and do not establish real identity, credential, queue, integration, UI, or runtime enforcement. Operator containment remains defined in [KILLSWITCH-AND-CONTAINMENT.md](KILLSWITCH-AND-CONTAINMENT.md).

The mission hub coordinates direction; the Ecosystem Guide teaches navigation; OAC defines mapping methodology; OAC Fixtures provides reproducible examples; OARMI handles usage representation; P10–P15 address distinct agent reliability topics. Private workspaces are excluded.
