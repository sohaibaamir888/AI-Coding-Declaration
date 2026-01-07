from __future__ import annotations

import argparse
import os
from typing import List

from . import prompts
from .config import AppConfig, load_config
from .writer import append_to_commit_message, build_structured_payload, build_trailers, write_structured_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record AI assistance declarations (non-enforcing).")
    parser.add_argument("--config", default=None, help="Path to .aideclare.yaml (optional)")
    parser.add_argument(
        "--write-commit-message",
        action="store_true",
        help="Append trailers to .git/COMMIT_EDITMSG (explicit opt-in).",
    )
    parser.add_argument(
        "--write-structured-file",
        action="store_true",
        help="Write the structured declaration file (explicit opt-in).",
    )
    parser.add_argument(
        "--declared-by",
        default=None,
        help="Optional declared_by value for structured file (defaults to USER or git config).",
    )
    parser.add_argument(
        "--declared-at",
        default=None,
        help="Optional ISO-8601 timestamp for structured file (defaults to current UTC).",
    )
    return parser.parse_args()


def resolve_declared_by(explicit: str | None) -> str:
    if explicit:
        return explicit
    return os.getenv("GIT_AUTHOR_NAME") or os.getenv("USER") or "unknown"


def run_with_config(config: AppConfig, args: argparse.Namespace) -> None:
    material_answer = prompts.ask_materially_influenced()
    assistance_types = prompts.ask_assistance_types()
    tool = prompts.ask_tool()

    trailers = build_trailers(material_answer, assistance_types, tool)
    print("\n".join(trailers))

    if args.write_commit_message or config.append_to_commit_message:
        append_to_commit_message(trailers)

    if args.write_structured_file or config.structured_file:
        payload = build_structured_payload(
            material_answer=material_answer,
            assistance_types=assistance_types,
            tool=tool,
            declared_by=resolve_declared_by(args.declared_by),
            declared_at=args.declared_at,
            schema_version=config.schema_version,
        )
        write_structured_file(payload, config.structured_file_path)


def run() -> None:
    args = parse_args()
    config = load_config(args.config)
    run_with_config(config, args)


if __name__ == "__main__":
    run()
