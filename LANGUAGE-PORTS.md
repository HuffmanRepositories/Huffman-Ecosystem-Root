# Programming-Language Ports and Adapters

Keep specifications and fixtures language-neutral. A port should implement or consume the same canonical contract, not redefine it.

Initial priorities: Python, TypeScript/JavaScript, Rust, Go, Java, C#, C/C++, Ruby, PHP, Swift, Kotlin, PowerShell, and Bash. Additional languages are welcome. This is not an exhaustive list of GitHub-supported languages.

Do not generate every port at once. Add a language directory only when there is a real use case, maintainer, build instructions, shared-fixture tests, dependency policy, and review. Untested generated code creates false confidence.

Each port must document canonical spec/version, supported and unsupported behavior, build/use instructions, tests, dependencies, security notes, maintainers, provenance, and license compatibility.

Contributions involving C/C++, assembly, bytecode, disassembly, or reverse-engineering tools must be limited to lawful, authorized interoperability, debugging, preservation, or security research. No malware, credential theft, evasion, unauthorized exploitation, or access-control bypass instructions.

New language proposal: state users, use case, canonical contract, tests, maintainer, and license compatibility; begin with a small proof of concept.