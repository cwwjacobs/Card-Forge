# Card Maker

Card Maker reviews candidate Cards produced by the Card Forge Skill.

## Purpose

Card Forge Skill cuts candidate Cards from source material. Card Maker checks those candidates against the canonical ledger and emits:

- a **duplicate report**
- a **promotion worklist**

## Canon ledger

`registry/card_registry.jsonl` is the canon ledger. It contains only operator-approved Cards with `status: canon`.

## What Card Maker does

1. Read candidate Cards from a JSONL file (usually `_card_forge_out/registry_card_candidates.jsonl`).
2. Read the canonical ledger (`registry/card_registry.jsonl`).
3. Detect duplicates by:
   - exact `card_id` match
   - exact normalized name match
   - same normalized move text
4. Flag promotion candidates that are not duplicates.
5. Warn on name overlap, move overlap, short fields, or unexpected status.

## What Card Maker does NOT do

- **Auto-canonize.** Card Maker never changes `candidate` to `canon`.
- **Guarantee completeness.** Duplicate detection is heuristic, not proof.

## Operator approval

Only the operator may promote a Card to `canon`.

The promotion worklist explains the steps:

1. Read the candidate Card file.
2. Check that it is bounded, repeatable, playable, and receiptable.
3. If warnings are listed, resolve them first.
4. Only then change `status` from `candidate` to `canon`.
5. Append the approved record to `registry/card_registry.jsonl`.

## Run

From the repo root:

```bash
python3 skills/card-forge-skill/card_maker.py \
  --candidates _card_forge_out/registry_card_candidates.jsonl \
  --registry registry/card_registry.jsonl \
  --out _card_maker_out
```

Or through the wrapper:

```bash
python3 scripts/card_maker.py \
  --candidates _card_forge_out/registry_card_candidates.jsonl \
  --registry registry/card_registry.jsonl \
  --out _card_maker_out
```

## Output

```text
_card_maker_out/
  duplicate_report.md
  promotion_worklist.md
  promotion_worklist.jsonl
```

## Claim boundary

Duplicate detection is heuristic. A flagged duplicate may be a valid variant. An unflagged candidate may still overlap semantically. Only the operator decides what enters the canon ledger.
