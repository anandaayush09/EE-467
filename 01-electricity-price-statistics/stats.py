import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from pathlib import Path

BASE = Path(__file__).resolve().parent
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

# === 1. Load the data ===
# Update the file path to your file in Google Drive
df = pd.read_excel(BASE / "data" / "iex_mcp_apr_jul_2025.xlsx")

# Rename columns for convenience if needed
df.columns = ['Datetime', 'MCP_Rs_per_MWh']

# Convert to datetime
df['Datetime'] = pd.to_datetime(df['Datetime'])
# Rs/kWh conversion
df['MCP_Rs_per_kWh'] = df['MCP_Rs_per_MWh'] / 1000

# === 2. Whole dataset statistical measures ===
target = df['MCP_Rs_per_kWh']

overall_stats = {
    "count": len(target),
    "mean": np.mean(target),
    "median": np.median(target),
    "mode": stats.mode(target, keepdims=True)[0][0],
    "min": np.min(target),
    "max": np.max(target),
    "variance": np.var(target, ddof=1),
    "std_dev": np.std(target, ddof=1),
    "percentile_25": np.percentile(target, 25),
    "percentile_50": np.percentile(target, 50),
    "percentile_75": np.percentile(target, 75)
}
print("=== Overall Statistical Measures (Rs/kWh) ===")
for k, v in overall_stats.items():
    print(f"{k:15}: {v:.2f}")

# === 3. Daily statistical measures ===
df['date'] = df['Datetime'].dt.date
daily_group = df.groupby('date')['MCP_Rs_per_kWh']

daily_stats = daily_group.agg([
    'count', 'mean', 'median', 'min', 'max', 'std',
    lambda x: np.percentile(x,25), lambda x: np.percentile(x,75)
])
daily_stats.columns = ['count','mean','median','min','max','stddev','perc25','perc75']

print("\n=== Per-Day Statistical Measures (first 5 days) ===")
print(daily_stats.head())

# Optional: save daily summary to CSV
daily_stats.to_csv(RESULTS / "daily_statistics.csv")

# === 4. Histogram + KDE plot ===
plt.figure(figsize=(12,7))
sns.histplot(target, bins=50, kde=True, color='skyblue', edgecolor="black", stat="frequency")
plt.xlabel("MCP (Rs/kWh)")
plt.ylabel("Frequency")
plt.title("Distribution of MCP (Rs/kWh)")
plt.tight_layout()
plt.savefig(RESULTS / "mcp_distribution_plot.png")
plt.show()

# === 5. Fit probability distribution (Gamma, for prices 0 < x < cap) ===
body = target[(target>0) & (target<10)]
fit_shape, fit_loc, fit_scale = stats.gamma.fit(body)
print("\nGamma distribution fit parameters (excluding spikes at 0 and 10):")
print(f"Shape: {fit_shape:.2f}, Loc: {fit_loc:.2f}, Scale: {fit_scale:.2f}")

# Compare empirical and fitted distribution visually
x = np.linspace(body.min(), body.max(), 200)
pdf_fitted = stats.gamma.pdf(x, fit_shape, fit_loc, fit_scale)
plt.figure(figsize=(10,6))
sns.histplot(body, bins=50, color='skyblue', stat="density", edgecolor="black", label='Empirical')
plt.plot(x, pdf_fitted, 'r-', lw=2, label='Gamma fit')
plt.xlabel("MCP (Rs/kWh)")
plt.ylabel("Density")
plt.title("Empirical vs Gamma Fit (0 < MCP < 10)")
plt.legend()
plt.tight_layout()
plt.show()