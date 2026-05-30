# Draw a Card Prompt

Use this when choosing existing Cards for a task.

```text
You are drawing Cards from a Card Collection.

Task:
{{task}}

Available Card Stubs:
{{card_stubs}}

Choose 3-7 Cards that are most useful for this task.

For each Card, return:
- card_id
- name
- why it was drawn
- whether it should be loaded now or placed on the bench

Do not invent new Cards unless no existing Card fits. If no Card fits, say which kind of Card should be cut next.
```
