# AI Build Preflight Deck

Status: draft
Deck ID: `deck.ai_build_preflight.v0_1`

## Purpose

Check an AI-built app before publishing by running bounded Cards that inspect source material, identify common blockers, and produce receipts.

## Stacks in order

1. Intake Stack
2. Structure Check Stack
3. Repair Planning Stack
4. Readiness Stack

## Allowed permissions

- `read_only`
- `write_reports`

This Deck should not modify source files by default.

## Run outputs

- `source_inventory.md`
- `blocker_report.md`
- `repair_prompt.md`
- `readiness_receipt.md`

## Final gate

Allowed final statuses (from `RUN_STANDARD.md`):

- `PASS`
- `PASS_WITH_WARNINGS`
- `FAIL`
- `NEEDS_SOURCE`
- `NEEDS_HUMAN`

## Draw Pool

The Cards this Deck draws from, in rough Stack order:

- `check.source_inventory.v0_1` — Intake
- `contract.no_overclaim.v0_1` — Intake
- `check.blocker_report.v0_1` — Structure Check
- `prompt.repair_prompt.v0_1` — Repair Planning
- `receipt.readiness_receipt.v0_1` — Readiness
- `gate.human_approval.v0_1` — Gate (played whenever a risky action or index change needs sign-off)

## Claim boundary

This Deck does not guarantee security, correctness, compliance, or production readiness. It identifies common publish-readiness blockers and records what was checked.
