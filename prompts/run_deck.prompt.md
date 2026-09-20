# Run Deck Prompt

Use this when a Deck needs to be executed against real source material.

## Prompt

Given a Deck, Run State, available Cards, and source material, play the current Card and update the Run.

Return:

- Card played,
- input seen,
- output created,
- status,
- warnings,
- blockers,
- next action,
- receipt update.

If the Card requires human approval, stop and request it instead of continuing.
