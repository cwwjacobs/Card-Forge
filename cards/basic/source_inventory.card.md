---
card_id: "check.source_inventory.v0_1"
name: "Source Inventory"
type: "Check Card"
status: "indexed"
input: "Files, pasted text, repo listing, or source bundle."
move: "List available source material and classify it by type."
output: "source_inventory.md"
done_when: "Source material is listed and grouped."
stop_if: "No source material is provided."
receipt: "Record files seen, files missing, and whether intake can continue."
permissions:
  - "read_only"
risk_level: "low"
token_size: "small"
source_origin: "Card Forge starter set"
---

# Source Inventory

## Input

Files, pasted text, repo listing, or source bundle.

## Move

List available source material and classify it by type.

## Output

`source_inventory.md`

## Done When

Source material is listed and grouped.

## Stop If

No source material is provided.

## Receipt

Record files seen, files missing, and whether intake can continue.

## Permissions

`read_only`
