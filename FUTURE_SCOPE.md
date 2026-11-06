# Future Scope & Improvements

Known issues first, then improvements per project, then repo-wide work. Items are roughly ordered by value for effort.

## 1. Known issues to fix
| Where | Issue | Fix |
|-------|-------|-----|
| `04-…/clustering_kmeans_dbscan.py` | Uses `df1/df2/df3` that are never loaded, so it cannot run | Load `data/original/co2_room_{1,2,3}.csv` (as `co2_clustering_extension.py` does) and merge the other sensors |
| `04-…/clustering_kmeans_dbscan.py` | `create_datetime` builds timestamps from `Year`, `Month`, `DayId` offsets — fragile | Reuse the sequential datetime construction from `co2_clustering_extension.py` or parse the real timestamps |
| `01-…/stats.py` vs `results/statistical_measures.csv` | CSV is in Rs/MWh; script outputs Rs/kWh | Pick one unit, regenerate the CSV from the script |
| `01-…/stats.py` | The price cap (10 Rs/kWh) and the 0–10 body filter are hard-coded; the overall mode is the cap value | Make the cap a named constant; report statistics with and without cap-clipped samples |
| `02-…/load_forecasting.ipynb` | Random Forest evaluated on a random split — leaks future into training for a time series | Use a chronological split / walk-forward validation |
| `02-…/load_forecasting.ipynb` | ARIMA/SARIMA fitted without a date index (statsmodels warns forecasts cannot be generated); orders not tuned | Set a datetime index with `freq="h"`; select orders with AIC or `pmdarima.auto_arima` |
| `03-…/pca_variance.py` | Only DS 3 is run; DS 1/2/4 counts exist only in the report | Loop over all four CSVs and save a summary table |
| `05-endsem/endsem_21d170001.ipynb` | `fillna(method="ffill")` was removed in pandas 3 and fails on a current install | Replace with `.ffill().bfill()` |

## 2. Per-project extensions

### 01 — Electricity price statistics
- Time-of-day conditional distributions (peak / off-peak / solar-hour) instead of one global fit.
- Model the spike at the price cap explicitly: a mixture or zero/one-inflated model plus Gamma/log-normal body.
- Compare candidate distributions with KS / AIC / Q-Q plots in one table.
- Price forecasting (day-ahead) using lagged prices, calendar features and demand.

### 02 — Load forecasting
- Add XGBoost / LightGBM and a sequence model (LSTM / Temporal Fusion Transformer) and compare on equal footing.
- Lag, rolling-window, calendar and holiday features; weather covariates (temperature) as exogenous inputs (ARIMAX/SARIMAX).
- Multi-seasonal models (hourly + weekly + annual): TBATS, Prophet, MSTL.
- Evaluate with MAPE, MASE and pinball loss; add probabilistic / quantile forecasts.
- Handle the missing values by interpolation rather than dropping them.

### 03 — PCA
- Interpret loadings and relate each component to physical quantities (e.g. voltage vs reactance directions).
- Scree plots for all four datasets side by side; compare PCA with factor analysis / ICA / nonlinear methods (kernel PCA, autoencoders).
- Use PCA for dimensionality reduction ahead of a downstream task (anomaly detection on measurements).

### 04 — Thermal-comfort clustering
- Fix the multi-sensor pipeline (see section 1) and cluster CO₂ + temperature + illuminance + occupancy jointly.
- Time-series-aware clustering (DTW / k-Shape, daily-profile clustering) instead of point-wise clustering.
- Use `vav_room_x.csv` (damper position) to link clusters to HVAC behaviour and quantify energy impact.
- Compare against thermal-comfort standards (e.g. CO₂ < 1000 ppm, PMV/PPD) to turn clusters into concrete ventilation set-point recommendations.
- Predictive occupancy model (camera counts → occupancy from CO₂) for demand-controlled ventilation.
- Query the Brick graph (`brick_graph.ttl`) with SPARQL to select sensors programmatically.

### 05 — End-sem
- Quantify renewable share and net-load (Demand − Solar − Hydro) and its ramps; discuss implications for dispatch.
- Short-term forecasts of Solar / Demand on the 15-minute data.

## 3. Repository-wide
- **Reproducibility:** pin versions in `requirements.txt` (or add `pyproject.toml`), fix random seeds everywhere, record Python version.
- **Structure:** move reusable code (loading, datetime handling, metrics) into a shared `src/` package; keep notebooks for exploration and scripts for runs.
- **Notebook hygiene:** strip outputs (`nbstripout`) or keep a rendered HTML copy; one notebook per question.
- **Tests & CI:** a few smoke tests (scripts run on a small data sample) and a GitHub Actions workflow with `ruff` + `pytest`.
- **Data management:** download script or Git LFS for the large CSVs; document data licences and provenance; regenerate `filleddata/` from `original/` with a documented interpolation step.
- **Docs:** add a LICENSE, results summary tables with figures embedded in each project README, and short "lessons learned" notes.
