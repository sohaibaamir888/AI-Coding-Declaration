"""Configuration loader for aideclare.

- Local-only dotfile: .aideclare.yaml
- Structural parsing only; defaults are permissive and non-enforcing.
- Importing PyYAML is optional; if unavailable, config parsing is skipped and defaults are used.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - dependency-free fallback
    yaml = None


@dataclass
class AppConfig:
    commit_trailer: bool = False
    structured_file: bool = False
    append_to_commit_message: bool = False
    structured_file_path: str = ".ai/ai-assistance.yaml"
    schema_version: str = "1.0"


DEFAULT_CONFIG = AppConfig()


def load_config(path: Optional[str] = None) -> AppConfig:
    """Load configuration from a local dotfile.

    If the file is missing or PyYAML is unavailable, return defaults.
    """
    config_path = Path(path or ".aideclare.yaml")
    if not config_path.exists() or yaml is None:
        return DEFAULT_CONFIG

    try:
        with config_path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except Exception:
        return DEFAULT_CONFIG

    output = data.get("output", {}) if isinstance(data, dict) else {}
    paths = data.get("paths", {}) if isinstance(data, dict) else {}
    defaults = data.get("defaults", {}) if isinstance(data, dict) else {}

    return AppConfig(
        commit_trailer=bool(output.get("commit_trailer", DEFAULT_CONFIG.commit_trailer)),
        structured_file=bool(output.get("structured_file", DEFAULT_CONFIG.structured_file)),
        append_to_commit_message=bool(
            output.get("append_to_commit_message", DEFAULT_CONFIG.append_to_commit_message)
        ),
        structured_file_path=str(paths.get("structured_file", DEFAULT_CONFIG.structured_file_path)),
        schema_version=str(defaults.get("schema_version", DEFAULT_CONFIG.schema_version)),
    )

