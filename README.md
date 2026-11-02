# Card Forge

Reusable workflow Cards, Card Stacks, Decks, Runs, and Receipts for AI-assisted work.

Card Forge turns high-noise source material into small reusable workflow moves that can be stacked into repeatable Decks and run by humans, frontier models, or smaller edge agents.

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

AI-assisted work often leaves behind rough prompts, partial apps, broken files, scattered notes, and unclear decisions. Card Forge gives that work a reusable structure:

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
schemas/         Reference JSON schemas for Cards, Decks, Runs, and Receipts
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
  Records validated against full schemas: 15 cards, 10 generated cards, 5 stacks, 1 decks, 3 runs, 6 receipt checkpoint records from 5 receipts.
  Cross-references checked: 38.
Functional checks (negative fixtures, reported separately from the validator pass): 15 passed, 0 failed.
```

The validator is intentionally standard-library only (no third-party JSON Schema package is a repo dependency, so the needed JSON Schema subset is implemented in stdlib Python inside the validator). It checks required paths and then validates every Card, Stack, Deck, Run, and Receipt record in the repository against the full schema files in `schemas/` (generated Card examples against `skills/card-forge-skill/schemas/generated_card.schema.json`), enforces the Run status set from `RUN_STANDARD.md`, and verifies cross-reference integrity: Deck→Stack→Card references resolve and Run→Receipt references resolve (the receipt exists and declares the Run's `run_id`).

It also runs the negative-fixture suite in `tests/negative/`: each fixture is a mutated copy of the repository (wrong types/ranges, missing required fields, dangling references, duplicate IDs, invalid Run states) that the validator must reject. Fixture results are functional checks and are reported separately from the overall validator pass; the exit code is non-zero if either fails. The suite can also be run standalone:

```bash
python3 tests/run_negative_fixtures.py
```

The same validator is wired into GitHub Actions through:

```text
.github/workflows/validate.yml
```

## License

Card Forge is source-available under the **PolyForm Noncommercial License 1.0.0**. Noncommercial use is permitted under the included license; commercial use requires a separate written license from Corey Jacobs. See `LICENSE` and `COMMERCIAL_LICENSE.md`.
