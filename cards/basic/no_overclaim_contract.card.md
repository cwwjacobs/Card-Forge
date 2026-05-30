# No Overclaim Contract Card

Card ID: `contract.no_overclaim.v0_1`
Type: Contract Card
Status: candidate

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
