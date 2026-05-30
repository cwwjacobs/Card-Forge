# Human Approval Gate Card

Card ID: `gate.human_approval.v0_1`
Type: Gate Card
Status: canon

## Input

A proposed risky action, canon change, publish step, file modification, deployment, spending action, or external communication.

## Move

Pause the Run and request operator approval.

## Output

`APPROVED`, `REJECTED`, or `NEEDS_REVISION`.

## Done When

The human decision is recorded.

## Stop If

No approval is provided for a risky action.

## Receipt

Record the decision and next action.

## Permissions

`human_required`
