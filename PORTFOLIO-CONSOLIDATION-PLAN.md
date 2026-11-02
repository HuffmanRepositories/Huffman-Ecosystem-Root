# Portfolio Consolidation and Alignment Plan

**Status:** Active portfolio-wide audit plan  
**Scope:** 14 repositories currently visible under the HuffmanRepositories account (12 public, 2 private). The public ecosystem catalog excludes private repositories.  
**Goal:** Keep every repository discoverable, current, security-reviewed, directionally aligned, and explicit about required companion components—without falsely presenting research/fixtures as production systems.

## Operating principles

1. **One public source of truth:** this root owns the public ecosystem routing, catalog, maturity overview, cross-repository dependency map, validation matrix, and integration-level evidence.
2. **Repository ownership:** each repository owns its specification, README, tests, license, SECURITY.md, contribution guidance, release/maturity claims, and local agent instructions.
3. **No false completeness:** a green fixture test is evidence about the fixture/model only; it is not proof of production enforcement, interoperability, safety, security, or certification.
4. **Progressive discovery:** AI agents read root routing first, then the selected project and explicitly required companions. Never ingest all repos by default.
5. **Public/private separation:** public index files must not reveal private repo contents, paths, issue details, or implementation specifics.
6. **Dependency completeness:** if a task requires multiple components, each project's README and agent instructions must identify the companions, exact purpose, required version/maturity, and validation route.
7. **Push verification:** a task is complete only after commit SHA is visible on the intended branch, remote contents match, and relevant CI has completed. Local or tool-generated edits alone are not completion.
8. **Human approvals:** branch protection, account security, releases, license/governance changes, destructive actions, visibility changes, and risky merges require owner/admin approval.

## Repository sweep order

### Wave 0 — Portfolio inventory and evidence
- Enumerate repositories, visibility, default branch, archived status, latest commit, open/closed/merged PRs, releases, workflows, and current CI.
- Reconcile the count against the account listing; keep private repositories in the private audit only.
- Produce an evidence ledger with date, exact repository/ref, commit SHA, workflow URL/status, tests, limitations, and unresolved owner actions.

### Wave 1 — Root / master alignment
- Validate README, PROJECT-CATALOG, ECOSYSTEM-MAP, ecosystem.json, AGENT-ROUTER.json, START-HERE, USE-CASE-ROUTER, AGENTS.md, security/maturity matrix, and cross-repository test matrix.
- Ensure each public project appears exactly once with correct purpose, status, route, and dependencies.
- Check all links and JSON validity; eliminate stale repo counts, old test totals, outdated maturity claims, and broken paths.
- Make Root the coordination index—not a duplicate implementation or authority over project-local specs.

### Wave 2 — Discovery and coordination
1. HuffmanRepositories profile: concise discovery entrypoint and root/guide links.
2. Open-Source-AI-Independence: mission, governance/coordination, handshake, and cross-project contribution direction.
3. Huffman-Ecosystem-Guide: newcomer path, architecture, project selection, maturity distinctions, and contribution journey.
4. OAC: protocol/mapping research and version boundaries.
5. OAC Fixtures: concrete synthetic examples, explicitly dependent on OAC schema/version.

### Wave 3 — Technical project review
Review each in sequence, updating its local README and agent guidance, then root catalog/matrix:
- OARMI — run metrics/usage interoperability; clarify it is not billing infrastructure.
- P10 — memory portability; identify migration/format companions where needed.
- P11 — evaluation/oracle integrity; identify benchmark/evaluator dependencies.
- P12 — retries/idempotency; explain links to P13 authorization, P14 budget accounting, and P15 stop semantics when the scenario spans them.
- P13 — delegated scope/authority; explain P12 dispatch/retry and P14 budget dependencies.
- P14 — delegated budgets; link P13 authority and P12 idempotent accounting where applicable.
- P15 (root) — stop semantics and synthetic seam model; link P12/P13/P14 but clearly distinguish reference model from production integration.

### Wave 4 — Cross-project integration and directional graph
For every pair of claimed dependencies:
- Document producer/consumer and interface/artifact.
- Specify schema/version and compatible maturity.
- Add a small synthetic integration test where appropriate.
- Add an explicit negative statement for unsupported/absent integration.
- Maintain a graph with edges labeled **required**, **recommended**, or **related** (not imply dependency merely from thematic relevance).
- A project task must discover its companion pieces via README/AGENTS/manifest and root router, not by guessing repo names.

### Wave 5 — AI/agent instruction files (all repositories)
Check presence and correctness of:
- AGENTS.md (or documented alternative)
- README agent/discovery section
- root router/manifest references (public repos only)
- project-specific preflight, dependency expansion, safety/authority boundaries, tests, and handoff
- no prompt-injection-like repository instructions that override user/system policy
- no stale references to renamed repos, branches, or private workspaces

Use a shared template, but preserve local specificity. Avoid copying root AGENTS wholesale into every project; link to it and add local rules. Do not include private repo routes in public files.

### Wave 6 — Security and quality gates
For each repo:
- inspect source, workflows, dependency manifests, action pins, permissions, secrets handling, generated artifacts, and commit history where supported;
- run project validators/tests and current CI;
- review CodeQL, dependency alerts, secret scanning, push protection, Dependabot, license and SECURITY.md;
- distinguish scanner pass, scanner unavailable, disabled, skipped, and “no alert data” states;
- check branch protection/rulesets and required checks (owner/admin settings);
- verify no credentials, private data, or sensitive details in public docs;
- record remediation and rerun evidence.
This is a layered repository review, not a guarantee that all vulnerabilities or production risks are found.

### Wave 7 — PRs, releases, and remote verification
- Triage each PR: security/dependency update, docs, bug, feature, stale, or duplicate.
- Inspect diff, tests, CI, and mergeability. Merge only when scope is understood, checks are green, and policy permits; otherwise request changes or leave open.
- Do not close PRs merely to reduce counts. Do not force-push or bypass protection.
- Verify every change landed on the expected branch and re-check latest CI.
- Release only when project maturity, versioning, provenance, changelog, and user approval are ready.

## Per-repository completion checklist

- [ ] Correct name, purpose, audience, scope and “not for” boundaries
- [ ] README explains use, quick start, project status, upstream/downstream/companion links
- [ ] Project spec and schema versions agree with tests and fixtures
- [ ] AI/agent instructions are present, local, safe, and route to required companions
- [ ] LICENSE, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT (if adopted) and citation/provenance are accurate
- [ ] Tests/validators are reproducible; expected outcomes and limitations are stated
- [ ] CI/workflows use least privilege, maintained actions, pinned versions where policy requires
- [ ] Secret/dependency/code scanning states recorded (including unavailable/disabled)
- [ ] Open PRs, releases, issues, discussions and branch rules reviewed
- [ ] Public links and root catalog/router references validated
- [ ] Latest commit is pushed to intended branch; CI rerun and status recorded
- [ ] Root evidence ledger/catalog/maturity matrix updated

## Required output for each wave

A dated report with: repos/files inspected; commits pushed; PRs reviewed and decisions; test/scanner status with links; mismatches fixed; unresolved items and their owners; exact next step. No “all done” claim while any checklist item remains unverified.

## Current known starting point (2026-11-02)

- Account snapshot: 14 repositories; 12 public and 2 private.
- Earlier PR baseline: 22. Nine additional PRs merged in the 2026-11-02 continuation (Blueprint #4; P12 #3/#4; P13 #4/#5; P14 #4/#5/#6; Root #1). Current observed total: 31 closed/merged, 0 open; verify canonical per-repo PR metadata for future updates.
- Root P15 map/router consistency requires ongoing check: ecosystem map should include P15 and indicate synthetic P12–P15 seam coverage only.
- Branch API evidence: main is unprotected for all 14 repos; public ruleset API returns zero rulesets for all 12 public repos. Private Blueprint/Archive ruleset reads are blocked (403). Owner/admin follow-up remains for enabling branch protections/rulesets, account 2FA/recovery, native security-alert/push-protection settings, and restore-drill evidence.
