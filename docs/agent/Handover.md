# Handover

Last updated: 2026-11-06. Read `Constraints.md` next, then `Flow.md`.

## Project and status
EE 467 coursework (IIT Bombay, Autumn 2025): five projects (statistics, forecasting, PCA, clustering, end-sem). **Status: organised earlier
(see `README.md`), and now has a single runner `main.py`.** Git: branch `main`, one commit, remote `origin`; **this session's changes are uncommitted**
(see below). Nothing was pushed.

## Work completed this session
1. Wrote `main.py` (registry, tiers, dependency check, subprocess/nbconvert execution into copies, logs, summary, exit codes) — `Flow.md`.
2. Ran every project; set tiers from the results (`Testing.md` T2-T5).
3. Added README "Run everything" section, `.gitignore` entries, `requirements.txt` (+ nbconvert, ipykernel), FUTURE_SCOPE updates, `docs/agent/*`, `CLAUDE.md`, `AGENTS.md`.

## Files changed
- Modified (tracked): `.gitignore`, `README.md`, `FUTURE_SCOPE.md`, `requirements.txt`.
- New (untracked): `main.py`, `CLAUDE.md`, `AGENTS.md`, `docs/agent/{PROTOCOL,Flow,Decisions,Constraints,Testing,Handover}.md`.
- Not touched: all projects' code, notebooks, data, reports.

## Key decisions
`Decisions.md` D1-D8. Notably: runner as subprocesses (D1), executed copies never in place (D3), no notebook edits just to turn the runner green (D4).

## Known issues
- **02** fails on statsmodels 0.15 (`forecast()` needs a date index with frequency). **04b** cannot run (undefined `df1/df2/df3`). Both are registered *broken*.
- **05** has a latent pandas-3 incompatibility (`fillna(method=...)`) that only triggers with NaNs.
- Not tested: 02 end to end, Python other than 3.12.0rc3, Linux/macOS (`Testing.md`).

## Immediate next steps (owner decides)
1. Review the working-tree changes with `git status` / `git diff`, then commit and push yourself (nothing was committed for you).
2. Fix 02 (datetime index with frequency) and 04b (load the data), then switch their tier to `quick` in `main.py`.
3. Optional: re-run on Python 3.13 / a final 3.12 release.

## Warnings for the next agent
- Do not run notebooks in place or overwrite their stored outputs. Do not commit or push without an explicit instruction.
- Timings of `04` varied 21-69 s with machine load; do not read anything into them.
