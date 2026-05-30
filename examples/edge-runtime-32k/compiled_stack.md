# Compiled Stack: AI Build Preflight — Intake Slice

Stack ID: `stack.intake.compiled.v0_1`
Source Deck: `deck.ai_build_preflight.v0_1`

## Purpose

Prepare source material and enforce claim boundaries before the Deck continues.

## Cards in order

1. `check.source_inventory.v0_1`
2. `contract.no_overclaim.v0_1`

## Entry condition

Source material has been provided.

## Exit condition

Source material is inventoried and claim boundaries are active.

## Failure route

- If no source material is provided, stop and emit an intake receipt.
- If an unsupported claim is found, mark it and stop before continuing.

## Permissions

- `read_only`
- `write_reports`

## Claim boundary

This Stack does not guarantee correctness, security, compliance, or production readiness. It inventories source material and flags overclaims.
