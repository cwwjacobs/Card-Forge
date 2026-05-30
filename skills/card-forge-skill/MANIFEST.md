# Card Forge Skill Manifest

## Package

`card-forge-skill`

## Contents

```text
SKILL.md
README.md
scripts/card_forge_skill.py
schemas/generated_card.schema.json
examples/card_registry.example.jsonl
examples/tiny_source/README.md
examples/expected_outputs/
```

## Validation performed

```bash
python3 -m py_compile skills/card-forge-skill/scripts/card_forge_skill.py
python3 skills/card-forge-skill/scripts/card_forge_skill.py \
  --source skills/card-forge-skill/examples/tiny_source \
  --registry skills/card-forge-skill/examples/card_registry.example.jsonl \
  --out skills/card-forge-skill/examples/expected_outputs
```

Expected result:

```text
PASS: Card Forge Skill completed.
```

## Boundary

This Skill generates usable Cards. It does not require canonicalization. Operators may use Cards immediately, edit them, group them, index trusted ones on MCP, or ignore them.
