# Card Index

This is the human-readable index of known Cards.

The source of truth is `registry/card_registry.jsonl`. If this index and the registry disagree, the registry wins.

## Canon Cards

| Card ID | Name | Type | Status | Use |
|---|---|---|---|---|
| `check.source_inventory.v0_1` | Source Inventory | Check Card | canon | Start a Run by listing and classifying source material. |
| `contract.no_overclaim.v0_1` | No Overclaim | Contract Card | canon | Prevent unsupported readiness, safety, or production claims. |
| `gate.human_approval.v0_1` | Human Approval Gate | Gate Card | canon | Pause before risky actions or canon changes. |
| `check.blocker_report.v0_1` | Blocker Report | Check Card | canon | List blockers that prevent the current Run from continuing cleanly. |
| `prompt.repair_prompt.v0_1` | Repair Prompt | Prompt Card | canon | Write a focused repair prompt for the listed blockers without expanding scope. |
| `receipt.readiness_receipt.v0_1` | Readiness Receipt | Receipt Card | canon | Produce a bounded readiness receipt for the current Run. |

## Status levels

- `candidate`: may become a Card
- `cut`: extracted as a rough Card
- `forged`: cleaned into valid Card shape
- `canon`: approved reusable owned Card
- `deprecated`: replaced or retired
- `rejected`: explicitly not useful, unsafe, or duplicate
