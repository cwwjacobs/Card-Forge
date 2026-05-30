---
card_id: "check.blocker_report.v0_1"
name: "Blocker Report"
type: "Check Card"
status: "indexed"
input: "Source inventory, source material, notes, or prior Run outputs."
move: "List blockers that prevent the current Run from continuing cleanly."
output: "blocker_report.md"
done_when: "Blockers are listed, or the report states that no blocker was found by this Card."
stop_if: "The source material is too incomplete to inspect."
receipt: "Record blockers found, source gaps, and the next recommended Card."
permissions:
  - "read_only"
  - "write_reports"
risk_level: "low"
token_size: "small"
source_origin: "Card Forge starter set"
---

# Blocker Report

## Input

Source inventory, source material, notes, or prior Run outputs.

## Move

List blockers that prevent the current Run from continuing cleanly.

## Output

`blocker_report.md`

## Done When

Blockers are listed, or the report states that no blocker was found by this Card.

## Stop If

The source material is too incomplete to inspect.

## Receipt

Record blockers found, source gaps, and the next recommended Card.

## Permissions

`read_only`, `write_reports`
