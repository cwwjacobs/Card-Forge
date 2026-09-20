# Repair Planning Stack

Stack ID: `stack.repair_planning.v0_1`

## Purpose

Turn findings into a focused next-step prompt.

## Cards in order

1. `prompt.repair_prompt.v0_1`
2. `contract.no_overclaim.v0_1`

## Entry condition

A blocker report exists.

## Exit condition

A focused next-step prompt exists and claim boundaries are preserved.

## Failure route

If there are no clear blockers, skip this Stack and continue to readiness.

## Run outputs

- `repair_prompt.md`
- `allowed_claims_and_blocked_claims.md`

## Permissions

- `read_only`
- `write_reports`
