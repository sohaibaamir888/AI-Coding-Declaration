"""Output helpers for aideclare.

- Build commit trailers.
- Optionally append to .git/COMMIT_EDITMSG (explicit opt-in).
- Optionally write structured YAML file locally.
- Validation is structural only (presence and allowed values).
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Dict, List, Optional

from .config import AppConfig

MATERIAL_VALUES = {"yes": True, "no": False, "unknown": "unknown"}
ASSISTANCE_ALLOWED = {"generation", "refactor", "suggestion", "test_generation", "unknown"}


def build_trailers(material_answer: str, assistance_types: List[str], tool: str) -> List[str]:
    trailers = [f"ai-assisted: {material_answer}"]
    if assistance_types:
        trailers.append(f"ai-assistance-type: {','.join(assistance_types)}")
    if tool:
        trailers.append(f"ai-tool: {tool}")
    return trailers


def append_to_commit_message(trailers: List[str]) -> None:
    commit_msg = Path(".git/COMMIT_EDITMSG")
    if not commit_msg.exists():
        print("COMMIT_EDITMSG not found; printing trailers only.")
        for line in trailers:
            print(line)
        return

    try:
        with commit_msg.open("a", encoding="utf-8") as fh:
            fh.write("\n" + "\n".join(trailers) + "\n")
    except Exception:
        # Never block; fall back to stdout
        print("Could not append to COMMIT_EDITMSG; printing trailers instead.")
        for line in trailers:
            print(line)


def validate_structural(material_answer: str, assistance_types: List[str], schema_version: str) -> Optional[str]:
    if material_answer not in MATERIAL_VALUES:
        return "Invalid materially_influenced value."
    unknowns = [a for a in assistance_types if a not in ASSISTANCE_ALLOWED]
    if unknowns:
        return f"Invalid assistance_type entries: {', '.join(unknowns)}"
    if schema_version != "1.0":
        return "Unsupported schema_version; expected '1.0'."
    return None


def build_structured_payload(
    material_answer: str,
    assistance_types: List[str],
    tool: str,
    declared_by: str,
    declared_at: Optional[str],
    schema_version: str,
) -> Dict:
    validation_error = validate_structural(material_answer, assistance_types, schema_version)
    if validation_error:
        print(validation_error)

    payload = {
        "ai_assistance": {
            "materially_influenced": MATERIAL_VALUES.get(material_answer, "unknown"),
            "assistance_type": assistance_types or None,
            "tool": tool or None,
            "declared_by": declared_by,
            "declared_at": declared_at
            or _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "schema_version": schema_version,
        }
    }
    return payload


def write_structured_file(payload: Dict, path: str) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Manual YAML serialization to avoid extra dependencies.
    ai = payload.get("ai_assistance", {})
    lines = ["ai_assistance:"]
    lines.append(f"  materially_influenced: {str(ai.get('materially_influenced')).lower()}")
    assistance = ai.get("assistance_type")
    if assistance:
        lines.append("  assistance_type:")
        for item in assistance:
            lines.append(f"    - {item}")
    else:
        lines.append("  assistance_type: []")
    tool = ai.get("tool")
    lines.append(f"  tool: {tool if tool is not None else 'null'}")
    lines.append(f"  declared_by: {ai.get('declared_by')}")
    lines.append(f"  declared_at: {ai.get('declared_at')}")
    lines.append(f"  schema_version: \"{ai.get('schema_version')}\"")

    try:
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except Exception:
        print(f"Could not write structured file at {out_path}")

