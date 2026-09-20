# Deck Standard

A Deck is a reusable workflow package made from ordered Card Stacks.

## Minimum Deck fields

```yaml
deck_id: ""
name: ""
purpose: ""
stacks_in_order: []
allowed_permissions: []
run_outputs: []
final_gate: ""
```

## Deck responsibilities

A Deck should define:

- the problem it handles
- the Card Stacks it runs
- the permissions allowed during a Run
- the outputs it should produce
- the final decision gate
- the receipt expected at the end

## Edge-compatible Decks

An edge-compatible Deck should be able to run from compressed Cards and clear state transitions.

Edge agents need:

- explicit Card order
- clear stop conditions
- small outputs
- checkpoint receipts
- human gates for risky decisions

## Frontier-compatible Decks

Frontier models may use richer Deck documentation, examples, alternate paths, and synthesis notes.

## Core principle

Frontier models can help forge Decks. Edge agents should be able to run Decks when the rails are clear.
