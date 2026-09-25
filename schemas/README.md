# Schemas

These JSON Schema files are reference contracts for Card Forge objects.

They describe the expected shape of:

- Cards
- Decks
- Run States
- Receipts

## Current validation boundary

`python3 scripts/validate_card_forge.py` is intentionally standard-library only. No JSON Schema package is a repo dependency, so the validator implements the needed JSON Schema subset (`type`, `enum`, `required`, `properties`, `items`, `additionalProperties`) in stdlib Python.

It validates every record in the repository against these schemas:

- Cards: registry JSONL records and `*.card.md` frontmatter against `card.schema.json`; generated Card examples against `skills/card-forge-skill/schemas/generated_card.schema.json`.
- Stacks and Decks: parsed from their structured Markdown files against `stack.schema.json` and `deck.schema.json`.
- Run States: the JSON Run State files against `run.schema.json`, with statuses restricted to the `RUN_STANDARD.md` set.
- Receipts: Run Receipt Markdown files against `receipt.schema.json`. Each played Card yields one checkpoint record per `RUN_STANDARD.md`. Extraction rules: an absent `Warnings`/`Blockers` section means none were recorded (empty list); `Outputs created` and `Output created` both map to `output_created`; a `Cards played` table produces one record per row, otherwise the `Card ID` header field is `card_played`.

It also enforces cross-reference integrity: Deck→Stack→Card references resolve, and every Run's `receipt_path` exists and declares that Run's `run_id`.

Negative fixtures under `tests/negative/` prove the validator rejects wrong types/ranges, missing required fields, dangling references, duplicate IDs, and invalid Run states. Their counts are functional checks reported separately from the validator pass.
