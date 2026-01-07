# Contributing to AI Coding Declaration

Thanks for considering a contribution! This project is intentionally minimal and non-enforcing. Please keep changes aligned with these principles:

- **No compliance, audit, or governance positioning.**
- **No enforcement:** do not add CI gating, required hooks, or blockers.
- **Local-only configuration:** keep settings in `.aideclare.yaml`; avoid org-wide policy mechanisms.
- **Schema validation is structural only:** allowed values and presence; no semantic or behavioral checks.
- **Runtime:** Python 3.9+ only.

## Development quickstart
1. Create a virtual environment (optional): `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies (currently standard library only).
3. Run the CLI interactively: `python -m cli.aideclare.main`
4. Inspect output: commit trailers printed to stdout; structured file written locally if configured.

## Code style
- Prefer standard library only; minimize dependencies.
- Keep CLI prompts and outputs exactly as specified in the README.
- Avoid complex abstractions; prioritize clarity and determinism.

## Tests
- Manual, lightweight checks only.
- Do **not** add tests that enforce declaration presence or correctness.

## Pull requests
- Describe how your change respects the non-goals and non-enforcement stance.
- Avoid marketing or enterprise-readiness language.
