# Final owner handoff checklist — 2026-11-02

Status: Repository automation and documentation have advanced. The following work requires owner access, a real integration environment, or maintainer/legal decisions. This is not certification.

## 1. GitHub account and repository settings
- [ ] Verify account 2FA and recovery-code storage.
- [ ] Review account credentials, tokens, SSH/deploy keys, OAuth grants, and app installations; remove unused or unknown access.
- [ ] Review collaborators and private repository access.
- [ ] Configure branch rulesets for main: PR review, required CI, prevent force-push/deletion, and minimal bypass.
- [ ] Review each repository Security tab: dependency alerts, secret scanning, CodeQL/code scanning, and dependency review. Triage actual findings.
- [ ] Set About descriptions, topics, and homepage links using [repository metadata](REPOSITORY-ABOUT-METADATA.md); verify saved live fields.
- [ ] Set profile pins and create/populate the account Projects board; keep private items private.

## 2. Real P15 and cross-system integration
- [ ] Select isolated staging with disposable identities, tenants, and provider test accounts.
- [ ] Execute BAD-05 through BAD-08 from [the catastrophic failure and recovery plan](DISASTER-RECOVERY-AND-CATASTROPHIC-FAILURE-EXERCISE.md); capture test version, timestamps, expected/actual, logs, and cleanup.
- [ ] Run multi-process/multi-host stop-resume races, duplicate delivery, stale-state, retry, and TOCTOU tests.
- [ ] Test real queue/provider cancellation, delegated grant revocation, and integration credential invalidation; record late side-effect limitations.
- [ ] Verify identity/control-plane outage behavior fails closed.
- [ ] Test stop UI integrity, keyboard/screen-reader/mobile/high-contrast accessibility.
- [ ] Integrate external audit storage; test permissions, retention, tamper detection, restore, and sensitive-data minimization.
- [ ] Restore from backup and reconcile external effects. Turn failures into issues, fix, and rerun.

## 3. USI conformance and governance
- [ ] Add operation-specific payload validators for capabilities, invoke, result, stop, acknowledgement, and errors.
- [ ] Define errors, deadlines, cancellation, version negotiation, and unknown-field behavior.
- [ ] Add language-neutral vectors and two independent implementations (e.g. Python and TypeScript) with CI cross-checks.
- [ ] Obtain independent review of semantic contract and threat model.
- [ ] Decide governance, license, naming/trademark, versioning, and change process.

## 4. Release gate
- [ ] Required CI green on exact release commit.
- [ ] Security findings triaged; high/critical findings fixed or formally accepted with rationale.
- [ ] Real integration/recovery evidence attached to [tracker issue #2](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/issues/2); label synthetic evidence separately.
- [ ] Verify READMEs, About metadata, license, security policy, changelog, versions, and cross-repo links.
- [ ] Review artifacts, provenance/signing, and compatibility notes.
- [ ] Obtain maintainer approval before publishing any release/tag.

## CI evidence recorded
- [USI envelope CI](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41527557594)
- [P15 synthetic tests](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41527669286)
- [Secret scan](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41527669358)
- [CodeQL](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/actions/runs/41527669344)

These runs prove only their specific workflow scope, not production security, provider cancellation, native GitHub alerts status, disaster recovery, or release readiness.
