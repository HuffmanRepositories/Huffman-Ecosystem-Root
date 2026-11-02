# Use-Case Router

| Your question | Start here |
|---|---|
| What is the mission? | [Mission hub](https://github.com/HuffmanRepositories/Open-Source-AI-Independence) |
| How do I navigate the portfolio? | [Ecosystem Guide](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Guide) |
| Can two agent systems map concepts? | [OAC](https://github.com/HuffmanRepositories/Open-Agent-Compatibility) |
| Can I inspect reproducible compatibility examples? | [OAC Fixtures](https://github.com/HuffmanRepositories/Open-Agent-Compatibility-Fixtures) |
| How should run usage be represented? | [OARMI](https://github.com/HuffmanRepositories/Open-Agent-Run-Metrics-Interop) |
| What can memory migration lose? | [P10](https://github.com/HuffmanRepositories/Agent-Memory-Portability-Tests) |
| Can evaluation evidence be manipulated? | [P11](https://github.com/HuffmanRepositories/Agent-Evaluation-Oracle-Integrity-Fixtures) |
| What if a tool call is retried or its outcome is uncertain? | [P12](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures) |
| How should delegated permissions be bounded? | [P13](https://github.com/HuffmanRepositories/Agent-Delegation-Scope-Boundary-Fixtures) |
| How should delegated spending or resource use be bounded? | [P14](https://github.com/HuffmanRepositories/Agent-Delegated-Budget-Enforcement-Fixtures) |
| How should a user independently stop their own agent task? | [P15 reference fixtures](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/tree/main/p15) and [user-stop specification](USER-CONTROLLED-KILLSWITCH.md) |

Choose one starting point. Add another repository only when the task crosses a documented boundary.

## Cross-boundary scenarios — when to consult companion projects

| Scenario | Read together | Why / boundary |
|---|---|---|
| Delegated tool call with uncertain outcome or retry | [P12](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures) + [P13](https://github.com/HuffmanRepositories/Agent-Delegation-Scope-Boundary-Fixtures); add [P15](p15/README.md) if stop/cancellation is involved | P13 describes synthetic authority limits; P12 describes retries/idempotency; P15 describes stop semantics. |
| Delegated task with a spend/resource cap | [P13](https://github.com/HuffmanRepositories/Agent-Delegation-Scope-Boundary-Fixtures) + [P14](https://github.com/HuffmanRepositories/Agent-Delegated-Budget-Enforcement-Fixtures); add P12 if reservation/settlement retries are in scope | Authority and budget accounting are distinct; P14 does not define who is authorized. |
| Cancel/stop a delegated, budgeted task | P13 + P14 + [P15](p15/README.md); add P12 when tool effects may retry or have uncertain outcomes | Stop, grant revocation, budget release, and external-effect reconciliation are separate concerns. |
| Usage metrics versus budget enforcement | [OARMI](https://github.com/HuffmanRepositories/Open-Agent-Run-Metrics-Interop) for usage representation + P14 for budget scenarios | Metrics/usage representation is not billing or a budget enforcement engine. |

These routes are **conditional reading guidance**, not mandatory runtime dependencies. The projects are synthetic/draft research artifacts with independent maturity and limitations. Follow each selected project's README and AGENTS.md before proposing changes; do not infer a live integration from a cross-link.
