# Blocker Report Card

Card ID: `check.blocker_report.v0_1`
Type: Check Card
Status: canon

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
