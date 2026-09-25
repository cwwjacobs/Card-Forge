#!/usr/bin/env python3
"""Validate the public Card Forge Core skeleton.

This validator intentionally uses only the Python standard library so edge/local
users can run it without installing dependencies. Because no JSON Schema library
is available as a repo dependency, full schema validation is provided by a small
standard-library subset validator (see ``validate_instance``) covering the JSON
Schema keywords used by the schemas in this repository: ``type`` (including
union types), ``required``, ``properties``, ``items``, ``enum``, and
``additionalProperties``.

What is validated:

- required paths and non-empty files
- every Card record against ``schemas/card.schema.json`` (registry JSONL files
  and ``*.card.md`` frontmatter) and every generated Card record against
  ``skills/card-forge-skill/schemas/generated_card.schema.json``
- every Stack record against ``schemas/stack.schema.json`` (parsed from the
  structured Stack Markdown files)
- every Deck record against ``schemas/deck.schema.json`` (parsed from the
  structured Deck Markdown files)
- every Run State record against ``schemas/run.schema.json``, with Run statuses
  restricted to the set defined in ``RUN_STANDARD.md``
- every Run Receipt against ``schemas/receipt.schema.json`` (parsed from the
  Receipt Markdown files; each played Card yields one checkpoint record per
  ``RUN_STANDARD.md``)
- cross-reference integrity: Deck -> Stack -> Card references resolve, and
  Run -> Receipt references resolve (the receipt file exists and declares the
  Run's ``run_id``)

Markdown extraction rules for Receipt records: an absent ``Warnings`` or
``Blockers`` section means none were recorded and maps to an empty list; the
``Outputs created`` / ``Output created`` sections both map to
``output_created``; a ``Card ID`` header field maps to ``card_played`` for
single-Card checkpoint receipts, while a ``Cards played`` table produces one
checkpoint record per row.

The overall validator pass covers repository content only. Functional checks
(the negative-fixture suite under ``tests/negative/``) are run afterwards and
their counts are reported separately from the validator pass. The exit code is
non-zero if either fails.
"""

from __future__ import annotations

import json
import py_compile
import shutil
import sys
import tempfile
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
    "schemas/stack.schema.json",
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

CARD_SCHEMA = "schemas/card.schema.json"
GENERATED_CARD_SCHEMA = "skills/card-forge-skill/schemas/generated_card.schema.json"
STACK_SCHEMA = "schemas/stack.schema.json"
DECK_SCHEMA = "schemas/deck.schema.json"
RUN_SCHEMA = "schemas/run.schema.json"
RECEIPT_SCHEMA = "schemas/receipt.schema.json"

REGISTRY_FILES = [
    "registry/card_registry.jsonl",
    "registry/card_registry.example.jsonl",
    "skills/card-forge-skill/examples/card_registry.example.jsonl",
]

MAIN_REGISTRY = "registry/card_registry.jsonl"

GENERATED_CARD_DIR = "skills/card-forge-skill/examples/expected_outputs/cards"
GENERATED_WORKLIST = "skills/card-forge-skill/examples/expected_outputs/card_index_worklist.jsonl"

STACK_FILES = [
    "stacks/intake_stack.md",
    "stacks/structure_check_stack.md",
    "stacks/repair_planning_stack.md",
    "stacks/readiness_stack.md",
    "examples/edge-runtime-32k/compiled_stack.md",
]

RUN_FILES = [
    "runs/example_run_state.json",
    "runs/examples/ai_build_preflight_run_state.example.json",
    "examples/edge-runtime-32k/run_state.json",
]

RECEIPT_DIRS = [
    "receipts",
    "examples/edge-runtime-32k/receipts",
]

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

# Run statuses defined by RUN_STANDARD.md.
ALLOWED_RUN_STATUSES = {
    "READY",
    "RUNNING",
    "BLOCKED",
    "NEEDS_SOURCE",
    "NEEDS_HUMAN",
    "PASS",
    "PASS_WITH_WARNINGS",
    "FAIL",
}

SCHEMA_FILE_NAMES = [
    "card.schema.json",
    "deck.schema.json",
    "stack.schema.json",
    "run.schema.json",
    "receipt.schema.json",
]


# ---------------------------------------------------------------------------
# JSON Schema subset validation (standard library only)
# ---------------------------------------------------------------------------


def _type_name(instance: Any) -> str:
    if instance is None:
        return "null"
    if isinstance(instance, bool):
        return "boolean"
    if isinstance(instance, int):
        return "integer"
    if isinstance(instance, float):
        return "number"
    if isinstance(instance, str):
        return "string"
    if isinstance(instance, list):
        return "array"
    if isinstance(instance, dict):
        return "object"
    return type(instance).__name__


def _type_matches(instance: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    return False


def validate_instance(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate ``instance`` against the JSON Schema subset used in this repo.

    Supported keywords: ``type`` (string or list of strings), ``enum``,
    ``required``, ``properties``, ``items``, and ``additionalProperties``
    (boolean form). Returns a list of human-readable error strings.
    """
    errors: list[str] = []

    if "type" in schema:
        allowed = schema["type"]
        if isinstance(allowed, str):
            allowed = [allowed]
        if not any(_type_matches(instance, expected) for expected in allowed):
            errors.append(
                f"{path}: expected type {'/'.join(allowed)}, "
                f"got {_type_name(instance)}"
            )
            return errors

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} is not one of {schema['enum']}")

    if isinstance(instance, dict):
        for required_key in schema.get("required", []):
            if required_key not in instance:
                errors.append(f"{path}: missing required property '{required_key}'")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate_instance(value, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: additional property '{key}' is not allowed")

    if isinstance(instance, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(instance):
            errors.extend(validate_instance(item, schema["items"], f"{path}[{index}]"))

    return errors


# ---------------------------------------------------------------------------
# Loading and Markdown helpers
# ---------------------------------------------------------------------------


def load_json(path: Path) -> tuple[Any, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON in {path}: {exc}"
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"


def schema_capability_errors(schema: Any, path: str = "$schema") -> list[str]:
    """Reject schema features this validator would silently ignore.

    Only properties' values and items contain subschemas. Property names and
    annotation/enum payloads are data, even when named like schema keywords.
    """
    if not isinstance(schema, dict):
        return [f"{path}: unsupported schema form (expected an object)"]
    supported = {"type", "enum", "required", "properties", "items", "additionalProperties"}
    annotations = {"$schema", "$id", "$comment", "title", "description", "default", "examples", "deprecated", "readOnly", "writeOnly"}
    errors = [f"{path}: unsupported schema keyword '{key}'"
              for key in schema if key not in supported | annotations]
    if "type" in schema:
        allowed = schema["type"]
        allowed = [allowed] if isinstance(allowed, str) else allowed
        types = {"object", "array", "string", "integer", "number", "boolean", "null"}
        if (not isinstance(allowed, list) or not allowed
                or any(not isinstance(value, str) or value not in types for value in allowed)):
            errors.append(f"{path}.type: unsupported type declaration")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        errors.append(f"{path}.enum: expected a nonempty array")
    if "required" in schema and (not isinstance(schema["required"], list)
            or any(not isinstance(value, str) for value in schema["required"])):
        errors.append(f"{path}.required: expected an array of property names")
    if "additionalProperties" in schema and not isinstance(schema["additionalProperties"], bool):
        errors.append(f"{path}.additionalProperties: only boolean form is supported")
    if "properties" in schema:
        if not isinstance(schema["properties"], dict):
            errors.append(f"{path}.properties: expected an object")
        else:
            for key, child in schema["properties"].items():
                errors.extend(schema_capability_errors(child, f"{path}.properties.{key}"))
    if "items" in schema:
        errors.extend(schema_capability_errors(schema["items"], f"{path}.items"))
    return errors


def load_schema(root: Path, relative: str) -> dict[str, Any]:
    schema, error = load_json(root / relative)
    if error:
        raise RuntimeError(error)
    if not isinstance(schema, dict):
        raise RuntimeError(f"Schema is not a JSON object: {relative}")
    capability_errors = schema_capability_errors(schema, relative)
    if capability_errors:
        raise RuntimeError("; ".join(capability_errors))
    return schema


def strip_ticks(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def header_field(text: str, field: str) -> str | None:
    """Extract ``Field: `value``` style header lines from Markdown."""
    prefix = f"{field}:"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return strip_ticks(stripped[len(prefix):].strip())
    return None


def markdown_sections(text: str) -> dict[str, str]:
    """Split Markdown into a mapping of heading title -> section body.

    The first ``#`` title is stored under the key ``"__title__"``. Section
    keys are the literal heading text (e.g. ``"Cards in order"``).
    """
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            current = title
            if line.startswith("# ") and "__title__" not in sections:
                sections["__title__"] = [title]
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections.setdefault(current, []).append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def section_text(sections: dict[str, str], title: str) -> str | None:
    body = sections.get(title)
    if body is None or not body.strip():
        return None
    return body.strip()


def section_items(sections: dict[str, str], title: str) -> list[str] | None:
    """Extract bullet/numbered list item values from a section.

    Backtick-quoted items are unquoted. Returns ``None`` when the section is
    absent, otherwise the list of item strings (possibly empty).
    """
    body = sections.get(title)
    if body is None:
        return None
    items: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(strip_ticks(stripped[2:].strip()))
        elif stripped[:2].rstrip(".").isdigit() and ". " in stripped:
            items.append(strip_ticks(stripped.split(". ", 1)[1].strip()))
    return items


def section_tick_tokens(sections: dict[str, str], title: str) -> list[str]:
    """Extract the first backtick-quoted token of each list item in a section."""
    body = sections.get(title)
    if body is None:
        return []
    tokens: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("- ") or (stripped[:2].rstrip(".").isdigit() and ". " in stripped)):
            continue
        if "`" in stripped:
            token = stripped.split("`", 2)[1] if stripped.count("`") >= 2 else ""
            if token:
                tokens.append(token)
    return tokens


def parse_cards_played_table(sections: dict[str, str]) -> list[dict[str, str]]:
    """Parse the ``Cards played`` Markdown table into row dicts."""
    body = sections.get("Cards played")
    if body is None:
        return []
    rows: list[dict[str, str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [strip_ticks(cell) for cell in stripped.strip("|").split("|")]
        cells = [cell.strip() for cell in cells]
        if not cells or all(not cell for cell in cells):
            continue
        if cells[0].lower() == "card" or set(cells[0]) <= {"-", ":"}:
            continue
        row = {
            "card": cells[0],
            "status": cells[1] if len(cells) > 1 else "",
            "output": cells[2] if len(cells) > 2 else "",
        }
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Record parsers
# ---------------------------------------------------------------------------


def parse_card_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"
    if not text.startswith("---"):
        return None, f"Missing YAML frontmatter in {path}"

    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, f"Invalid YAML frontmatter in {path}"

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
                return None, f"List item without key in {path}: {line}"
            item = stripped[2:].strip().strip('"').strip("'")
            if current_key not in data:
                data[current_key] = []
            if not isinstance(data[current_key], list):
                return None, f"Mixed list and scalar for {current_key} in {path}"
            data[current_key].append(item)
        else:
            if ": " in line:
                key, value = line.split(": ", 1)
            elif line.endswith(":"):
                key = line[:-1]
                value = ""
            else:
                return None, f"Invalid frontmatter line in {path}: {line}"

            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                data[key] = value
            else:
                data[key] = []

    return data, None


def parse_stack(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"
    sections = markdown_sections(text)

    record: dict[str, Any] = {}
    stack_id = header_field(text, "Stack ID")
    if stack_id:
        record["stack_id"] = stack_id
    title = sections.get("__title__")
    if title:
        record["name"] = title
    for section_title, key in [
        ("Purpose", "purpose"),
        ("Entry condition", "entry_condition"),
        ("Exit condition", "exit_condition"),
        ("Failure route", "failure_route"),
    ]:
        value = section_text(sections, section_title)
        if value is not None:
            record[key] = value
    for section_title, key in [
        ("Cards in order", "cards_in_order"),
        ("Run outputs", "run_outputs"),
        ("Permissions", "permissions"),
    ]:
        items = section_items(sections, section_title)
        if items is not None:
            record[key] = items

    return record, None


def parse_deck(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"
    sections = markdown_sections(text)

    record: dict[str, Any] = {}
    deck_id = header_field(text, "Deck ID")
    if deck_id:
        record["deck_id"] = deck_id
    title = sections.get("__title__")
    if title:
        record["name"] = title
    for section_title, key in [("Purpose", "purpose"), ("Final gate", "final_gate")]:
        value = section_text(sections, section_title)
        if value is not None:
            record[key] = value
    for section_title, key in [
        ("Stacks in order", "stacks_in_order"),
        ("Allowed permissions", "allowed_permissions"),
        ("Run outputs", "run_outputs"),
    ]:
        items = section_items(sections, section_title)
        if items is not None:
            record[key] = items

    draw_pool = section_tick_tokens(sections, "Draw Pool")
    if draw_pool:
        record["draw_pool"] = draw_pool

    return record, None


def parse_receipt(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    """Parse a Run Receipt Markdown file into checkpoint Receipt records.

    Returns (records, info, errors). ``info`` carries the receipt-level header
    fields (run_id, deck_id, stack_id, status) used for cross-reference checks.
    """
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    info: dict[str, Any] = {"path": str(path)}

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return records, info, [f"Cannot read {path}: {exc}"]

    sections = markdown_sections(text)

    run_id = header_field(text, "Run ID")
    status = header_field(text, "Status")
    deck_id = header_field(text, "Deck ID")
    stack_id = header_field(text, "Stack ID")
    card_id = header_field(text, "Card ID")

    if run_id is None:
        errors.append(f"{path}: missing 'Run ID' header field")
        return records, info, errors
    info["run_id"] = run_id
    if deck_id:
        info["deck_id"] = deck_id
    if stack_id:
        info["stack_id"] = stack_id
    if status:
        info["status"] = status

    base: dict[str, Any] = {"run_id": run_id}
    if status is not None:
        base["status"] = status

    input_seen = section_items(sections, "Input seen")
    if input_seen is None:
        errors.append(f"{path}: missing 'Input seen' section")
    else:
        base["input_seen"] = input_seen

    outputs = section_items(sections, "Outputs created")
    if outputs is None:
        outputs = section_items(sections, "Output created")
    if outputs is None:
        errors.append(f"{path}: missing 'Outputs created' section")

    next_action = section_text(sections, "Next action")
    if next_action is None:
        errors.append(f"{path}: missing 'Next action' section")
    else:
        base["next_action"] = next_action

    # An absent Warnings/Blockers section means none were recorded.
    base["warnings"] = section_items(sections, "Warnings") or []
    blockers = section_items(sections, "Blockers")
    if blockers:
        base["blockers"] = blockers

    rows = parse_cards_played_table(sections)
    if rows:
        for row in rows:
            record = dict(base)
            record["card_played"] = row["card"]
            if row["status"]:
                record["status"] = row["status"]
            record["output_created"] = [row["output"]] if row["output"] else []
            records.append(record)
    else:
        if card_id is None:
            errors.append(
                f"{path}: no 'Cards played' table and no 'Card ID' header field"
            )
        else:
            record = dict(base)
            record["card_played"] = card_id
            record["output_created"] = outputs or []
            records.append(record)

    if errors:
        return [], info, errors
    return records, info, errors


# ---------------------------------------------------------------------------
# Repository validation
# ---------------------------------------------------------------------------


def new_stats() -> dict[str, int]:
    return {
        "cards": 0,
        "generated_cards": 0,
        "stacks": 0,
        "decks": 0,
        "runs": 0,
        "receipts": 0,
        "receipt_records": 0,
        "crossrefs": 0,
    }


def validate_repository(root: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    stats = new_stats()

    def err(message: str) -> None:
        errors.append(message)

    # -- required paths -----------------------------------------------------
    for relative_path in REQUIRED_PATHS:
        path = root / relative_path
        if not path.exists():
            err(f"Missing required path: {relative_path}")
        elif path.is_file() and path.stat().st_size == 0:
            err(f"Required file is empty: {relative_path}")

    # -- schema files -------------------------------------------------------
    schemas: dict[str, dict[str, Any]] = {}
    for schema_name in SCHEMA_FILE_NAMES:
        relative = f"schemas/{schema_name}"
        schema, error = load_json(root / relative)
        if error:
            err(error)
            continue
        if not isinstance(schema, dict) or schema.get("type") != "object":
            err(f"Schema does not declare object type: {relative}")
            continue
        if not schema.get("required"):
            err(f"Schema has no required fields: {relative}")
            continue
        schemas[relative] = schema
    generated_schema, gen_error = load_json(root / GENERATED_CARD_SCHEMA)
    if gen_error:
        err(gen_error)
    elif isinstance(generated_schema, dict):
        schemas[GENERATED_CARD_SCHEMA] = generated_schema

    card_schema = schemas.get(CARD_SCHEMA)
    stack_schema = schemas.get(STACK_SCHEMA)
    deck_schema = schemas.get(DECK_SCHEMA)
    run_schema = schemas.get(RUN_SCHEMA)
    receipt_schema = schemas.get(RECEIPT_SCHEMA)
    generated_card_schema = schemas.get(GENERATED_CARD_SCHEMA)

    # -- Card records: registries -------------------------------------------
    main_registry_ids: set[str] = set()
    if card_schema is not None:
        for relative in REGISTRY_FILES:
            path = root / relative
            if not path.exists():
                err(f"Missing required path: {relative}")
                continue
            seen: set[str] = set()
            lines = path.read_text(encoding="utf-8").splitlines()
            if not lines:
                err(f"Card registry is empty: {relative}")
                continue
            for line_number, line in enumerate(lines, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    err(f"Invalid JSONL in {relative} line {line_number}: {exc}")
                    continue
                stats["cards"] += 1
                label = f"{relative} line {line_number}"
                for message in validate_instance(record, card_schema):
                    err(f"{label}: {message}")
                card_id = record.get("card_id") if isinstance(record, dict) else None
                if isinstance(card_id, str):
                    if card_id in seen:
                        err(f"Duplicate card_id in registry: {card_id}")
                    seen.add(card_id)
                    if relative == MAIN_REGISTRY:
                        main_registry_ids.add(card_id)
                status = record.get("status") if isinstance(record, dict) else None
                if status is not None and status not in ALLOWED_CARD_STATUSES:
                    err(f"Invalid status for {card_id}: {status}")

    # -- Card records: *.card.md frontmatter ---------------------------------
    card_file_ids: set[str] = set()
    if card_schema is not None:
        for card_file in sorted(root.rglob("*.card.md")):
            relative = card_file.relative_to(root).as_posix()
            # Skip generated outputs (validated separately against the
            # generated Card schema) and negative-fixture payloads.
            if "expected_outputs" in relative or relative.startswith("tests/"):
                continue
            data, error = parse_card_frontmatter(card_file)
            if error:
                err(error)
                continue
            stats["cards"] += 1
            for message in validate_instance(data, card_schema):
                err(f"{relative}: {message}")
            card_id = data.get("card_id")
            if isinstance(card_id, str):
                card_file_ids.add(card_id)

    # -- Generated Card records (skill examples) ------------------------------
    if generated_card_schema is not None:
        generated_dir = root / GENERATED_CARD_DIR
        if generated_dir.is_dir():
            for card_file in sorted(generated_dir.glob("*.card.md")):
                relative = card_file.relative_to(root).as_posix()
                data, error = parse_card_frontmatter(card_file)
                if error:
                    err(error)
                    continue
                stats["generated_cards"] += 1
                for message in validate_instance(data, generated_card_schema):
                    err(f"{relative}: {message}")
        worklist_path = root / GENERATED_WORKLIST
        if worklist_path.exists():
            seen_generated: set[str] = set()
            for line_number, line in enumerate(
                worklist_path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    err(f"Invalid JSONL in {GENERATED_WORKLIST} line {line_number}: {exc}")
                    continue
                stats["generated_cards"] += 1
                label = f"{GENERATED_WORKLIST} line {line_number}"
                for message in validate_instance(record, generated_card_schema):
                    err(f"{label}: {message}")
                card_id = record.get("card_id") if isinstance(record, dict) else None
                if isinstance(card_id, str):
                    if card_id in seen_generated:
                        err(f"Duplicate card_id in generated worklist: {card_id}")
                    seen_generated.add(card_id)

    card_ids = main_registry_ids | card_file_ids

    # -- Stack records --------------------------------------------------------
    stacks: list[tuple[str, dict[str, Any]]] = []
    if stack_schema is not None:
        for relative in STACK_FILES:
            path = root / relative
            if not path.exists():
                continue
            record, error = parse_stack(path)
            if error:
                err(error)
                continue
            stats["stacks"] += 1
            for message in validate_instance(record, stack_schema):
                err(f"{relative}: {message}")
            stacks.append((relative, record))

    # -- Deck records ---------------------------------------------------------
    decks: list[tuple[str, dict[str, Any]]] = []
    if deck_schema is not None:
        for deck_file in sorted(root.glob("decks/*/deck.md")):
            relative = deck_file.relative_to(root).as_posix()
            record, error = parse_deck(deck_file)
            if error:
                err(error)
                continue
            stats["decks"] += 1
            for message in validate_instance(record, deck_schema):
                err(f"{relative}: {message}")
            decks.append((relative, record))

    # -- Run records ----------------------------------------------------------
    runs: list[tuple[str, dict[str, Any]]] = []
    if run_schema is not None:
        for relative in RUN_FILES:
            path = root / relative
            if not path.exists():
                continue
            record, error = load_json(path)
            if error:
                err(error)
                continue
            stats["runs"] += 1
            for message in validate_instance(record, run_schema):
                err(f"{relative}: {message}")
            if isinstance(record, dict):
                status = record.get("status")
                if status is not None and status not in ALLOWED_RUN_STATUSES:
                    err(
                        f"{relative}: invalid Run status {status!r} "
                        f"(allowed: {', '.join(sorted(ALLOWED_RUN_STATUSES))})"
                    )
                runs.append((relative, record))

    # -- Receipt records ------------------------------------------------------
    receipts: dict[str, dict[str, Any]] = {}
    if receipt_schema is not None:
        for receipt_dir in RECEIPT_DIRS:
            directory = root / receipt_dir
            if not directory.is_dir():
                continue
            for receipt_file in sorted(directory.rglob("*.md")):
                relative = receipt_file.relative_to(root).as_posix()
                text = receipt_file.read_text(encoding="utf-8")
                if header_field(text, "Run ID") is None:
                    # Not a Run Receipt record (e.g. approval receipts).
                    continue
                records, info, parse_errors = parse_receipt(receipt_file)
                stats["receipts"] += 1
                for message in parse_errors:
                    err(message)
                for record in records:
                    stats["receipt_records"] += 1
                    for message in validate_instance(record, receipt_schema):
                        err(f"{relative}: {message}")
                receipts[relative] = {
                    "info": info,
                    "cards_played": [r.get("card_played") for r in records],
                }

    # -- Cross-reference integrity --------------------------------------------
    stack_ids = {r.get("stack_id") for _, r in stacks}
    stack_names = {r.get("name") for _, r in stacks}
    deck_ids = {r.get("deck_id") for _, r in decks}

    def resolve(value: Any, known: set[Any], kind: str, source: str) -> None:
        stats["crossrefs"] += 1
        if value not in known:
            err(f"{source}: dangling {kind} reference: {value}")

    for relative, record in decks:
        for stack_name in record.get("stacks_in_order", []):
            resolve(stack_name, stack_names, "Stack", relative)
        for card_id in record.get("draw_pool", []):
            resolve(card_id, card_ids, "Card", f"{relative} draw pool")

    for relative, record in stacks:
        for card_id in record.get("cards_in_order", []):
            resolve(card_id, card_ids, "Card", relative)

    for relative, record in runs:
        resolve(record.get("deck_id"), deck_ids, "Deck", relative)
        resolve(record.get("current_stack"), stack_ids, "Stack", relative)
        resolve(record.get("current_card"), card_ids, "Card", relative)
        receipt_path = record.get("receipt_path")
        stats["crossrefs"] += 1
        if not isinstance(receipt_path, str) or not (root / receipt_path).exists():
            err(f"{relative}: points to missing receipt: {receipt_path}")
        elif receipt_path not in receipts:
            err(f"{relative}: receipt {receipt_path} is not a parseable Run Receipt")
        elif receipts[receipt_path]["info"].get("run_id") != record.get("run_id"):
            err(
                f"{relative}: receipt {receipt_path} declares Run ID "
                f"{receipts[receipt_path]['info'].get('run_id')!r}, "
                f"expected {record.get('run_id')!r}"
            )

    for relative, receipt in receipts.items():
        for card_id in receipt["cards_played"]:
            resolve(card_id, card_ids, "Card", relative)

    # -- Python script compile health ------------------------------------------
    skill_script = root / "skills/card-forge-skill/scripts/card_forge_skill.py"
    if skill_script.exists():
        try:
            py_compile.compile(str(skill_script), doraise=True)
        except py_compile.PyCompileError as exc:
            err(f"Python compile failed for skills/card-forge-skill/scripts/card_forge_skill.py: {exc}")

    return errors, stats


# ---------------------------------------------------------------------------
# Negative fixture suite (functional checks)
# ---------------------------------------------------------------------------


def run_negative_fixtures(root: Path) -> tuple[list[dict[str, Any]], str | None]:
    """Run every fixture under ``tests/negative/`` against a mutated copy of
    the repository and assert that validation rejects it.

    Each fixture directory holds a ``manifest.json``:

    .. code-block:: json

        {
          "description": "what this fixture breaks",
          "replacements": {"repo/relative/target": "payload-file-in-fixture"},
          "expect_error": "substring expected in the validator errors"
        }

    Returns (results, suite_error). Each result is a dict with ``name``,
    ``description``, ``passed``, and ``detail``.
    """
    fixtures_root = root / "tests" / "negative"
    if not fixtures_root.is_dir():
        return [], f"negative fixture directory missing: {fixtures_root}"

    results: list[dict[str, Any]] = []
    for case_dir in sorted(fixtures_root.iterdir()):
        if not case_dir.is_dir():
            continue
        name = case_dir.name
        manifest_path = case_dir / "manifest.json"
        result: dict[str, Any] = {
            "name": name,
            "description": "",
            "passed": False,
            "detail": "",
        }
        results.append(result)
        if not manifest_path.exists():
            result["detail"] = "missing manifest.json"
            continue
        manifest, error = load_json(manifest_path)
        if error or not isinstance(manifest, dict):
            result["detail"] = error or "manifest is not a JSON object"
            continue
        result["description"] = manifest.get("description", "")
        replacements = manifest.get("replacements", {})
        expect_error = manifest.get("expect_error")

        with tempfile.TemporaryDirectory() as temporary:
            mutated_root = Path(temporary) / "repo"
            shutil.copytree(
                root,
                mutated_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            for target, payload in replacements.items():
                payload_path = case_dir / payload
                if not payload_path.exists():
                    result["detail"] = f"missing payload file: {payload}"
                    break
                target_path = mutated_root / target
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(payload_path, target_path)
            else:
                validation_errors, _ = validate_repository(mutated_root)
                if not validation_errors:
                    result["detail"] = "mutated repository was not rejected"
                elif expect_error and not any(
                    expect_error in message for message in validation_errors
                ):
                    result["detail"] = (
                        f"expected error containing {expect_error!r}, got: "
                        + " | ".join(validation_errors)
                    )
                else:
                    result["passed"] = True
                    result["detail"] = validation_errors[0]
    return results, None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    exit_code = 0

    errors, stats = validate_repository(ROOT)
    for message in errors:
        print(f"FAIL: {message}", file=sys.stderr)

    if errors:
        print(
            f"FAIL: Card Forge core validation failed with {len(errors)} error(s).",
            file=sys.stderr,
        )
        exit_code = 1
    else:
        print("PASS: Card Forge core validation completed.")
        print(
            "  Records validated against full schemas: "
            f"{stats['cards']} cards, {stats['generated_cards']} generated cards, "
            f"{stats['stacks']} stacks, {stats['decks']} decks, "
            f"{stats['runs']} runs, "
            f"{stats['receipt_records']} receipt checkpoint records "
            f"from {stats['receipts']} receipts."
        )
        print(f"  Cross-references checked: {stats['crossrefs']}.")

    fixture_results, suite_error = run_negative_fixtures(ROOT)
    passed = sum(1 for result in fixture_results if result["passed"])
    failed = len(fixture_results) - passed
    for result in fixture_results:
        if not result["passed"]:
            print(
                f"FAIL: negative fixture {result['name']}: {result['detail']}",
                file=sys.stderr,
            )
    if suite_error:
        print(f"FAIL: {suite_error}", file=sys.stderr)
        exit_code = 1
    print(
        f"Functional checks (negative fixtures, reported separately from the "
        f"validator pass): {passed} passed, {failed} failed."
    )
    if failed or suite_error:
        exit_code = 1

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
