# Card Maker / Card Index

Card Maker reviews generated Cards produced by the Card Forge Skill.

## Purpose

Card Forge Skill generates usable Cards from source material. Card Maker checks those generated Cards against the existing Card registry and emits:

- a **duplicate report**
- a **review worklist**

## Card index

`registry/card_registry.jsonl` is the existing Card registry. It contains Cards the operator has chosen to index, including trusted Cards with `status: canon`.

Card Forge generates usable Cards. Our recommended operating pattern is to keep a local MCP Card index of trusted/tested Cards for agents, while allowing experimental Cards to remain local, private, dev-indexed, or unindexed.

## What Card Maker does

1. Read generated Cards from a JSONL file (usually `_card_forge_out/registry_card_generated.jsonl`).
2. Read the existing Card registry (`registry/card_registry.jsonl`).
3. Detect duplicates by:
   - exact `card_id` match
   - exact normalized name match
   - same normalized move text
4. Flag review candidates that are not duplicates.
5. Warn on name overlap, move overlap, short fields, or unexpected status.

## What Card Maker does NOT do

- **Auto-approve.** Card Maker never changes `candidate` to `canon`.
- **Enforce indexing.** Card Maker does not require operators to use the registry.
- **Guarantee completeness.** Duplicate detection is heuristic, not proof.

## Operator indexing

Only the operator decides what enters their local MCP Card index.

The review worklist explains the steps:

1. Read the generated Card file.
2. Check that it is bounded, repeatable, playable, and receiptable.
3. If warnings are listed, resolve them first.
4. Only then index it for your local MCP Card use, publish it, or keep it private.

## Run

From the repo root:

```bash
python3 skills/card-forge-skill/card_maker.py \
  --candidates _card_forge_out/registry_card_generated.jsonl \
  --registry registry/card_registry.jsonl \
  --out _card_maker_out
```

Or through the wrapper:

```bash
python3 scripts/card_maker.py \
  --candidates _card_forge_out/registry_card_generated.jsonl \
  --registry registry/card_registry.jsonl \
  --out _card_maker_out
```

## Output

```text
_card_maker_out/
  duplicate_report.md
  review_worklist.md
  review_worklist.jsonl
```

## Publishing guidance

Card Forge recommends trusted/indexed Cards for public or shared MCP exposure. Operators may still expose generated or experimental Cards. The Card index is advisory guidance, not an enforcement gate.

## Claim boundary

Duplicate detection is heuristic. A flagged duplicate may be a valid variant. An unflagged generated Card may still overlap semantically. Only the operator decides what enters their local MCP Card index.
