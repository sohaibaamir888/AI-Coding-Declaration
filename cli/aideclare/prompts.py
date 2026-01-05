"""Interactive prompts for aideclare.

Prompts are deterministic and allow skipping/unknown values.
"""
from __future__ import annotations

from typing import List


MATERIAL_OPTIONS = {"yes", "no", "unknown"}
ASSISTANCE_TYPES = {"generation", "refactor", "suggestion", "test_generation", "unknown"}


def ask_materially_influenced(input_fn=input) -> str:
    while True:
        value = input_fn("Did AI materially influence this change? [yes / no / unknown]\n").strip().lower()
        if value in MATERIAL_OPTIONS:
            return value
        print("Please answer with: yes, no, or unknown.")


def ask_assistance_types(input_fn=input) -> List[str]:
    value = input_fn(
        "Which assistance type? (optional) [generation / refactor / suggestion / test_generation / unknown]\n"
    ).strip()
    if not value:
        return []
    parts = [item.strip().lower() for item in value.split(",") if item.strip()]
    return [p for p in parts if p in ASSISTANCE_TYPES]


def ask_tool(input_fn=input) -> str:
    return input_fn("Which tool? (optional)\n").strip()

