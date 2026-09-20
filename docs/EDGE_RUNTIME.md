# Edge Runtime

Card Forge Decks can be compiled into edge-runnable Card Stacks.

## Core idea

- **Frontier models** forge Decks.
- **Edge agents** run compiled Card Stacks.
- **Receipts** replace memory.
- A **Deck** is the full workflow package.
- A **Card Stack** is the runtime slice.
- A **Skill** is an optional runner or wrapper, not the Deck itself.

## What edge runtime means

An edge agent does not need the full Deck documentation, forge history, or alternate paths. It needs:

- the current Card
- the current Stack
- the Run State
- relevant prior Receipts

That is the run packet. When the packet is small enough, it can fit into a 32k context window.

## 32k compatibility

32k compatibility means the run packet is **designed to fit in 32k tokens**. It does not mean every model will execute it reliably. Model capability, instruction following, and context utilization vary.

## Permissions

Permissions in a Card are advisory runtime hints until an enforcing runner exists. A Card may declare `read_only`, but the actual enforcement depends on the runner or agent using the Stack.

## Claim boundary

This is a constrained runtime-contract demo. It shows that the Card Forge structure can compress into small-context packets.

It does **not** guarantee:

- local-model correctness
- reliable execution on any specific edge model
- production safety
- security validation

See `examples/edge-runtime-32k/` for a concrete demo.
