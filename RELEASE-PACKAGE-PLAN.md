# Release Package Plan and Candidate Manifest

**Maintainer:** Robert Huffman (MrCakes931)  
**Prepared:** 2026-11-02  
**Status:** Candidate plan — NOT a published release

## Release strategy

The ecosystem is a collection of independently versioned research, documentation, and synthetic-fixture projects. Do not create one falsely uniform version number across projects with different maturity and license terms.

### Candidate milestone

- Portfolio milestone label: `Huffman Ecosystem Baseline 2026-11`
- Suggested release channel: `pre-release` / research baseline
- No GitHub Release, signed tag, downloadable release asset, or production deployment has been issued by this plan.
- No final release date or version should be assigned until the maintainer approves licensing and project maturity.

## Candidate public release inventory

| Repository | Proposed package scope | Release condition |
|---|---|---|
| `HuffmanRepositories` | Profile / discovery README snapshot | License and attribution review |
| `Open-Source-AI-Independence` | Mission and coordination docs | Confirm license and doc status |
| `Huffman-Ecosystem-Guide` | Human onboarding docs | Confirm docs license and links |
| `Huffman-Ecosystem-Root` | Ecosystem directory, routing, P15 reference model | License decision; latest CI green; package provenance |
| `Open-Agent-Compatibility` | Compatibility research/spec | Versioned spec, schema compatibility policy |
| `Open-Agent-Compatibility-Fixtures` | Compatibility test fixtures | Fixture schema/version mapping |
| `Open-Agent-Run-Metrics-Interop` | Metrics interoperability research | Schema version and fixture validation |
| `Agent-Memory-Portability-Tests` | Memory portability/privacy fixtures | Privacy review and fixture versioning |
| `Agent-Evaluation-Oracle-Integrity-Fixtures` | Evaluation-integrity fixtures | Versioned fixture catalog |
| `Agent-Tool-Retry-Idempotency-Fixtures` | Retry/idempotency fixtures | Semantic contract and versioned tests |
| `Agent-Delegation-Scope-Boundary-Fixtures` | Delegation-scope fixtures | Semantic validator and CI green |
| `Agent-Delegated-Budget-Enforcement-Fixtures` | Delegated-budget fixtures | Semantic validator and CI green |

Private Blueprint and Archive repositories are excluded from public release bundles.

## Required release package contents

Each repository release should include:
1. Source snapshot or GitHub-generated source archive.
2. Exact version tag and immutable commit SHA.
3. Release notes: scope, maturity, breaking changes, known limitations, validation evidence.
4. `SHA256SUMS` for uploaded artifacts, verified independently.
5. SPDX/license and third-party notice files after license review.
6. SBOM (CycloneDX or SPDX) for repositories that package executable code or dependencies.
7. Test/CI links and any skipped or manual tests clearly identified.
8. Provenance: repository URL, commit, build workflow, build timestamp, maintainer.
9. A statement that fixture/spec validation is not production security certification.

## Pre-release checklist

- [ ] Maintainer confirms licensing for profile, guide, root, and mission hub.
- [ ] Review contributor ownership, copied materials, third-party notices, and trademarks.
- [ ] Verify all project version identifiers and schema compatibility relationships.
- [ ] Confirm all latest workflow runs are successful (not merely older green runs).
- [ ] Perform comprehensive link checks, dependency review, and secret-history scan.
- [ ] Review issues, discussions, PRs, release notes, and known limitations.
- [ ] Verify GitHub branch rules, Actions permissions, secret scanning, CodeQL alerts, and account security.
- [ ] Apply descriptions, homepages, topics, and pins through GitHub UI/API with suitable permissions.
- [ ] Build reproducible release archives and generate SHA-256 checksums.
- [ ] Publish GitHub Releases with explicit pre-release flag if appropriate.
- [ ] Confirm downloads, checksums, signatures/provenance, and release links after publication.

## Explicit exclusions

Do not publish:
- Private Blueprint or Archive contents.
- Real credentials, private configuration, personal data, or operational logs.
- An assertion that the user-controlled kill switch is deployed. P15 is a synthetic reference model.
- Claims of legal compliance, security certification, or production readiness without independent evidence.

## Approval

This is a release preparation checklist, not authorization to apply a license or publish release artifacts. Maintainer approval and the remaining release gates are required.
