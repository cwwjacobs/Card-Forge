# Card Standard

A Card is one reusable workflow move that can be played during a Run and leave evidence behind.

## Minimum Card rule

A Card must tell an agent:

1. what to do
2. what to use
3. what to produce
4. when to stop
5. what to record

## Minimum Card fields

```yaml
card_id: ""
name: ""
type: ""
status: ""
input: ""
move: ""
output: ""
done_when: ""
stop_if: ""
receipt: ""
```

## Optional fields

```yaml
permissions: ""
used_in_decks: []
risk_level: ""
token_size: ""
source_origin: ""
maturity: ""
model_compatibility: []
requires: []
unlocks: []
```

## Card types

- **Action Card**: performs one bounded workflow action.
- **Check Card**: checks a condition or artifact.
- **Code Card**: reads, writes, patches, scans, runs, or validates code.
- **Prompt Card**: provides a reusable LLM instruction.
- **Contract Card**: applies a rule or boundary to the Run.
- **Gate Card**: makes a continue, stop, fix, or ready decision.
- **Receipt Card**: records what happened.
- **Template Card**: provides a reusable output shape.
- **Adapter Card**: converts one input shape into another.

## Card boundary

A Card is useful when it is:

- bounded
- repeatable
- playable
- receiptable

A Card is too small when it is only an obvious instruction, such as `use markdown` or `add a heading`.

A Card is too big when it contains multiple phases, such as `fix the whole app` or `build the product`.

## Canon line

A Card is not a thought, a tiny instruction, or a whole project.

A Card is one reusable workflow move with an output and a receipt.
