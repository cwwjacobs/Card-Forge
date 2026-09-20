# Start Here

This file is the fastest path for using Card Forge Core.

Card Forge is a small workflow grammar for AI-assisted work:

```text
source material -> Cards -> Card Stacks -> Deck -> Run -> Receipt
```

## The 5-minute path

### 1. Read the basic objects

- A **Card** is one reusable workflow move.
- A **Card Stack** is an ordered group of Cards.
- A **Deck** is a reusable workflow package.
- A **Run** is an execution of a Deck on real material.
- A **Receipt** proves what happened.

### 2. Open the Card template

Use:

```text
templates/card_template.md
```

A Card must answer:

```text
What does it use?
What does it do?
What does it produce?
When does it stop?
What does it record?
```

### 3. Look at the starter Cards

Start with:

```text
cards/basic/source_inventory.card.md
cards/basic/no_overclaim_contract.card.md
cards/basic/human_approval_gate.card.md
```

These are intentionally basic. They are public-core examples, not paid Deck content.

### 4. Check the registry

The Card Registry is the source of truth:

```text
registry/card_registry.jsonl
```

The human-readable view is:

```text
registry/card_index.md
```

### 5. Run the first example Deck path

The first draft Deck is:

```text
decks/ai-build-preflight/deck.md
```

Its example Run State is:

```text
runs/examples/ai_build_preflight_run_state.example.json
```

Its example Receipt is:

```text
receipts/examples/ai_build_preflight_receipt.example.md
```

## How to use this with an LLM

Give the model this instruction:

```text
Use Card Forge Core. Play only the current Card from the Run State. Produce the requested output and update the Receipt. Stop if the Card stop condition appears.
```

Then provide:

1. the Deck
2. the Run State
3. the current Card
4. the source material

## Public-core boundary

This repo should stay focused on the open standard and minimal examples.

Do not add private paid Deck Pack content here unless intentionally publishing it.

## Validation

Run the validator from the repository root:

```bash
python3 scripts/validate_card_forge.py
```

Expected result:

```text
PASS: Card Forge core validation completed.
```
