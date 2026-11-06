# Constraints

Authoritative list of project-specific restrictions. Read before changing anything; a change that conflicts with an item needs the
owner's explicit authorisation first.

## Protected
- **Committed notebooks keep their stored outputs.** The runner must only write executed *copies* (`results/executed/`); never
  `--inplace`, never overwrite `02-…/load_forecasting.ipynb` or `05-…/endsem_21d170001.ipynb`. A change to a notebook is limited to the lines
  the owner approved and is recorded in `Testing.md` (md5 before/after).
- **Data files** (`*/data/**`) are inputs. Do not edit or regenerate them.
- **Reports** (`04-…/report/`, `01-…/report/`, `03-…/report/`) are the submitted work; do not edit.
- `docs/agent/PROTOCOL.md` — the owner's operating protocol, verbatim.

## Never commit (enforced by `.gitignore`)
`_review/`, `course-material/` (instructor and publisher material), `04-…/data/filleddata/` (large derived copy),
`run_logs/`, `*/results/executed/`, virtual environments, caches.

## Process rules (from the protocol)
- Do **not commit, push, merge or deploy** unless the owner explicitly asks. The repository already has a first commit and a GitHub remote.
- Do not delete files; unneeded files go to `_review/`.
- No new dependency without a stated reason (the runner added only `nbconvert` and `ipykernel`).
- No unrelated refactoring; one logical change per request.
- Never describe something as tested unless it was run; evidence goes into `Testing.md`.
- Keep `Handover.md` current at the end of every session.
- Hard-coded machine paths are not allowed.
