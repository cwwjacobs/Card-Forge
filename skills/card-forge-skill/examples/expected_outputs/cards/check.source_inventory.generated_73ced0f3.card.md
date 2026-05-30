---
card_id: "check.source_inventory.generated_73ced0f3"
name: "Source inventory"
type: "Check Card"
status: "generated"
input: "Source files, notes, prior receipts, or run state relevant to the check."
move: "Inspect the source material for source inventory and summarize findings with evidence."
output: "source_inventory_report.md"
done_when: "`source_inventory_report.md` exists and states findings, warnings, blockers, and next action where applicable."
stop_if: "Stop if required source material is missing or the move would require guessing."
receipt: "Record inputs used, result summary, warnings, skipped checks, and path to `source_inventory_report.md`."
permissions:
  - "read_only"
  - "write_reports"
risk_level: "low"
token_size: "small"
source_origin: "README.md"
---

# Source inventory

## Input

Source files, notes, prior receipts, or run state relevant to the check.

## Move

Inspect the source material for source inventory and summarize findings with evidence.

## Output

`source_inventory_report.md`

## Done when

`source_inventory_report.md` exists and states findings, warnings, blockers, and next action where applicable.

## Stop if

Stop if required source material is missing or the move would require guessing.

## Receipt

Record inputs used, result summary, warnings, skipped checks, and path to `source_inventory_report.md`.

## Review notes

- Use now: with review
- Duplicate risk: high
- Suggested action: review_or_merge
- Reason: Possible overlap: exact name match. Review before indexing or publishing.
