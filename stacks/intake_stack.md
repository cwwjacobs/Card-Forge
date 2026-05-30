# Intake Stack

Stack ID: `stack.intake.v0_1`

## Purpose

Prepare source material before the Deck continues.

## Cards in order

1. `check.source_inventory.v0_1`
2. `contract.no_overclaim.v0_1`

## Entry condition

Source material has been provided.

## Exit condition

Source material has been inventoried and claim boundaries are active.

## Failure route

If no source material is provided, stop the Run and emit an intake receipt.

## Run outputs

- `source_inventory.md`
- `allowed_claims_and_blocked_claims.md`

## Permissions

- `read_only`
- `write_reports`
