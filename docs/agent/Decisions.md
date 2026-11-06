# Decision log

Dates 2026-11-06. Model identifier: the session ran on Claude models `claude-opus-5-5` and `claude-sonnet-5-5` (switched during the
session); which model took which decision is **unknown**. D1-D4 were chosen by the owner when approving the plan.

## D1 — A runner `main.py` instead of one monolithic script
- **Problem:** the repo holds five independent projects (3 scripts, 2 notebooks, 1 broken script). The owner asked for a single `main.py` to run "the whole project".
- **Alternatives:** (a) one script that imports and calls every project; (b) a runner that starts each as its own process; (c) no main.py.
- **Chosen:** (b). **Why:** the projects use relative `data/` paths and some are notebooks that cannot be imported; a subprocess with the project folder as working directory runs them exactly as the READMEs describe, and one failure cannot break the others.
- **Trade-off:** no shared in-process state (none is needed); start-up cost per project.

## D2 — Tiers: quick (default), heavy (`--all`), broken (skipped)
- **Why:** a "run all" that takes an hour or fails for a known reason is not useful as a default (owner chose "quick set by default").
- **Tiers come from real runs**, not guesses: 02 was first expected to be *heavy* (SARIMA on 35k points) but it fails within 27 s, so it is *broken* (Testing T5). No project is heavy at the moment; the tier and `--all` stay for parity with the EE 769 runner and for future projects.

## D3 — Notebooks are executed as copies, never in place
- **Why:** the committed notebooks carry the original Colab outputs, which are part of the submitted work. nbconvert writes to `<project>/results/executed/` (git-ignored). Verified by md5 before/after (Testing T7).

## D4 — Do not edit notebooks just to make the runner green
- The planned one-line `fillna` fix in notebook 05 was **not needed** (the line only executes when the data contain NaNs) and was dropped. The ARIMA index failure in 02 needs a behavioural change (datetime index with frequency), so it is reported, not patched. Both are recorded in `FUTURE_SCOPE.md`.

## D5 — Per-item timeout, process-tree kill
- nbconvert's default cell timeout is 30 s, which would fail slow cells; the runner sets `--ExecutePreprocessor.timeout` to the item timeout (default 1800 s). On timeout the whole process tree is killed (`taskkill /T` on Windows) because the notebook kernel is a child process.

## D6 — Missing dependencies are a SKIP, not a FAIL
- A missing package says nothing about the project's correctness; the table shows which modules are missing instead.

## D7 — Minimal `docs/agent/` set
- Only the documents this repository needs (Flow, Decisions, Constraints, Testing, Handover). No Architecture/Bug/Feature files: the repository has no software architecture beyond the runner, and bugs/features are tracked in `FUTURE_SCOPE.md`. Per the protocol, no documentation for its own sake.

## D8 — Git
- The repository already has one commit and a GitHub remote. This session made **no commits**; changes are left as working-tree modifications for the owner to review.
