# Security Policy

## Scope

This repository contains public ecosystem documentation, schemas, and synthetic reference fixtures. It is not a hosted agent runtime or production emergency-stop service.

## Reporting a vulnerability

Please do not publish credentials, exploit details, personal information, or sensitive reproduction data in a public issue.

If GitHub Private Vulnerability Reporting is enabled for this repository, use the repository's **Security → Advisories → Report a vulnerability** workflow. If that option is unavailable, contact the maintainer through the GitHub account profile and request a private disclosure channel. Include only the minimum information needed to reproduce and assess the issue.

## Response expectations

Reports will be triaged based on severity, reproducibility, affected scope, and available evidence. No response-time or remediation guarantee is implied. Coordinate public disclosure with the maintainer and affected upstream projects.

## Safe testing

- Use synthetic identifiers and data only.
- Never commit real tokens, credentials, private keys, or customer data.
- Test destructive behavior only in isolated, authorized environments.
- Do not interpret passing fixtures or CI as proof of production security.

Maintainer: Robert Huffman (MrCakes931).
