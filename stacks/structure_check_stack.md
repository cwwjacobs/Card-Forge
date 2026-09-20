# Structure Check Stack

Stack ID: `stack.structure_check.v0_1`

## Purpose

Inspect source shape and identify common structural blockers.

## Cards in order

1. `check.source_inventory.v0_1`
2. `check.blocker_report.v0_1`

## Entry condition

The Intake Stack has produced a source inventory.

## Exit condition

Common structure blockers have been listed or no blocker was found by this Stack.

## Failure route

If source shape is unclear, stop and request more source.

## Run outputs

- `blocker_report.md`

## Permissions

- `read_only`
- `write_reports`
