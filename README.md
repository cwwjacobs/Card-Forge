# Card Forge

Reusable workflow Cards, Card Stacks, Decks, Runs, and Receipts for AI-assisted work.

Card Forge turns messy source material into small reusable workflow moves that can be stacked into repeatable Decks and run by humans, frontier models, or smaller edge agents.

## Start here

New users should begin with:

```text
START_HERE.md
```

That file gives the 5-minute path through the templates, starter Cards, registry, first example Deck, example Run State, and example Receipt.

## Core idea

- A **Card** is one reusable workflow move.
- A **Card Stack** is an ordered group of Cards.
- A **Deck** is a reusable workflow package.
- A **Run** is an execution of a Deck on real material.
- A **Receipt** proves what happened.

> Build workflow Decks that frontier models can forge and edge agents can run.

## Why this exists

AI-assisted work often leaves behind messy prompts, partial apps, broken files, scattered notes, and unclear decisions. Card Forge gives that work a reusable structure:

```text
source material -> Cards -> Card Stacks -> Deck -> Run -> Receipts
```

The goal is not to make agents more magical. The goal is to give them rails.

## Minimum runtime objects

Edge-sized agents should only need the runtime layer:

- `Card`: what to do, what to use, what to produce, when to stop, what to record.
- `Card Stack`: which Cards to play, in what order, and where to route failures.
- `Deck`: the packaged reusable workflow.
- `Run State`: the current execution state.
- `Receipt`: proof and memory bridge for what happened.

## Repository map

```text
registry/        Canonical Card Registry and Card Index
cards/           Reusable Cards grouped by type
decks/           Packaged reusable Decks
runs/            Example Run states and outputs
receipts/        Example receipts from Runs
schemas/         JSON schemas for Cards, Decks, Runs, and Receipts
prompts/         Prompt cards for drawing, cutting, forging, building, and running
templates/       Copyable templates for Cards, Decks, and Receipts
scripts/         Validation scripts
```

## First Deck

The first planned Deck is:

```text
decks/ai-build-preflight/
```

It is a Deck for checking AI-built apps before publishing.

## Edge Runtime Demo

**Decks compile to Card Stacks for small-context agents.**

See:

- `docs/EDGE_RUNTIME.md` — How frontier models forge Decks and edge agents run compiled Stacks.
- `examples/edge-runtime-32k/` — A concrete 32k-context run packet demo using the `ai-build-preflight` Deck.

This demo shows structural compression, not model benchmarking. 32k compatibility means the run packet is designed to fit in 32k tokens; it does not guarantee that every edge model will execute it reliably.

## Validation

Run the public-core validator from the repository root:

```bash
python3 scripts/validate_card_forge.py
```

Expected result:

```text
PASS: Card Forge core validation completed.
```

The same validator is wired into GitHub Actions through:

```text
.github/workflows/validate.yml
```

## License

MIT. See `LICENSE`.
