# Readiness Stack

Stack ID: `stack.readiness.v0_1`

## Purpose

Make a bounded final Run decision and record what happened.

## Cards in order

1. `receipt.readiness_receipt.v0_1`
2. `gate.human_approval.v0_1`

## Entry condition

The Run has produced findings or outputs to summarize.

## Exit condition

A readiness receipt exists and any required human approval is recorded.

## Failure route

If a human decision is required and unavailable, mark the Run as `NEEDS_HUMAN`.

## Run outputs

- `readiness_receipt.md`

## Permissions

- `read_only`
- `write_reports`
- `human_required`
