# Card Index

This is the human-readable index of known Cards.

The source of truth is `registry/card_registry.jsonl`. If this index and the registry disagree, the registry wins.

## Indexed Cards

| Card ID | Name | Type | Status | Use |
|---|---|---|---|---|
| `check.source_inventory.v0_1` | Source Inventory | Check Card | indexed | Start a Run by listing and classifying source material. |
| `contract.no_overclaim.v0_1` | No Overclaim | Contract Card | indexed | Prevent unsupported readiness, safety, or production claims. |
| `gate.human_approval.v0_1` | Human Approval Gate | Gate Card | indexed | Pause before risky actions or index changes. |
| `check.blocker_report.v0_1` | Blocker Report | Check Card | indexed | List blockers that prevent the current Run from continuing cleanly. |
| `prompt.repair_prompt.v0_1` | Repair Prompt | Prompt Card | indexed | Write a focused repair prompt for the listed blockers without expanding scope. |
| `receipt.readiness_receipt.v0_1` | Readiness Receipt | Receipt Card | indexed | Produce a bounded readiness receipt for the current Run. |

## Status levels

- `generated`: newly made Card
- `reviewed`: operator/model reviewed for shape and usefulness
- `trusted`: operator has tried it and trusts it for their own use
- `indexed`: added to a local MCP/Card index
- `deprecated`: replaced or no longer recommended
- `rejected`: explicitly not useful, unsafe, or duplicate
