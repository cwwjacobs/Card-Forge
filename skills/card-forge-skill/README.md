# Card Forge Skill

A drop-in Card Forge Skill for turning messy source material into usable Cards.

## What it does

```text
source material -> generated Cards -> worklist + duplicate report + receipt
```

Generated Cards are usable Cards. Operators may use them immediately, edit them, group them into Stacks, add them to Decks, or index trusted ones later.

## Quick run

```bash
python3 skills/card-forge-skill/scripts/card_forge_skill.py --source skills/card-forge-skill/examples/tiny_source --out _card_forge_out
```

With an existing Card registry/index:

```bash
python3 skills/card-forge-skill/scripts/card_forge_skill.py \
  --source skills/card-forge-skill/examples/tiny_source \
  --registry skills/card-forge-skill/examples/card_registry.example.jsonl \
  --out _card_forge_out
```

## Recommended MCP strategy

We recommend putting only trusted/tested/indexed Cards on shared or public MCP servers. Card Forge does not enforce that. Operators can expose generated or experimental Cards through private/dev MCP if they clearly label them.
