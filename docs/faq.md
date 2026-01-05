# FAQ

**Does this tool prove compliance or provide audit evidence?**
No. It records human declarations only and explicitly avoids compliance or audit positioning.

**What happens if I skip or choose `unknown`?**
Nothing. Skipping and `unknown` are valid. The CLI always exits successfully and never blocks git actions.

**Does the tool detect AI usage?**
No. It captures what developers declare; it does not detect or infer usage.

**Where are declarations stored?**
Optionally in git commit trailers and/or a local structured file at `.ai/ai-assistance.yaml`, controlled by local config or flags.

**Is there telemetry or remote config?**
No. Configuration is local-only via `.aideclare.yaml`. No network calls are made.

**Can I use this as a system of record?**
No. This project is informational only and not a source of authority or responsibility assignment.
