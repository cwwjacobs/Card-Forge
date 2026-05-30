# Card Forge Skill

Card Forge Skill scans an old repo, folder, file, notes bundle, or build artifact and emits **multiple individual generated Cards**.

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
  registry_card_generated.jsonl
  receipts/
    card_forge_extraction_receipt.md
```

## Review rule

All emitted Cards are newly generated.

Review before adding to `registry/card_registry.jsonl`.

Only operator-approved Cards should be indexed for MCP use.

## Card Maker / Card Index flow

Step 1: **Card Forge Skill** emits generated Cards.

```bash
python3 skills/card-forge-skill/card_forge_skill.py --source . --out _card_forge_out
```

Step 2: **Card Maker** checks duplicate risk against the existing Card registry (`registry/card_registry.jsonl`) and emits a review worklist.

```bash
python3 skills/card-forge-skill/card_maker.py \
  --candidates _card_forge_out/registry_card_generated.jsonl \
  --registry registry/card_registry.jsonl \
  --out _card_maker_out
```

Step 3: **Operator** manually reviews the worklist and decides which Cards to index, publish, or keep private.

Card Maker does not auto-approve. See `CARD_MAKER.md` for details.

## Publishing guidance

Card Forge recommends **trusted/indexed Cards** for public or shared MCP exposure. Operators may still share **generated or experimental Cards** if they choose. The Card index is advisory guidance, not an enforcement gate.
