# Cut a Card Prompt

Use this when extracting a rough Card from messy source material.

```text
You are cutting a reusable Card from messy source material.

Source material:
{{source_material}}

Find one bounded reusable workflow move.

Return a rough Card with:
- name
- likely type
- input
- move
- output
- done_when
- stop_if
- receipt
- source_origin

Do not cut a Card if the move is too vague, too small, too large, private, unsafe, or only useful once.
```
