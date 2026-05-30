#!/usr/bin/env python3
"""Card Maker: check candidate Cards against the canonical registry.

Reads candidate Cards (e.g. from Card Forge Skill output) and the canonical
registry. Emits a duplicate report and a promotion worklist. Does NOT
auto-canonize without operator approval.

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
    candidate: CardRecord
    canonical: CardRecord
    reasons: list[str]


@dataclass
class PromotionCandidate:
    card: CardRecord
    warnings: list[str]


def find_duplicates(candidates: list[CardRecord], canonical: list[CardRecord]) -> list[DuplicateFinding]:
    findings: list[DuplicateFinding] = []
    canonical_by_id = {c.card_id: c for c in canonical}
    canonical_by_name = {normalize(c.name): c for c in canonical if normalize(c.name)}

    for cand in candidates:
        reasons: list[str] = []
        matched: CardRecord | None = None

        if cand.card_id in canonical_by_id:
            matched = canonical_by_id[cand.card_id]
            reasons.append("exact card_id match")

        norm_name = normalize(cand.name)
        if norm_name and norm_name in canonical_by_name:
            matched = canonical_by_name[norm_name]
            if "exact name match" not in reasons:
                reasons.append("exact name match")

        if matched:
            norm_cand_move = normalize(cand.move)
            norm_match_move = normalize(matched.move)
            if norm_cand_move and norm_cand_move == norm_match_move:
                if "same move text" not in reasons:
                    reasons.append("same move text")

            findings.append(DuplicateFinding(candidate=cand, canonical=matched, reasons=reasons))

    return findings


def find_promotion_candidates(
    candidates: list[CardRecord],
    canonical: list[CardRecord],
    duplicate_findings: list[DuplicateFinding],
) -> list[PromotionCandidate]:
    duplicate_ids = {f.candidate.card_id for f in duplicate_findings}
    canonical_norm_names = {normalize(c.name) for c in canonical}
    canonical_norm_moves = {normalize(c.move) for c in canonical}
    promotion_candidates: list[PromotionCandidate] = []

    for cand in candidates:
        if cand.card_id in duplicate_ids:
            continue
        warnings: list[str] = []
        norm_name = normalize(cand.name)
        norm_move = normalize(cand.move)

        if norm_name and any(norm_name in cn or cn in norm_name for cn in canonical_norm_names if cn):
            warnings.append("name overlaps with existing canonical Card")
        if norm_move and any(norm_move in cm or cm in norm_move for cm in canonical_norm_moves if cm):
            warnings.append("move text overlaps with existing canonical Card")
        if not cand.name or len(cand.name) < 3:
            warnings.append("name is too short")
        if not cand.move or len(cand.move) < 10:
            warnings.append("move is too short")
        if cand.status != "candidate":
            warnings.append(f"status is '{cand.status}', expected 'candidate'")

        promotion_candidates.append(PromotionCandidate(card=cand, warnings=warnings))

    return promotion_candidates


def write_duplicate_report(findings: list[DuplicateFinding], out_path: Path) -> None:
    lines = [
        "# Card Maker Duplicate Report",
        "",
        f"Duplicates found: {len(findings)}",
        "",
        "This report lists candidate Cards that appear to already exist in the canonical registry.",
        "",
        "## Operator instruction",
        "",
        "Review each finding. If the candidate is truly a duplicate, discard it. If it is a variant, rename or differentiate the move/output before promotion.",
        "",
    ]

    for i, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"### {i}. `{finding.candidate.card_id}`",
                "",
                f"- Candidate name: `{finding.candidate.name}`",
                f"- Canonical match: `{finding.canonical.card_id}` (`{finding.canonical.name}`)",
                f"- Reasons: {', '.join(finding.reasons)}",
                f"- Candidate source: `{finding.candidate.source_origin}`",
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
            "This report uses heuristics. It does not guarantee completeness. A candidate flagged as duplicate may be a valid variant, and a candidate not flagged may still overlap semantically.",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_promotion_worklist(promotions: list[PromotionCandidate], out_path: Path) -> None:
    lines = [
        "# Card Maker Promotion Worklist",
        "",
        f"Candidates ready for operator review: {len(promotions)}",
        "",
        "This worklist contains candidate Cards that are not flagged as duplicates. The operator must review each Card before promoting it to `canon`.",
        "",
        "## Operator instruction",
        "",
        "1. Read the candidate Card file.",
        "2. Check that it is bounded, repeatable, playable, and receiptable.",
        "3. If warnings are listed, resolve them first.",
        "4. Only then change `status` from `candidate` to `canon`.",
        "5. Append the approved record to `registry/card_registry.jsonl`.",
        "",
    ]

    clean: list[PromotionCandidate] = []
    warned: list[PromotionCandidate] = []
    for p in promotions:
        (warned if p.warnings else clean).append(p)

    if clean:
        lines.extend(
            [
                "## Clean candidates",
                "",
            ]
        )
        for p in clean:
            lines.extend(
                [
                    f"- `{p.card.card_id}` — {p.card.name}",
                    f"  - Source: `{p.card.source_origin}`",
                    f"  - Output: `{p.card.output}`",
                    "",
                ]
            )

    if warned:
        lines.extend(
            [
                "## Candidates with warnings",
                "",
            ]
        )
        for p in warned:
            lines.extend(
                [
                    f"- `{p.card.card_id}` — {p.card.name}",
                    f"  - Source: `{p.card.source_origin}`",
                    f"  - Output: `{p.card.output}`",
                    f"  - Warnings: {', '.join(p.warnings)}",
                    "",
                ]
            )

    if not promotions:
        lines.append("No promotion candidates.")
        lines.append("")

    lines.extend(
        [
            "## Claim boundary",
            "",
            "This worklist is a filtered view, not an approval. Only the operator may promote a Card to canon. Card Maker never auto-canonizes.",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_worklist_jsonl(promotions: list[PromotionCandidate], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for p in promotions:
            record = dict(p.card.raw)
            record["_card_maker_warnings"] = p.warnings
            record["_card_maker_ready_for_review"] = not p.warnings
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check candidate Cards against the canonical registry.")
    parser.add_argument(
        "--candidates",
        default="_card_forge_out/registry_card_candidates.jsonl",
        help="Candidate registry JSONL (default: _card_forge_out/registry_card_candidates.jsonl)",
    )
    parser.add_argument(
        "--registry",
        default="registry/card_registry.jsonl",
        help="Canonical registry JSONL (default: registry/card_registry.jsonl)",
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
        fail(f"Candidates file not found: {candidates_path}")
    if not registry_path.exists():
        fail(f"Registry file not found: {registry_path}")

    candidate_records = load_jsonl(candidates_path)
    canonical_records = load_jsonl(registry_path)

    for i, rec in enumerate(candidate_records):
        validate_record(rec, f"Candidate line {i + 1}")
    for i, rec in enumerate(canonical_records):
        validate_record(rec, f"Canonical line {i + 1}")

    candidates = [to_card(r) for r in candidate_records]
    canonical = [to_card(r) for r in canonical_records]

    duplicates = find_duplicates(candidates, canonical)
    promotions = find_promotion_candidates(candidates, canonical, duplicates)

    out_dir.mkdir(parents=True, exist_ok=True)

    write_duplicate_report(duplicates, out_dir / "duplicate_report.md")
    write_promotion_worklist(promotions, out_dir / "promotion_worklist.md")
    write_worklist_jsonl(promotions, out_dir / "promotion_worklist.jsonl")

    print(f"PASS: Card Maker completed.")
    print(f"  Candidates checked: {len(candidates)}")
    print(f"  Canonical Cards:    {len(canonical)}")
    print(f"  Duplicates found:   {len(duplicates)}")
    print(f"  Promotion ready:    {len(promotions)}")
    print(f"  Output:             {out_dir}")


if __name__ == "__main__":
    main()
