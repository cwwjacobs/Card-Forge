# Edge Runtime 32k Demo

A 5-minute demo showing how a Card Forge Deck compiles into an edge-runnable Card Stack.

## What this demo shows

Frontier models forge Decks. Edge agents run compiled Card Stacks. This demo compiles two Cards from the `ai-build-preflight` Deck into a small-context run packet.

## Files

| File | Purpose |
|---|---|
| `compiled_stack.md` | The compiled Stack with only the Cards needed at runtime |
| `run_state.json` | Current execution state |
| `context_packet_01.md` | Run packet for Card 1: source inventory |
| `context_packet_02.md` | Run packet for Card 2: no-overclaim contract |
| `receipts/receipt_01_source_inventory.md` | Receipt after Card 1 |
| `receipts/receipt_02_no_overclaim.md` | Receipt after Card 2 |
| `receipts/final_receipt.md` | Final receipt for the compiled Stack |

## How to read it

1. Open `compiled_stack.md` to see the compiled Stack.
2. Open `context_packet_01.md` to see what an edge agent receives for the first Card.
3. Open `receipts/receipt_01_source_inventory.md` to see what the agent produces.
4. Open `context_packet_02.md` to see the next run packet, which includes the prior receipt.
5. Open `receipts/final_receipt.md` to see the Stack conclusion.

## Claim boundary

This demo shows structure compression, not model capability. 32k compatibility means the packet is designed to fit in 32k tokens. It does not guarantee that every edge model will execute it correctly. See `CLAIM_BOUNDARY.md` for system-wide claim limits.
