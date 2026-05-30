#!/usr/bin/env python3
"""Tiny wrapper that delegates to the Card Maker skill implementation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SKILL_PATH = Path(__file__).resolve().parents[1] / "skills" / "card-forge-skill" / "card_maker.py"

spec = importlib.util.spec_from_file_location("card_maker_skill", SKILL_PATH)
if spec is None or spec.loader is None:
    raise SystemExit(f"Could not load Card Maker skill from {SKILL_PATH}")

module = importlib.util.module_from_spec(spec)
sys.modules["card_maker_skill"] = module
spec.loader.exec_module(module)
module.main()
