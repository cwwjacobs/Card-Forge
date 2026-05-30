# Build a Deck Prompt

Use this when arranging Cards into a reusable Deck.

```text
You are building a Deck from available Cards.

Deck goal:
{{deck_goal}}

Available Cards:
{{cards}}

Create:
- deck_id
- name
- purpose
- Card Stacks in order
- Cards inside each Stack
- entry and exit conditions
- allowed permissions
- expected Run outputs
- final gate
- claim boundary

Keep the Deck edge-runnable when possible. Prefer clear order, small outputs, stop conditions, and receipts.
```
