# Instructions for coding agents

This repository follows the engineering protocol in [`docs/agent/PROTOCOL.md`](docs/agent/PROTOCOL.md). In short:
understand before changing, explain before implementing, verify before declaring completion, document before ending.

**At the start of every session:** read [`docs/agent/Handover.md`](docs/agent/Handover.md), then
[`docs/agent/Constraints.md`](docs/agent/Constraints.md); inspect `git status` and `git log`.
**At the end:** update `Handover.md` with what is actually true.

Quick facts
- Run everything: `python main.py` (quick projects), `python main.py --list`, `python main.py --all`. Flow: [`docs/agent/Flow.md`](docs/agent/Flow.md).
- The committed notebooks must keep their stored outputs; the runner writes copies to `*/results/executed/`.
- Never commit `_review/`, `course-material/`, `run_logs/`. Do not commit or push without the owner's explicit instruction.
- Docs in `docs/agent/`: Flow, Decisions, Constraints, Testing, Handover.
