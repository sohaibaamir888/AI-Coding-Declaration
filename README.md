# AI Coding Declaration

> **IMPORTANT:** This project records human declarations only. It does **not** produce compliance artifacts, audit evidence, attestations, certifications, or governance decisions. Any use of the data for regulatory, contractual, procurement, or audit purposes requires separate systems and explicit human authority.

## Purpose
A neutral, low-friction standard for developers to declare whether AI materially influenced a code change. It improves declaration hygiene without governing, enforcing, evaluating, certifying, or concluding anything about software development.

## Problem Statement
- Declarations are inconsistent or missing
- Answers are often reconstructed under pressure
- Developers fear over-disclosure
- No standard, neutral format exists

This project captures declarations only; it does **not** interpret them.

## Scope (Hard Boundaries)
- **Does:** capture human-declared facts about AI assistance; standardize representation; reduce friction; produce structured metadata.
- **Does NOT:** detect AI-generated code; infer AI usage; evaluate correctness or quality; assign responsibility; create attestations; guarantee completeness; claim audit, regulatory, or compliance readiness.

## Explicit Non-Goals (Non-Negotiable)
This project will never:
- Generate documents or exports for third-party review (auditors, regulators, procurement, customers)
- Provide questionnaire-ready answers or summaries
- Encode approvals, sign-offs, responsible parties, policy constraints, or exceptions
- Function as a system of record or source of authority

If a feature implies any of the above, it is forbidden.

## Core Concept
At commit or pull-request time, a developer is asked one question:

> **Did AI materially influence this change?**

The answer is recorded as structured metadata. The declaration reflects developer intent only. It does **not** imply approval, acceptance, correctness, or compliance.

## Terminology
- **AI assistance:** any AI tool that influenced code structure, logic, or behavior.
- **Material influence:** AI contributed logic, structure, or behavior that would not reasonably have been produced identically without the AI tool.
- **Declaration:** a human statement, not a verified fact.
- **Unknown:** valid when influence cannot be confidently determined.

## Operational Guidance (Non-Binding)
Typically material: AI-generated functions/logic, AI-suggested refactors adopted, AI-generated tests affecting behavior/coverage.

Typically non-material: formatting, renaming, trivial autocomplete, documentation-only changes. This guidance aids consistency only; it does not enforce correctness.

## Canonical Declaration Schema (v1.0)
```yaml
ai_assistance:
  materially_influenced: true | false | unknown
  assistance_type:
    - generation
    - refactor
    - suggestion
    - test_generation
    - unknown
  tool: string | null
  declared_by: string
  declared_at: ISO-8601 timestamp
  schema_version: "1.0"
```
Field semantics:
- `materially_influenced`: true (material AI influence), false (no material influence), unknown (unclear or mixed)
- `assistance_type`: descriptive only; optional; multiple values allowed; no evaluative meaning
- `tool`: free-form string; nullable
- `declared_by`: identifier of the declaring human
- `declared_at`: timestamp of declaration (not required to match commit time)
- `schema_version`: explicit versioning for forward compatibility

## Declaration Surfaces (Priority Order)
1. Pull Request description (preferred in PR-based workflows)
2. Git commit trailers
3. Structured declaration file

No surface is authoritative over others.

## Storage & Transport Formats
### Git commit trailers (primary)
```
ai-assisted: yes | no | unknown
ai-assistance-type: generation,refactor
ai-tool: github-copilot
```

### Structured file (optional)
Path: `.ai/ai-assistance.yaml`

Example:
```yaml
ai_assistance:
  materially_influenced: true
  assistance_type:
    - generation
  tool: github-copilot
  declared_by: sohaib
  declared_at: 2026-03-14T10:22:00Z
  schema_version: "1.0"
```

## Behavioral Principles
The system **MUST**:
- Allow skipping
- Allow `unknown`
- Never block commits or merges
- Never enforce truthfulness
- Never score or judge declarations
- Never transmit data externally

The system **MUST NOT**:
- Detect AI usage
- Override developer input
- Aggregate declarations
- Produce summaries or conclusions

## CLI Specification (`aideclare`)
- Runtime: Python 3.9+
- Invocation: `python -m cli.aideclare.main` or installed entrypoint `aideclare`
- Interactive flow:
  1. `Did AI materially influence this change? [yes / no / unknown]`
  2. `Which assistance type? (optional) [generation / refactor / suggestion / test_generation / unknown]`
  3. `Which tool? (optional)`
- Output behavior:
  - Writes commit trailers and/or structured file, controlled by local config or flags
  - Always exits successfully
  - Never blocks git actions

## Configuration
Local-only dotfile: `.aideclare.yaml`

Example:
```yaml
output:
  commit_trailer: true
  structured_file: false
  append_to_commit_message: false
paths:
  structured_file: .ai/ai-assistance.yaml
```
- No org-level policy, no remote config, no telemetry.

## Git Integration (Optional, Non-Enforcing)
- Non-blocking pre-commit reminder script (`git/pre-commit-reminder.sh`)
- Commit message template snippet (`git/commit-template.txt`)
- Manual invocation by default
- Explicit non-features: no enforced hooks, no CI gating, no merge blocking

## Explicit Non-Goals (Reiterated)
- No detection of AI usage
- No evaluation of correctness or quality
- No responsibility assignment
- No attestations or compliance positioning
- No governance or authority claims

## Examples
- See `examples/commit-message.txt` for commit trailers
- See `examples/ai-assistance.yaml` for the structured file example

## Testing
- Lightweight manual checks only (run the CLI, inspect trailers/file)
- **No automated tests that enforce declaration presence or correctness**

## Design Philosophy (Final)
This project captures what developers say happened. It does not decide what that means.

_Final grounding sentence: This OSS normalizes declaration. Vantys formalizes responsibility._
