# Forge a Card Prompt

Use this when cleaning a rough Card into the Card Standard.

```text
You are forging a rough Card into a valid Card.

Rough Card:
{{rough_card}}

Card Standard:
A Card must define what to do, what to use, what to produce, when to stop, and what to record.

Return a valid Card with:
- card_id
- name
- type
- status
- input
- move
- output
- done_when
- stop_if
- receipt
- permissions
- risk_level
- token_size
- source_origin

If the rough Card is too broad, split it.
If it is too small, merge it into a larger Card.
If it cannot leave a receipt, reject it.
```
