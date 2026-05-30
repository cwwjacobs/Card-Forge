---
card_id: "gate.human_approval.v0_1"
name: "Human Approval Gate"
type: "Gate Card"
status: "indexed"
input: "A proposed risky action, trusted Card index change, publish step, file modification, deployment, spending action, or external communication."
move: "Pause the Run and request operator approval."
output: "APPROVED / REJECTED / NEEDS_REVISION"
done_when: "The human decision is recorded."
stop_if: "No approval is provided for a risky action."
receipt: "Record the decision and next action."
permissions:
  - "human_required"
risk_level: "medium"
token_size: "small"
source_origin: "Card Forge starter set"
---

# Human Approval Gate

## Input

A proposed risky action, trusted Card index change, publish step, file modification, deployment, spending action, or external communication.

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
