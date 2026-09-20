# Card Stack Standard

A Card Stack is an ordered group of Cards inside a Deck.

## Minimum Card Stack fields

```yaml
stack_id: ""
name: ""
cards_in_order: []
entry_condition: ""
exit_condition: ""
failure_route: ""
```

## Stack responsibilities

A Card Stack should define:

- when the Stack starts
- which Cards are played
- what order they are played in
- what output means the Stack is complete
- where the Run goes if a Card fails or blocks

## Edge rule

A Card Stack should be explicit enough that an edge agent can answer:

```text
What Card do I play now?
What do I produce?
Do I continue or stop?
```

## Boundary

If a Stack has too many phases or goals, it should become multiple Stacks.

If it has only one meaningful move, it may just be a Card.
