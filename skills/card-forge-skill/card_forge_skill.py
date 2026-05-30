#!/usr/bin/env python3
"""Card Forge Skill helper.

Scan an old repo, folder, or source bundle and emit multiple generated Cards.

This script is intentionally heuristic and standard-library only. It creates a
first-pass generated Card set for model/operator review. It does not
index Cards and does not build Card Stacks or Decks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yml",
    ".yaml",
    ".html",
    ".css",
    ".sh",
    ".toml",
}

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".cache",
}

TYPE_RULES = [
    ("Contract Card", ["must not", "do not", "never", "claim boundary", "overclaim", "rule", "permission"]),
    ("Gate Card", ["pass", "fail", "gate", "ready", "not ready", "needs human", "approval"]),
    ("Receipt Card", ["receipt", "record", "log", "proof", "evidence"]),
    ("Code Card", ["validate", "scan", "script", "function", "command", "pytest", "json", "dependency", "run"]),
    ("Prompt Card", ["prompt", "instruction", "ask the model", "llm", "claude", "chatgpt"]),
    ("Template Card", ["template", "format", "fill", "shape"]),
    ("Adapter Card", ["convert", "transform", "map", "extract", "parse"]),
    ("Check Card", ["check", "verify", "detect", "find", "inspect", "audit"]),
]


@dataclass(frozen=True)
class GeneratedCard:
    card_id: str
    name: str
    type: str
    input: str
    move: str
    output: str
    done_when: str
    stop_if: str
    receipt: str
    permissions: str
    risk_level: str
    token_size: str
    source_origin: str
    source_file: str


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:64] or "generated_card"


def card_prefix(card_type: str) -> str:
    return card_type.split()[0].lower()


def read_text_safely(path: Path, max_chars: int = 12000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def iter_source_files(source: Path) -> Iterable[Path]:
    if source.is_file():
        if source.suffix.lower() in TEXT_EXTENSIONS:
            yield source
        return

    for path in source.rglob("*"):
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def classify_card_type(text: str, path: Path) -> str:
    haystack = f"{path.name}\n{text}".lower()
    for card_type, needles in TYPE_RULES:
        if any(needle in haystack for needle in needles):
            return card_type
    return "Action Card"


def infer_name(text: str, path: Path, card_type: str) -> str:
    lines = [line.strip("# -*\t") for line in text.splitlines() if line.strip()]
    for line in lines[:20]:
        if 4 <= len(line) <= 70 and not line.startswith("{"):
            cleaned = re.sub(r"[`*_]+", "", line).strip()
            if cleaned:
                return cleaned[:70]
    stem = path.stem.replace("_", " ").replace("-", " ").title()
    suffix = card_type.replace(" Card", "")
    if suffix.lower() not in stem.lower():
        return f"{stem} {suffix}"
    return stem


def infer_move(card_type: str, path: Path, text: str) -> str:
    file_hint = path.name
    if card_type == "Contract Card":
        return f"Apply the boundary or rule described in {file_hint} to the current Run output."
    if card_type == "Gate Card":
        return f"Evaluate the current Run state using the gate criteria described in {file_hint}."
    if card_type == "Receipt Card":
        return f"Record the Run evidence using the receipt pattern described in {file_hint}."
    if card_type == "Code Card":
        return f"Inspect or validate the relevant code/source behavior represented by {file_hint}."
    if card_type == "Prompt Card":
        return f"Use the reusable instruction pattern from {file_hint} with the current source material."
    if card_type == "Template Card":
        return f"Fill the reusable template pattern from {file_hint} for the current Run."
    if card_type == "Adapter Card":
        return f"Convert the current input into the output shape represented by {file_hint}."
    if card_type == "Check Card":
        return f"Check the current source material for the condition represented by {file_hint}."
    return f"Perform the bounded workflow move represented by {file_hint}."


def make_generated_card(path: Path, source_root: Path) -> GeneratedCard:
    text = read_text_safely(path)
    card_type = classify_card_type(text, path)
    name = infer_name(text, path, card_type)
    short = slugify(name)
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:6]
    card_id = f"{card_prefix(card_type)}.{short}.{digest}.v0_1"
    source_origin = str(path.relative_to(source_root)) if source_root.is_dir() else path.name
    move = infer_move(card_type, path, text)

    risk = "medium" if card_type in {"Contract Card", "Gate Card", "Code Card"} else "low"
    permission = "read_only"
    if card_type == "Gate Card":
        permission = "human_required"

    return GeneratedCard(
        card_id=card_id,
        name=name,
        type=card_type,
        input="Relevant source material, Run state, and any prior receipts needed to play this Card.",
        move=move,
        output=f"{slugify(name)}_output.md",
        done_when="The bounded move has produced its stated output or a stop condition has been recorded.",
        stop_if="Required input is missing, private material appears, or the move expands beyond one Card-sized action.",
        receipt=f"Record source file, decision, output path, warnings, blockers, and next action for {card_id}.",
        permissions=permission,
        risk_level=risk,
        token_size="small",
        source_origin=source_origin,
        source_file=source_origin,
    )


def card_markdown(card: GeneratedCard) -> str:
    return f"""# {card.name}

Card ID: `{card.card_id}`
Type: {card.type}
Status: candidate

## Input

{card.input}

## Move

{card.move}

## Output

`{card.output}`

## Done When

{card.done_when}

## Stop If

{card.stop_if}

## Receipt

{card.receipt}

## Permissions

`{card.permissions}`

## Risk Level

{card.risk_level}

## Token Size

{card.token_size}

## Source Origin

{card.source_origin}
"""


def registry_record(card: GeneratedCard) -> dict[str, object]:
    return {
        "card_id": card.card_id,
        "name": card.name,
        "type": card.type,
        "status": "candidate",
        "input": card.input,
        "move": card.move,
        "output": card.output,
        "done_when": card.done_when,
        "stop_if": card.stop_if,
        "receipt": card.receipt,
        "permissions": card.permissions,
        "used_in_decks": [],
        "risk_level": card.risk_level,
        "token_size": card.token_size,
        "source_origin": card.source_origin,
    }


def write_outputs(cards: list[GeneratedCard], out_dir: Path, source: Path) -> None:
    cards_dir = out_dir / "cards"
    receipts_dir = out_dir / "receipts"
    cards_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    registry_path = out_dir / "registry_card_generated.jsonl"
    with registry_path.open("w", encoding="utf-8") as registry_file:
        for card in cards:
            card_path = cards_dir / f"{card.card_id}.card.md"
            card_path.write_text(card_markdown(card), encoding="utf-8")
            registry_file.write(json.dumps(registry_record(card), ensure_ascii=False) + "\n")

    receipt_lines = [
        "# Card Forge Extraction Receipt",
        "",
        f"Source: `{source}`",
        f"Cards emitted: {len(cards)}",
        "",
        "## Generated Cards",
        "",
    ]
    for card in cards:
        receipt_lines.extend(
            [
                f"### `{card.card_id}` — {card.name}",
                "",
                f"- Type: {card.type}",
                f"- Source: `{card.source_origin}`",
                f"- Boundary decision: valid generated Card size",
                f"- Why it qualifies: bounded, repeatable, playable, and receiptable as a first-pass generated Card.",
                "",
            ]
        )

    receipt_lines.extend(
        [
            "## Next Action",
            "",
            "Review generated Cards before adding them to your local Card index. Only operator-approved Cards should be indexed for MCP use.",
        ]
    )
    (receipts_dir / "card_forge_extraction_receipt.md").write_text("\n".join(receipt_lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract generated Cards from a repo or source folder.")
    parser.add_argument("--source", required=True, help="Repo, folder, or file to scan.")
    parser.add_argument("--out", default="_card_forge_out", help="Output directory.")
    parser.add_argument("--limit", type=int, default=50, help="Maximum generated Cards to emit.")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")

    files = list(iter_source_files(source))[: args.limit]
    cards = [make_generated_card(path, source if source.is_dir() else source.parent) for path in files]

    if not cards:
        raise SystemExit("No text source files found to extract generated Cards from.")

    out_dir = Path(args.out).expanduser().resolve()
    write_outputs(cards, out_dir, source)
    print(f"PASS: emitted {len(cards)} generated Cards to {out_dir}")


if __name__ == "__main__":
    main()
