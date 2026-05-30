---
card_id: "prompt.repair_prompt.v0_1"
name: "Repair Prompt"
type: "Prompt Card"
status: "indexed"
input: "Blocker report, source inventory, and desired change boundary."
move: "Write a focused prompt that asks an AI/code agent to address the listed blockers without expanding scope."
output: "repair_prompt.md"
done_when: "The prompt names the source context, target blockers, allowed changes, and blocked changes."
stop_if: "No blocker report exists."
receipt: "Record which blockers the prompt targets."
permissions:
  - "read_only"
  - "write_reports"
risk_level: "medium"
token_size: "medium"
source_origin: "Card Forge starter set"
---

# Repair Prompt

## Input

Blocker report, source inventory, and desired change boundary.

## Move

Write a focused prompt that asks an AI/code agent to address the listed blockers without expanding scope.

## Output

`repair_prompt.md`

## Done When

The prompt names the source context, target blockers, allowed changes, and blocked changes.

## Stop If

No blocker report exists.

## Receipt

Record which blockers the prompt targets.

## Permissions

`read_only`, `write_reports`
