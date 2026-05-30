---
card_id: "contract.no_overclaim.v0_1"
name: "No Overclaim Contract"
type: "Contract Card"
status: "indexed"
input: "Draft output, readiness claim, sales claim, or final receipt language."
move: "Check for claims stronger than the available evidence supports."
output: "allowed_claims_and_blocked_claims.md"
done_when: "Unsupported claims are removed or marked."
stop_if: "A guarantee or unsupported safety, compliance, correctness, production-readiness, or bug-free claim remains."
receipt: "Record the claim boundary result."
permissions:
  - "read_only"
risk_level: "medium"
token_size: "small"
source_origin: "Card Forge starter set"
---

# No Overclaim Contract

## Input

Draft output, readiness claim, sales claim, or final receipt language.

## Move

Check for claims stronger than the available evidence supports.

## Output

`allowed_claims_and_blocked_claims.md`

## Done When

Unsupported claims are removed or marked.

## Stop If

A guarantee or unsupported safety, compliance, correctness, production-readiness, or bug-free claim remains.

## Receipt

Record the claim boundary result.

## Permissions

`read_only`
