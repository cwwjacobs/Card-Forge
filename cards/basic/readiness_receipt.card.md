---
card_id: "receipt.readiness_receipt.v0_1"
name: "Readiness Receipt"
type: "Receipt Card"
status: "indexed"
input: "Run outputs, blockers, warnings, skipped checks, and next-action notes."
move: "Create a bounded readiness receipt for the current Run."
output: "readiness_receipt.md"
done_when: "The receipt states what was checked, what was not checked, what passed, what blocked progress, and the next action."
stop_if: "Run outputs are missing."
receipt: "The readiness receipt is the evidence artifact."
permissions:
  - "read_only"
  - "write_reports"
risk_level: "low"
token_size: "small"
source_origin: "Card Forge starter set"
---

# Readiness Receipt

## Input

Run outputs, blockers, warnings, skipped checks, and next-action notes.

## Move

Create a bounded readiness receipt for the current Run.

## Output

`readiness_receipt.md`

## Done When

The receipt states what was checked, what was not checked, what passed, what blocked progress, and the next action.

## Stop If

Run outputs are missing.

## Receipt

The readiness receipt is the evidence artifact.

## Permissions

`read_only`, `write_reports`
