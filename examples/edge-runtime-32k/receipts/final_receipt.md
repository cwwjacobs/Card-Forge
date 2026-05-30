# Final Receipt: Edge Runtime 32k Demo

Run ID: `run.edge_runtime_32k.demo_001`
Deck ID: `deck.ai_build_preflight.v0_1`
Stack ID: `stack.intake.compiled.v0_1`
Status: `PASS`

## Input seen

- `example index.html`
- `example main.js`

## Cards played

| Card | Status | Output | Notes |
|---|---|---|---|
| `check.source_inventory.v0_1` | `PASS` | `source_inventory.md` | Source material inventoried. |
| `contract.no_overclaim.v0_1` | `PASS` | `allowed_claims_and_blocked_claims.md` | No overclaims found at intake. |

## Outputs created

- `source_inventory.md`
- `allowed_claims_and_blocked_claims.md`

## Warnings

- This is a compiled Stack demo. Not all Deck Stacks were run.
- Edge runtime compatibility is a structural claim, not a model-capability claim.

## Blockers

- None.

## Not checked

- Security
- Compliance
- Production readiness
- Full runtime correctness

## Next action

If the full Deck is required, continue to `stack.structure_check.v0_1`. If only the intake slice was needed, this Run is complete.

## Claim boundary

This receipt records what this compiled Stack checked. It does not guarantee correctness, security, compliance, bug-free code, or production readiness. 32k compatibility means the run packet is designed to fit in 32k tokens; it does not guarantee reliable execution on any specific edge model.
