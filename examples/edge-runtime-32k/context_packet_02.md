# Context Packet 02

## Current Card

- **card_id**: `contract.no_overclaim.v0_1`
- **type**: Contract Card
- **input**: Draft output, readiness claim, sales claim, or final receipt language.
- **move**: Check for claims stronger than the available evidence supports.
- **output**: `allowed_claims_and_blocked_claims.md`
- **done_when**: Unsupported claims are removed or marked.
- **stop_if**: A guarantee or unsupported safety, compliance, correctness, production-readiness, or bug-free claim remains.
- **receipt**: Record the claim boundary result.
- **permissions**: `read_only`

## Current Stack

- **stack_id**: `stack.intake.compiled.v0_1`
- **cards_in_order**:
  1. `check.source_inventory.v0_1`
  2. `contract.no_overclaim.v0_1`
- **entry_condition**: Source material has been provided.
- **exit_condition**: Source material is inventoried and claim boundaries are active.
- **failure_route**: Stop and emit an intake receipt if claim boundaries are violated.

## Run State

- **run_id**: `run.edge_runtime_32k.demo_001`
- **deck_id**: `deck.ai_build_preflight.v0_1`
- **status**: `RUNNING`
- **inputs**: `example index.html`, `example main.js`
- **outputs**: `source_inventory.md`
- **next_action**: `play contract.no_overclaim.v0_1`

## Relevant Prior Receipt

`receipts/receipt_01_source_inventory.md`

- Files seen: `example index.html`, `example main.js`
- Files missing: None
- Intake can continue: Yes

## Expected Output

`allowed_claims_and_blocked_claims.md` with unsupported claims flagged.

## Stop Condition

Stop if a guarantee or unsupported safety, compliance, correctness, production-readiness, or bug-free claim remains.
