# Context Packet 01

## Current Card

- **card_id**: `check.source_inventory.v0_1`
- **type**: Check Card
- **input**: Files, pasted text, repo listing, or source bundle.
- **move**: List available source material and classify it by type.
- **output**: `source_inventory.md`
- **done_when**: Source material is listed and grouped.
- **stop_if**: No source material is provided.
- **receipt**: Record files seen, files missing, and whether intake can continue.
- **permissions**: `read_only`

## Current Stack

- **stack_id**: `stack.intake.compiled.v0_1`
- **cards_in_order**:
  1. `check.source_inventory.v0_1`
  2. `contract.no_overclaim.v0_1`
- **entry_condition**: Source material has been provided.
- **exit_condition**: Source material is inventoried and claim boundaries are active.
- **failure_route**: Stop and emit an intake receipt if no source material is provided.

## Run State

- **run_id**: `run.edge_runtime_32k.demo_001`
- **deck_id**: `deck.ai_build_preflight.v0_1`
- **status**: `RUNNING`
- **inputs**: `example index.html`, `example main.js`
- **outputs**: []
- **next_action**: `play check.source_inventory.v0_1`

## Relevant Prior Receipt

None. This is the first Card.

## Expected Output

`source_inventory.md` listing the provided source material.

## Stop Condition

Stop if no source material is provided.
