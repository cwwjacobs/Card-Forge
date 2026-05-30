#!/usr/bin/env python3
"""Validate the public Card Forge Core skeleton.

This validator intentionally uses only the Python standard library so edge/local
users can run it without installing dependencies.
"""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "START_HERE.md",
    "LICENSE",
    "CLAIM_BOUNDARY.md",
    "CARD_STANDARD.md",
    "CARD_STACK_STANDARD.md",
    "DECK_STANDARD.md",
    "RUN_STANDARD.md",
    "registry/card_registry.jsonl",
    "registry/card_index.md",
    "registry/card_registry.example.jsonl",
    "registry/card_binder.example.md",
    "templates/card_template.md",
    "templates/card.md",
    "templates/deck_template.md",
    "templates/run_receipt_template.md",
    "decks/ai-build-preflight/deck.md",
    "runs/examples/ai_build_preflight_run_state.example.json",
    "runs/example_run_state.json",
    "receipts/examples/ai_build_preflight_receipt.example.md",
    "receipts/example_receipt.md",
    "schemas/card.schema.json",
    "schemas/deck.schema.json",
    "schemas/run.schema.json",
    "schemas/receipt.schema.json",
    "skills/card-forge-skill/SKILL.md",
    "skills/card-forge-skill/README.md",
    "skills/card-forge-skill/MANIFEST.md",
    "skills/card-forge-skill/scripts/card_forge_skill.py",
    "skills/card-forge-skill/schemas/generated_card.schema.json",
    "skills/card-forge-skill/examples/card_registry.example.jsonl",
    "skills/card-forge-skill/examples/tiny_source/README.md",
]

REQUIRED_CARD_FIELDS = {
    "card_id",
    "name",
    "type",
    "status",
    "input",
    "move",
    "output",
    "done_when",
    "stop_if",
    "receipt",
    "permissions",
    "risk_level",
    "token_size",
    "source_origin",
}

REQUIRED_RUN_FIELDS = {
    "run_id",
    "deck_id",
    "current_stack",
    "current_card",
    "status",
    "inputs",
    "outputs",
    "next_action",
    "receipt_path",
}

ALLOWED_CARD_STATUSES = {
    "raw",
    "cut",
    "forged",
    "deprecated",
    "rejected",
    "generated",
    "reviewed",
    "trusted",
    "indexed",
}

ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}
ALLOWED_TOKEN_SIZES = {"small", "medium", "large"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_path(relative_path: str) -> Path:
    path = ROOT / relative_path
    if not path.exists():
        fail(f"Missing required path: {relative_path}")
    if path.is_file() and path.stat().st_size == 0:
        fail(f"Required file is empty: {relative_path}")
    return path


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def parse_card_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail(f"Missing YAML frontmatter in {path.relative_to(ROOT)}")

    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"Invalid YAML frontmatter in {path.relative_to(ROOT)}")

    frontmatter = parts[1].strip()
    data: dict[str, Any] = {}
    current_key: str | None = None

    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        stripped = line.lstrip()
        if stripped.startswith("- "):
            if current_key is None:
                fail(f"List item without key in {path.relative_to(ROOT)}: {line}")
            item = stripped[2:].strip().strip('"').strip("'")
            if current_key not in data:
                data[current_key] = []
            if not isinstance(data[current_key], list):
                fail(f"Mixed list and scalar for {current_key} in {path.relative_to(ROOT)}")
            data[current_key].append(item)
        else:
            if ": " in line:
                key, value = line.split(": ", 1)
            elif line.endswith(":"):
                key = line[:-1]
                value = ""
            else:
                fail(f"Invalid frontmatter line in {path.relative_to(ROOT)}: {line}")

            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                data[key] = value
            else:
                data[key] = []

    return data


def validate_card_file(path: Path) -> None:
    data = parse_card_frontmatter(path)

    missing = REQUIRED_CARD_FIELDS - set(data)
    if missing:
        fail(
            f"{path.relative_to(ROOT)} missing required Card fields: "
            + ", ".join(sorted(missing))
        )

    risk = data.get("risk_level")
    if risk and risk not in ALLOWED_RISK_LEVELS:
        fail(f"{path.relative_to(ROOT)} invalid risk_level: {risk}")

    token = data.get("token_size")
    if token and token not in ALLOWED_TOKEN_SIZES:
        fail(f"{path.relative_to(ROOT)} invalid token_size: {token}")

    if "permissions" not in data:
        fail(f"{path.relative_to(ROOT)} missing permissions")

    if "source_origin" not in data:
        fail(f"{path.relative_to(ROOT)} missing source_origin")


def validate_registry(path: Path) -> None:
    seen: set[str] = set()
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        fail("Card registry is empty")

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSONL in {path.relative_to(ROOT)} line {line_number}: {exc}")

        missing = REQUIRED_CARD_FIELDS - set(record)
        if missing:
            fail(
                f"Registry line {line_number} missing required Card fields: "
                + ", ".join(sorted(missing))
            )

        card_id = record["card_id"]
        if card_id in seen:
            fail(f"Duplicate card_id in registry: {card_id}")
        seen.add(card_id)

        status = record.get("status")
        if status not in ALLOWED_CARD_STATUSES:
            fail(f"Invalid status for {card_id}: {status}")

        risk = record.get("risk_level")
        if risk and risk not in ALLOWED_RISK_LEVELS:
            fail(f"Invalid risk_level for {card_id}: {risk}")

        token = record.get("token_size")
        if token and token not in ALLOWED_TOKEN_SIZES:
            fail(f"Invalid token_size for {card_id}: {token}")


def validate_schema_file(path: Path) -> None:
    schema = load_json(path)
    if schema.get("type") != "object":
        fail(f"Schema does not declare object type: {path.relative_to(ROOT)}")
    if not schema.get("required"):
        fail(f"Schema has no required fields: {path.relative_to(ROOT)}")


def validate_run_state(path: Path) -> None:
    run_state = load_json(path)
    missing = REQUIRED_RUN_FIELDS - set(run_state)
    if missing:
        fail(
            f"Run state {path.relative_to(ROOT)} missing fields: "
            + ", ".join(sorted(missing))
        )

    receipt_path = run_state.get("receipt_path")
    if receipt_path and not (ROOT / receipt_path).exists():
        fail(
            f"Run state {path.relative_to(ROOT)} points to missing receipt: {receipt_path}"
        )


def validate_python_script(path: Path) -> None:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        fail(f"Python compile failed for {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    for relative_path in REQUIRED_PATHS:
        require_path(relative_path)

    validate_registry(ROOT / "registry/card_registry.jsonl")
    validate_registry(ROOT / "registry/card_registry.example.jsonl")

    for schema_name in [
        "card.schema.json",
        "deck.schema.json",
        "run.schema.json",
        "receipt.schema.json",
    ]:
        validate_schema_file(ROOT / "schemas" / schema_name)

    validate_run_state(ROOT / "runs/examples/ai_build_preflight_run_state.example.json")
    validate_run_state(ROOT / "runs/example_run_state.json")
    validate_python_script(ROOT / "skills/card-forge-skill/scripts/card_forge_skill.py")

    for card_file in ROOT.rglob("*.card.md"):
        # Skip generated outputs inside expected_outputs since they are examples
        if "expected_outputs" in str(card_file):
            continue
        validate_card_file(card_file)

    print("PASS: Card Forge core validation completed.")


if __name__ == "__main__":
    main()
