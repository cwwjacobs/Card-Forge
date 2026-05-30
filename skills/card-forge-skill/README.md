# Card Forge Skill

Card Forge Skill scans an old repo, folder, file, notes bundle, or build artifact and emits **multiple individual candidate Cards**.

It does not build a Stack or Deck by default.

## Run

From the repo root:

```bash
python3 skills/card-forge-skill/card_forge_skill.py --source . --out _card_forge_out
```

For a different repo or folder:

```bash
python3 skills/card-forge-skill/card_forge_skill.py --source /path/to/old/repo --out _card_forge_out
```

## Output

```text
_card_forge_out/
  cards/
    <card_id>.card.md
  registry_card_candidates.jsonl
  receipts/
    card_forge_extraction_receipt.md
```

## Review rule

All emitted Cards are `candidate` status.

Review before adding to `registry/card_registry.jsonl`.

Only operator-approved Cards should become `canon`.

## Card Maker flow

Step 1: **Card Forge Skill** emits candidate Cards.

```bash
python3 skills/card-forge-skill/card_forge_skill.py --source . --out _card_forge_out
```

Step 2: **Card Maker** checks duplicate risk against the canon ledger (`registry/card_registry.jsonl`) and emits a promotion worklist.

```bash
python3 skills/card-forge-skill/card_maker.py \
  --candidates _card_forge_out/registry_card_candidates.jsonl \
  --registry registry/card_registry.jsonl \
  --out _card_maker_out
```

Step 3: **Operator** manually reviews the worklist and approves canon Cards.

Card Maker does not auto-canonize. See `CARD_MAKER.md` for details.
