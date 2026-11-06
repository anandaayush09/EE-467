# Test evidence

Recorded 2026-11-06. Environment: Windows 11, Python 3.12.0rc3 (a release candidate) in a scratch venv with numpy 2.5.4,
pandas 3.1.1, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, seaborn 0.13.2, matplotlib 3.11.2, nbconvert 7.17.2,
nbclient 0.11.0, ipykernel 7.4.0, ruff 0.17.4. Git: branch `main`, one commit ("First Commit"), remote `origin`; nothing committed by this work.

Legend: **PASS** = run and verified · **FAIL** · **NOT TESTED** · **BLOCKED**.

## Checklist before implementing
- Expected: `python main.py` runs the quick projects, skips broken/heavy ones with a reason, never modifies committed notebooks.
- Edge cases: unknown id, missing dependency, project that raises, timeout, wrong working directory (scripts use relative `data/`).
- Existing behaviour at risk: notebooks' stored outputs; tracked files (`.gitignore`, `README.md`, `FUTURE_SCOPE.md`, `requirements.txt`).

## Results
| ID | What | Command / method | Result |
|----|------|------------------|--------|
| T1 | Listing | `python main.py --list` | 6 projects with tier, kind, dependency status and reason; exit 0. PASS |
| T2 | Quick tier | `python main.py` | 01 PASS (≈6 s), 03 PASS (≈4-5 s), 04 PASS (21-69 s, machine-load dependent), 05 PASS (12-21 s); 02 and 04b SKIPPED (broken); exit 0. Re-run after reclassifying 02: same result. PASS |
| T3 | `--all` | `python main.py --all` | Same as T2 (no heavy projects registered); exit 0. PASS |
| T4 | Named broken item | `python main.py 04b` | FAIL with the real error `NameError: name 'df1' is not defined` (log checked); exit 1. This is the expected, documented defect. PASS (behaves as designed) |
| T5 | Heavy-tier guess | `python main.py 02 --timeout 900` | **FAIL after 27 s**, not slow: `ValueError: No supported index is available` at `model_arima_fit.forecast(steps=50)` (statsmodels 0.15.0; Colab's older version only warned). 02 therefore reclassified **broken**; the SARIMA cell was never reached, so how long it takes is **not tested**. Result for 02: FAIL (known) |
| T6 | Error paths | unknown id `python main.py 99`; simulated missing module (a fake registry item requiring `not_a_real_module_xyz`) | unknown id: message, exit 2. Missing module: row `SKIPPED (missing deps)` naming the module, exit 0. PASS |
| T7 | Committed notebooks untouched | md5 of `02-…/load_forecasting.ipynb` and `05-…/endsem_21d170001.ipynb` before all runs and after the last run | identical (`34a0ada9…`, `a4d933e8…`). Executed copies went to `05-endsem/results/executed/` (ignored). PASS |
| T8 | Lint | `ruff check main.py` (rules E,F,W,I,B, line length 120) | first run 3× E702 (semicolons) fixed; then "All checks passed" |
| T9 | Diff review | `git diff` of the tracked files + `git status` | tracked changes are exactly: `.gitignore` (+ `run_logs/`, `*/results/executed/`), `README.md` (run-everything section, repo map), `requirements.txt` (+ nbconvert, ipykernel), `FUTURE_SCOPE.md` (02 failure, 05 latent issue, main.py row). New untracked: `main.py`, `CLAUDE.md`, `AGENTS.md`, `docs/agent/*`. No notebook, data or code file of the projects modified. PASS |
| T10 | Git hygiene | `git status --short` after runs | `run_logs/`, `*/results/executed/` and generated `results/` files do not appear (ignored). PASS |

## Not tested
- **02 end to end** (blocked by the statsmodels index error; its SARIMA cells were never executed here).
- **04b** (broken by design).
- Python other than 3.12.0rc3; other package versions; a clean `pip install -r requirements.txt` (the scratch venv was installed by hand with the same packages).
- Linux/macOS (the runner uses `taskkill` only on Windows; the POSIX path `proc.kill()` was not exercised).
- The timeout/kill path (no run reached the limit).
- Rendering of the Mermaid diagram in `Flow.md` (syntax written by hand, not rendered; GitHub rendering not checked).

## How to re-run
```bash
pip install -r requirements.txt
python main.py --list
python main.py
```
