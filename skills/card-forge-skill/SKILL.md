# Card Forge Skill

## Purpose

Use this Skill when the user wants to turn messy source material into usable Card Forge Cards.

This Skill accepts old repos, folders, notes, prompt logs, app folders, audit reports, workflow descriptions, prior conversation captures, or failed-build artifacts and emits Card Forge Cards that can be used immediately, edited, grouped into Stacks, added to Decks, or indexed later.

A generated Card is a real usable Card. It does not need to be indexed before use.

## Core operating rule

Card Forge makes usable Cards.

Operators may keep a trusted local MCP/Card index for Cards they have tried and trust. In our workflow, that local MCP Card index is our trusted list. This is recommended for shared/public MCP servers, but it is not mandatory.

Do not block use of a generated Card just because it has not been indexed.

## When to use

Use this Skill when asked to:

- make Cards from a repo, folder, or old project
- cut reusable Cards from notes or prompt logs
- turn repeated process into Card Forge Cards
- extract Cards from a conversation or audit report
- prepare Cards for a Deck or Stack
- check generated Cards against an existing Card registry/index
- make a Card index worklist without forcing indexing or MCP publishing

## Inputs

Useful inputs include:

- source folder or source file
- optional existing Card registry/index JSONL
- optional desired Card type focus
- optional output folder
- optional max Card count

## Outputs

A normal run emits:

```text
_card_forge_out/
  cards/
    <card_id>.card.md
  card_index_worklist.jsonl
  duplicate_report.md
  suggested_stacks.md
  receipts/
    card_making_receipt.md
  run_manifest.json
```

## Card boundary

A good Card must be:

- bounded
- repeatable
- playable
- receiptable
- useful more than once

Reject or resize anything that is:

- too vague
- too tiny
- too broad
- only useful once
- secretly a whole Stack or Deck
- dependent on private context that is not included
- making claims stronger than its evidence supports

## Card types

Choose one primary type:

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

Every generated Card must include:

```yaml
card_id: ""
name: ""
type: ""
status: "generated"
input: ""
move: ""
output: ""
done_when: ""
stop_if: ""
receipt: ""
permissions: []
risk_level: "low | medium | high | critical"
token_size: "small | medium | large"
source_origin: ""
```

## Status language

Use simple status labels:

- `generated` — newly made Card
- `reviewed` — operator/model reviewed for shape and usefulness
- `trusted` — operator has tried it and trusts it for their own use
- `indexed` — added to an MCP/Card index
- `deprecated` — replaced or no longer recommended

Avoid wording that makes generated Cards sound unusable or not-a-card.

## MCP/Card index guidance

Card Forge does not require operators to index Cards before using them.

Recommended strategy:

- use generated Cards locally as needed
- review and test useful Cards
- add trusted Cards to a local MCP/Card index for agents
- clearly label experimental/dev Cards if exposed through MCP
- reserve shared/public MCP indexes for Cards the operator has tried and trusts

## Process

### 1. Inventory the source

List available material, missing context, and source type.

Stop only if there is no usable source material.

### 2. Find reusable moves

Look for reusable checks, actions, prompts, gates, receipts, templates, adapters, transforms, validation steps, context compression moves, and human approval points.

Prefer many clean Cards over one oversized Card.

### 3. Cut Cards

For each reusable move, produce one Card.

Each Card should answer:

- What does it take in?
- What does it do?
- What does it produce?
- When is it done?
- When should it stop?
- What receipt/proof does it leave?

### 4. Check existing Card registry/index

If an existing registry/index is provided, compare generated Cards against it.

Flag likely overlap by:

- same or similar card_id
- same or similar name
- same type and output
- same type and move

Do not block the Card. Warn the operator.

### 5. Emit worklist and receipt

Emit Cards, a JSONL worklist, duplicate report, suggested Stack groupings, and a receipt.

## Helper script

Run from the Skill folder or repo root:

```bash
python3 skills/card-forge-skill/scripts/card_forge_skill.py --source <source-folder-or-file> --out _card_forge_out
```

With an existing registry/index:

```bash
python3 skills/card-forge-skill/scripts/card_forge_skill.py \
  --source <source-folder-or-file> \
  --registry registry/card_registry.jsonl \
  --out _card_forge_out
```

## Final response behavior

When using this Skill, summarize:

```text
Generated Cards:
- total:
- use-now:
- needs edit:
- likely duplicate:
- suggested Stack groupings:
- suggested MCP/index options:
- warnings:
```

Never claim that generated Cards are guaranteed correct, safe, or production-ready.
