# Run Standard

A Run is an execution of a Deck on real material.

## Minimum Run State

```json
{
  "run_id": "",
  "deck_id": "",
  "current_stack": "",
  "current_card": "",
  "status": "READY",
  "inputs": [],
  "outputs": [],
  "next_action": "",
  "receipt_path": ""
}
```

## Run statuses

- `READY`
- `RUNNING`
- `BLOCKED`
- `NEEDS_SOURCE`
- `NEEDS_HUMAN`
- `PASS`
- `PASS_WITH_WARNINGS`
- `FAIL`

## Runtime rule

A Run should always know:

- what Deck is being run
- what Stack is active
- what Card is active
- what inputs are being used
- what outputs have been produced
- what happens next
- where the Receipt is written

## Checkpoint Receipts

For edge agents, receipts are not only proof. They are memory replacement.

Each played Card should record:

- Card played
- input seen
- output created
- status
- warning or blocker
- next action

## Final Receipt

A final Receipt should summarize:

- what was processed
- what passed
- what failed
- what was skipped
- what still needs source or human decision
- what the next action should be
