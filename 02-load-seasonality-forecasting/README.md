# 02 — Load seasonality & forecasting (Class Project 1, Group 16)

Hourly electricity load (MW), 2015–2018 (35,062 observations after cleaning).

## Pipeline (`load_forecasting.ipynb`)
1. Load, clean (drop missing values), visual inspection and z-score outlier check.
2. Seasonality detection: ADF and KPSS tests, periodogram, STL (period = 24), seasonal differencing (lag 24), hour × weekday heatmap.
3. Statistical forecasting: ARIMA(5,1,0) and SARIMA(1,1,1)(1,1,1,24).
4. ML forecasting: Random Forest regressor (RMSE ≈ 158 MW, R² ≈ 0.955 on the held-out split).
5. Comparison of the two model families.

## Run
```bash
jupyter notebook load_forecasting.ipynb
```
Launch from this folder: the notebook reads `data/EE467_EDA_Data_Group16_Load.csv`. It was written in Google Colab; the Drive paths were changed to relative paths. Stored cell outputs are from the original Colab run.

## Caveats
Model orders are illustrative (not tuned), and the Random Forest is evaluated on a random split — see `FUTURE_SCOPE.md`.
