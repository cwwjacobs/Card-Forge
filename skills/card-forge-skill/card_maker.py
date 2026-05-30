#!/usr/bin/env python3
"""Card Maker: check generated Cards against the existing Card registry.

Reads generated Cards (e.g. from Card Forge Skill output) and the existing
Card registry. Emits a duplicate report and a review worklist. Does NOT
auto-approve or auto-index without operator consent.

This script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
}


@dataclass(frozen=True)
class CardRecord:
    card_id: str
    name: str
    card_type: str
    status: str
    move: str
    output: str
    source_origin: str
    raw: dict[str, Any]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSONL in {path} line {line_number}: {exc}")
        records.append(record)
    return records


def validate_record(record: dict[str, Any], source: str) -> None:
    missing = REQUIRED_CARD_FIELDS - set(record)
    if missing:
        fail(f"{source} missing required Card fields: {', '.join(sorted(missing))}")


def to_card(record: dict[str, Any]) -> CardRecord:
    return CardRecord(
        card_id=record.get("card_id", ""),
        name=record.get("name", ""),
        card_type=record.get("type", ""),
        status=record.get("status", ""),
        move=record.get("move", ""),
        output=record.get("output", ""),
        source_origin=record.get("source_origin", ""),
        raw=record,
    )


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


@dataclass
class DuplicateFinding:
    generated: CardRecord
    existing: CardRecord
    reasons: list[str]


@dataclass
class ReviewCandidate:
    card: CardRecord
    warnings: list[str]


def find_duplicates(generated: list[CardRecord], existing: list[CardRecord]) -> list[DuplicateFinding]:
    findings: list[DuplicateFinding] = []
    existing_by_id = {c.card_id: c for c in existing}
    existing_by_name = {normalize(c.name): c for c in existing if normalize(c.name)}

    for gen in generated:
        reasons: list[str] = []
        matched: CardRecord | None = None

        if gen.card_id in existing_by_id:
            matched = existing_by_id[gen.card_id]
            reasons.append("exact card_id match")

        norm_name = normalize(gen.name)
        if norm_name and norm_name in existing_by_name:
            matched = existing_by_name[norm_name]
            if "exact name match" not in reasons:
                reasons.append("exact name match")

        if matched:
            norm_gen_move = normalize(gen.move)
            norm_match_move = normalize(matched.move)
            if norm_gen_move and norm_gen_move == norm_match_move:
                if "same move text" not in reasons:
                    reasons.append("same move text")

            findings.append(DuplicateFinding(generated=gen, existing=matched, reasons=reasons))

    return findings


def find_review_candidates(
    generated: list[CardRecord],
    existing: list[CardRecord],
    duplicate_findings: list[DuplicateFinding],
) -> list[ReviewCandidate]:
    duplicate_ids = {f.generated.card_id for f in duplicate_findings}
    existing_norm_names = {normalize(c.name) for c in existing}
    existing_norm_moves = {normalize(c.move) for c in existing}
    review_candidates: list[ReviewCandidate] = []

    for gen in generated:
        if gen.card_id in duplicate_ids:
            continue
        warnings: list[str] = []
        norm_name = normalize(gen.name)
        norm_move = normalize(gen.move)

        if norm_name and any(norm_name in en or en in norm_name for en in existing_norm_names if en):
            warnings.append("name overlaps with existing indexed Card")
        if norm_move and any(norm_move in em or em in norm_move for em in existing_norm_moves if em):
            warnings.append("move text overlaps with existing indexed Card")
        if not gen.name or len(gen.name) < 3:
            warnings.append("name is too short")
        if not gen.move or len(gen.move) < 10:
            warnings.append("move is too short")
        if gen.status != "candidate":
            warnings.append(f"status is '{gen.status}', expected 'candidate' (newly generated)")

        review_candidates.append(ReviewCandidate(card=gen, warnings=warnings))

    return review_candidates


def write_duplicate_report(findings: list[DuplicateFinding], out_path: Path) -> None:
    lines = [
        "# Card Maker Duplicate Report",
        "",
        f"Duplicates found: {len(findings)}",
        "",
        "This report lists generated Cards that appear to already exist in the existing Card registry.",
        "",
        "## Operator instruction",
        "",
        "Review each finding. If the generated Card is truly a duplicate, discard it. If it is a variant, rename or differentiate the move/output before indexing.",
        "",
    ]

    for i, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"### {i}. `{finding.generated.card_id}`",
                "",
                f"- Generated Card name: `{finding.generated.name}`",
                f"- Existing match: `{finding.existing.card_id}` (`{finding.existing.name}`)",
                f"- Reasons: {', '.join(finding.reasons)}",
                f"- Generated Card source: `{finding.generated.source_origin}`",
                "",
            ]
        )

    if not findings:
        lines.append("No duplicates detected.")
        lines.append("")

    lines.extend(
        [
            "## Claim boundary",
            "",
            "This report uses heuristics. It does not guarantee completeness. A generated Card flagged as duplicate may be a valid variant, and a generated Card not flagged may still overlap semantically.",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_review_worklist(reviews: list[ReviewCandidate], out_path: Path) -> None:
    lines = [
        "# Card Maker Review Worklist",
        "",
        f"Generated Cards ready for operator review: {len(reviews)}",
        "",
        "This worklist contains generated Cards that are not flagged as duplicates. The operator may review each Card before indexing it for MCP use, publishing it, or keeping it private.",
        "",
        "## Operator instruction",
        "",
        "1. Read the generated Card file.",
        "2. Check that it is bounded, repeatable, playable, and receiptable.",
        "3. If warnings are listed, resolve them first.",
        "4. Only then index it for your local MCP Card use, publish it, or keep it private.",
        "",
    ]

    clean: list[ReviewCandidate] = []
    warned: list[ReviewCandidate] = []
    for r in reviews:
        (warned if r.warnings else clean).append(r)

    if clean:
        lines.extend(
            [
                "## Clean generated Cards",
                "",
            ]
        )
        for r in clean:
            lines.extend(
                [
                    f"- `{r.card.card_id}` — {r.card.name}",
                    f"  - Source: `{r.card.source_origin}`",
                    f"  - Output: `{r.card.output}`",
                    "",
                ]
            )

    if warned:
        lines.extend(
            [
                "## Generated Cards with warnings",
                "",
            ]
        )
        for r in warned:
            lines.extend(
                [
                    f"- `{r.card.card_id}` — {r.card.name}",
                    f"  - Source: `{r.card.source_origin}`",
                    f"  - Output: `{r.card.output}`",
                    f"  - Warnings: {', '.join(r.warnings)}",
                    "",
                ]
            )

    if not reviews:
        lines.append("No review candidates.")
        lines.append("")

    lines.extend(
        [
            "## Claim boundary",
            "",
            "This worklist is a filtered view, not an approval. Only the operator decides what enters their local MCP Card index. Card Maker never auto-approves.",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_worklist_jsonl(reviews: list[ReviewCandidate], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for r in reviews:
            record = dict(r.card.raw)
            record["_card_maker_warnings"] = r.warnings
            record["_card_maker_ready_for_review"] = not r.warnings
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check generated Cards against the existing Card registry.")
    parser.add_argument(
        "--candidates",
        default="_card_forge_out/registry_card_generated.jsonl",
        help="Generated Card registry JSONL (default: _card_forge_out/registry_card_generated.jsonl)",
    )
    parser.add_argument(
        "--registry",
        default="registry/card_registry.jsonl",
        help="Existing Card registry JSONL (default: registry/card_registry.jsonl)",
    )
    parser.add_argument(
        "--out",
        default="_card_maker_out",
        help="Output directory for reports (default: _card_maker_out)",
    )
    args = parser.parse_args()

    candidates_path = Path(args.candidates).expanduser().resolve()
    registry_path = Path(args.registry).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()

    if not candidates_path.exists():
        fail(f"Generated Cards file not found: {candidates_path}")
    if not registry_path.exists():
        fail(f"Registry file not found: {registry_path}")

    generated_records = load_jsonl(candidates_path)
    existing_records = load_jsonl(registry_path)

    for i, rec in enumerate(generated_records):
        validate_record(rec, f"Generated line {i + 1}")
    for i, rec in enumerate(existing_records):
        validate_record(rec, f"Existing line {i + 1}")

    generated = [to_card(r) for r in generated_records]
    existing = [to_card(r) for r in existing_records]

    duplicates = find_duplicates(generated, existing)
    reviews = find_review_candidates(generated, existing, duplicates)

    out_dir.mkdir(parents=True, exist_ok=True)

    write_duplicate_report(duplicates, out_dir / "duplicate_report.md")
    write_review_worklist(reviews, out_dir / "review_worklist.md")
    write_worklist_jsonl(reviews, out_dir / "review_worklist.jsonl")

    print(f"PASS: Card Maker completed.")
    print(f"  Generated Cards checked: {len(generated)}")
    print(f"  Existing indexed Cards:  {len(existing)}")
    print(f"  Duplicates found:        {len(duplicates)}")
    print(f"  Review ready:            {len(reviews)}")
    print(f"  Output:                  {out_dir}")


if __name__ == "__main__":
    main()
