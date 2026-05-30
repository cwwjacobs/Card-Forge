# Readiness Receipt Card

Card ID: `receipt.readiness_receipt.v0_1`
Type: Receipt Card
Status: canon

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
