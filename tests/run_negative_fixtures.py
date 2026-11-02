#!/usr/bin/env python3
"""Run the Card Forge negative-fixture suite standalone.

Each fixture under ``tests/negative/`` is applied to a temporary copy of the
repository; the suite passes when the validator rejects every mutated copy.
This is the same functional check that ``scripts/validate_card_forge.py``
runs and reports separately from the overall validator pass.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_card_forge  # noqa: E402


def main() -> None:
    results, suite_error = validate_card_forge.run_negative_fixtures(ROOT)
    if suite_error:
        print(f"FAIL: {suite_error}", file=sys.stderr)
        raise SystemExit(1)
    failed = 0
    for result in results:
        if result["passed"]:
            print(f"PASS: {result['name']}: {result['description']}")
        else:
            failed += 1
            print(f"FAIL: {result['name']}: {result['detail']}")
    print(f"Functional checks (negative fixtures): {len(results) - failed} passed, {failed} failed.")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
