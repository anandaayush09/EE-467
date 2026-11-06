# EE 467 — Data Analytics for Power & Energy Systems

Coursework for **EE 467 (Autumn 2025), IIT Bombay** — Aayush M Anand (21D170001).
Five pieces of work applying statistics, time-series analysis, PCA and clustering to real power-system and building-energy datasets.

| # | Folder | Topic | Methods | Key result |
|---|--------|-------|---------|-----------|
| 1 | [`01-electricity-price-statistics`](01-electricity-price-statistics) | Day-ahead market clearing price (IEX, Apr–Jul 2025) | Descriptive stats, per-day stats, distribution fitting | Prices hit the 10 Rs/kWh cap; Gamma fits the body of the distribution |
| 2 | [`02-load-seasonality-forecasting`](02-load-seasonality-forecasting) | Hourly electricity load, 2015–2018 (Group 16) | ADF/KPSS, periodogram, STL, ARIMA, SARIMA, Random Forest | Random Forest: RMSE ≈ 158 MW, R² ≈ 0.955 |
| 3 | [`03-pca-power-datasets`](03-pca-power-datasets) | PCA on 4 electrical-variable datasets | Standardisation, PCA, cumulative variance | DS 3 needs 3 PCs for >95% variance (DS 1/2/4: 1/2/4) |
| 4 | [`04-thermal-comfort-clustering`](04-thermal-comfort-clustering) | Room usage and comfort patterns from CO₂, temperature, illuminance, occupancy | K-Means, DBSCAN, hierarchical, PCA | See project README and `report/` |
| 5 | [`05-endsem`](05-endsem) | End-semester: normalisation and seasonality of Hydro/Solar/Demand | Min-Max, Z-score, IQR scaling, decomposition | See notebook |

## Repository layout
```
01-… to 05-…     one folder per project: README.md, code, data/, results/, report/
requirements.txt Python dependencies
FUTURE_SCOPE.md  known issues, improvements and further work
```
Each project folder is self-contained: scripts resolve paths relative to their own location, so they can be run from anywhere.

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
```

## Running
```bash
python 01-electricity-price-statistics/stats.py
python 03-pca-power-datasets/pca_variance.py
python 04-thermal-comfort-clustering/co2_clustering_extension.py
jupyter notebook 02-load-seasonality-forecasting/load_forecasting.ipynb
jupyter notebook 05-endsem/endsem_21d170001.ipynb
```
Generated files go to each project's `results/` folder. Notebooks read their data from a relative `data/` path, so launch them from inside their own project folder.

## Data notes
- All datasets were provided by the course. Project 4 ships only the `original/` data; the upsampled `filleddata/` copy (~65 MB) is not tracked.
- Course slides and assignment handouts are instructor material and are intentionally not included in this repository.

See [`FUTURE_SCOPE.md`](FUTURE_SCOPE.md) for improvements and next steps.
