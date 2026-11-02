#!/usr/bin/env python3
"""Run USI draft envelope golden vectors with JSON Schema Draft 2020-12.

Install: python -m pip install -r usi/requirements.txt
Run:     python usi/tools/validate_vectors.py
This validates envelope shape only—not operation semantics, authorization, or security.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "usi-envelope.schema.json"
VECTORS_PATH = ROOT / "fixtures" / "usi-envelope-vectors.json"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    vectors = json.loads(VECTORS_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    failures: list[str] = []
    for vector in vectors.get("valid", []):
        errors = list(validator.iter_errors(vector["message"]))
        if errors:
            failures.append(
                f'VALID vector {vector["name"]} rejected: '
                + "; ".join(error.message for error in errors)
            )

    for vector in vectors.get("invalid", []):
        errors = list(validator.iter_errors(vector["message"]))
        if not errors:
            failures.append(f'INVALID vector {vector["name"]} unexpectedly accepted')

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    valid_count = len(vectors.get("valid", []))
    invalid_count = len(vectors.get("invalid", []))
    print(f"USI envelope vectors: PASS ({valid_count} valid, {invalid_count} invalid)")
    print("Scope: envelope JSON Schema only; no semantic or security assurance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
