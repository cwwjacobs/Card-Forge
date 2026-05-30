# Run a Deck Prompt

Use this when executing a Deck on real material.

```text
You are running a Deck.

Deck:
{{deck}}

Run State:
{{run_state}}

Current Card:
{{current_card}}

Input material:
{{input_material}}

Play only the current Card.

Return:
- what input was seen
- what output was created
- whether the Card passed, warned, blocked, or failed
- receipt entry
- next action

Do not skip ahead unless the Deck says to. Stop if the Card stop condition appears.
```
