# Repair Prompt Card

Card ID: `prompt.repair_prompt.v0_1`
Type: Prompt Card
Status: canon

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
