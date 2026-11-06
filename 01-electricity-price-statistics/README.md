# 01 — Electricity price statistics (Assignment 1)

Statistical description and distribution modelling of the Indian Energy Exchange (IEX) day-ahead market clearing price (MCP), April–July 2025, 15-minute resolution (11,712 samples).

## What it does
1. Overall statistics: mean, median, mode, min/max, variance, std, quartiles.
2. Per-day statistics (count, mean, median, min, max, std, quartiles).
3. Histogram + KDE and a Gamma fit to the non-spike body of prices (0 < MCP < 10 Rs/kWh).

## Run
```bash
python stats.py
```
Outputs are written to `results/`. `results/statistical_measures.csv` is the daily-statistics table kept from the submission.

## Files
- `stats.py` — analysis script
- `data/iex_mcp_apr_jul_2025.xlsx` — input prices (Rs/MWh)
- `report/Assignment1_Aayush.pdf` — submitted report

## Note
`results/statistical_measures.csv` is in Rs/MWh, whereas `stats.py` converts to Rs/kWh before computing statistics (see `FUTURE_SCOPE.md`).
