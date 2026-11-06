#!/usr/bin/env python3
"""EE 467 coursework runner: list, run one, or run all of the projects from one place.

    python main.py                 run the quick projects, list the rest with the reason they were skipped
    python main.py --list          show every project, its tier and whether its dependencies are installed
    python main.py 01 03           run the named projects (any tier)
    python main.py --all           run quick + heavy projects ('broken' ones are still skipped)
    python main.py --timeout 600   per-project time limit in seconds (default 1800)

How it works (see docs/agent/Flow.md): every project runs in its own subprocess with the
project folder as working directory, because the scripts and notebooks read their data from
a relative ``data/`` path. Notebooks are executed with nbconvert into
``<project>/results/executed/``: the committed notebook, with its stored outputs, is never
modified. Output of each run goes to ``run_logs/<id>.log``.

Exit code: 0 = nothing failed, 1 = at least one project failed, 2 = bad command line.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "run_logs"

# nbconvert + ipykernel are needed to execute any notebook
NOTEBOOK_TOOLS = ("nbconvert", "ipykernel")

QUICK, HEAVY, BROKEN = "quick", "heavy", "broken"


@dataclass(frozen=True)
class Item:
    id: str
    title: str
    kind: str          # "script" or "notebook"
    path: str          # relative to the repo root
    tier: str          # QUICK / HEAVY / BROKEN
    requires: tuple    # importable module names
    reason: str        # why it has this tier


# Order = execution order. Tiers were set from real runs; see docs/agent/Testing.md.
REGISTRY = [
    Item("01", "Electricity price statistics", "script",
         "01-electricity-price-statistics/stats.py", QUICK,
         ("numpy", "pandas", "scipy", "seaborn", "matplotlib", "openpyxl"), "runs in seconds"),
    Item("02", "Load seasonality and forecasting", "notebook",
         "02-load-seasonality-forecasting/load_forecasting.ipynb", BROKEN,
         ("numpy", "pandas", "scipy", "seaborn", "matplotlib", "sklearn", "statsmodels"),
         "ARIMA forecast() raises ValueError on statsmodels 0.15 (series has no date index with frequency); "
         "it only warned on Colab's older version"),
    Item("03", "PCA on power-system datasets", "script",
         "03-pca-power-datasets/pca_variance.py", QUICK,
         ("numpy", "pandas", "sklearn", "matplotlib"), "runs in seconds"),
    Item("04", "Thermal-comfort CO2 clustering", "script",
         "04-thermal-comfort-clustering/co2_clustering_extension.py", QUICK,
         ("numpy", "pandas", "sklearn"), "runs in seconds"),
    Item("04b", "Thermal-comfort multi-sensor clustering", "script",
         "04-thermal-comfort-clustering/clustering_kmeans_dbscan.py", BROKEN,
         ("numpy", "pandas", "sklearn", "seaborn", "matplotlib"),
         "starts from df1/df2/df3 that are never loaded (see FUTURE_SCOPE.md)"),
    Item("05", "End-semester: normalisation and seasonality", "notebook",
         "05-endsem/endsem_21d170001.ipynb", QUICK,
         ("numpy", "pandas", "matplotlib"), "runs in seconds"),
]

# Status values
PASS, FAIL = "PASS", "FAIL"
SKIP_HEAVY, SKIP_BROKEN, SKIP_DEPS = "SKIPPED (heavy)", "SKIPPED (broken)", "SKIPPED (missing deps)"


def missing_modules(item: Item) -> list[str]:
    """Modules the item needs that are not importable here (checked without importing them)."""
    needed = list(item.requires) + (list(NOTEBOOK_TOOLS) if item.kind == "notebook" else [])
    return [m for m in needed if importlib.util.find_spec(m) is None]


def _kill_tree(proc: subprocess.Popen) -> None:
    """Stop a timed-out run including child processes (a notebook kernel outlives nbconvert)."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
    else:
        proc.kill()


def build_command(item: Item, timeout: int) -> tuple[list[str], Path]:
    """Command line and working directory for one item."""
    project_dir = (ROOT / item.path).parent
    name = Path(item.path).name
    if item.kind == "script":
        return [sys.executable, name], project_dir
    return [
        sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute",
        f"--ExecutePreprocessor.timeout={timeout}",   # nbconvert's default is 30 s PER CELL
        "--output-dir", str(project_dir / "results" / "executed"),
        name,
    ], project_dir


def run_item(item: Item, timeout: int) -> tuple[str, float, str]:
    """Run one item; returns (status, seconds, note)."""
    cmd, cwd = build_command(item, timeout)
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")  # Agg: never open plot windows
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"{item.id}.log"
    start = time.time()
    with open(log_path, "w", encoding="utf-8") as log:
        log.write(f"$ {' '.join(cmd)}\n(cwd: {cwd})\n\n")
        log.flush()
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            code = proc.wait(timeout=timeout)
            note = "" if code == 0 else f"exit code {code}"
        except subprocess.TimeoutExpired:
            _kill_tree(proc)
            proc.wait()
            code, note = -1, f"timed out after {timeout}s"
    return (PASS if code == 0 else FAIL), time.time() - start, note


def print_table(rows: list[tuple]) -> None:
    header = ("id", "project", "status", "seconds", "note / log")
    widths = [max(len(str(r[i])) for r in [header] + rows) for i in range(5)]
    line = "  ".join(h.ljust(w) for h, w in zip(header, widths, strict=True))
    print(line)
    print("-" * len(line))
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths, strict=True)))


def cmd_list() -> int:
    rows = []
    for it in REGISTRY:
        miss = missing_modules(it)
        deps = "ok" if not miss else "missing: " + ", ".join(miss)
        rows.append((it.id, it.title, it.tier, it.kind, deps, it.reason))
    header = ("id", "project", "tier", "kind", "dependencies", "why")
    widths = [max(len(str(r[i])) for r in [header] + rows) for i in range(6)]
    print("  ".join(h.ljust(w) for h, w in zip(header, widths, strict=True)))
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths, strict=True)))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run the EE 467 projects.", formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("ids", nargs="*", help="project ids to run (e.g. 01 03 04b); default: the quick ones")
    ap.add_argument("--list", action="store_true", help="list projects and exit")
    ap.add_argument("--all", action="store_true", help="also run the heavy projects (broken ones stay skipped)")
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per project (default 1800)")
    args = ap.parse_args(argv)

    if args.list:
        return cmd_list()

    by_id = {it.id: it for it in REGISTRY}
    unknown = [i for i in args.ids if i not in by_id]
    if unknown:
        print(f"error: unknown project id(s) {unknown}; known: {', '.join(by_id)}", file=sys.stderr)
        return 2

    named = [by_id[i] for i in args.ids]
    scope = named if named else REGISTRY      # a default / --all run reports every project in the table
    rows, failed = [], False
    for it in scope:
        explicit = bool(named)
        if not explicit and it.tier == BROKEN:
            rows.append((it.id, it.title, SKIP_BROKEN, "-", it.reason))
            continue
        if not explicit and it.tier == HEAVY and not args.all:
            rows.append((it.id, it.title, SKIP_HEAVY, "-", f"{it.reason}; run with --all or `{it.id}`"))
            continue
        miss = missing_modules(it)
        if miss:
            rows.append((it.id, it.title, SKIP_DEPS, "-", "missing: " + ", ".join(miss)))
            continue
        print(f"[{it.id}] running {it.title} ...", flush=True)
        status, secs, note = run_item(it, args.timeout)
        failed |= status == FAIL
        rows.append((it.id, it.title, status, f"{secs:.1f}", note or f"run_logs/{it.id}.log"))

    print()
    print_table(rows)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
