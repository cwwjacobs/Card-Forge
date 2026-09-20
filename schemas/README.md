# Schemas

These JSON Schema files are reference contracts for Card Forge objects.

They describe the expected shape of:

- Cards
- Decks
- Run States
- Receipts

## Current validation boundary

`python3 scripts/validate_card_forge.py` is intentionally standard-library only. It checks that schema files exist and declare an object shape with required fields. It also performs hand-rolled validation for the committed registry, Card frontmatter, Run State examples, Python script compile health, and receipt references.

It does **not** currently run a full JSON Schema validator against every Markdown or JSON instance in the repository.

## Operator rule

Treat these schemas as reference contracts unless and until a schema-enforcing validator is added. Do not claim full schema enforcement from the current validator output alone.

## Future hardening path

A later validator can add full instance validation by either:

1. adding a JSON Schema dependency such as `jsonschema`, or
2. expanding the standard-library validator with explicit per-object checks.

Until that happens, README and release language should say "reference schemas" rather than implying enforced schema compliance.
