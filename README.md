# Card Forge

Reusable workflow Cards, Card Stacks, Decks, Runs, and Receipts for AI-assisted work.

Card Forge turns messy source material into small reusable workflow moves that can be stacked into repeatable Decks and run by humans, frontier models, or smaller edge agents.

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
```

## First Deck

The first planned Deck is:

```text
decks/ai-build-preflight/
```

It is a Deck for checking AI-built apps before publishing.

## License

MIT. See `LICENSE`.
