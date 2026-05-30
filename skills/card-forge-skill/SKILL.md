# Card Forge Skill

## Purpose

Card Forge Skill scans an old repo, folder, source bundle, notes bundle, prompt log, or build artifact and extracts **all discoverable Card-sized reusable moves**.

It emits the results as **individual candidate Cards**.

It does not emit a Card Stack by default.
It does not emit a Deck by default.
It does not promote Cards to canon by default.

## Core output

For each discovered Card candidate, produce:

1. one Card markdown file
2. one registry JSONL line
3. one extraction note in the run receipt

The skill also produces one overall Card Forge receipt for the extraction run.

## Card boundary

A valid Card candidate must be:

- bounded
- repeatable
- playable
- receiptable

Reject or resize anything that is too vague, too tiny, too large, private, unsupported, or only useful once.

## Card types

Choose one primary type for each Card:

- Action Card
- Check Card
- Code Card
- Prompt Card
- Contract Card
- Gate Card
- Receipt Card
- Template Card
- Adapter Card

## Required Card fields

Every emitted Card must include:

```yaml
card_id: ""
name: ""
type: ""
status: "candidate"
input: ""
move: ""
output: ""
done_when: ""
stop_if: ""
receipt: ""
```

## Extraction rule

The skill should prefer **many clean single Cards** over one oversized Card.

Bad:

```text
Repo Audit Stack
```

Good:

```text
Source Inventory Card
Dependency Surface Card
JSON Validate Card
Readme Claim Boundary Card
Final Receipt Card
```

## Run outputs

A normal run should write:

```text
_card_forge_out/
  cards/
    <card_id>.card.md
  registry_card_candidates.jsonl
  receipts/
    card_forge_extraction_receipt.md
```

## Operator approval

New Cards are `candidate` status.

Only the operator may approve a Card as `canon`.

## Publishing guidance

Card Forge recommends canon-ledgered Cards for public or shared MCP exposure. Operators may still share candidate or experimental Cards. The canon ledger is advisory, not an enforcement gate.

## Local helper

Run from the repository root or any folder with Python 3:

```bash
python3 skills/card-forge-skill/card_forge_skill.py --source <repo-or-folder> --out _card_forge_out
```

The helper uses standard-library heuristics to extract candidate Cards from visible files. A model or operator should review the candidates before adding them to the canonical registry.
