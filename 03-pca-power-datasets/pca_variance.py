import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from pathlib import Path

BASE = Path(__file__).resolve().parent
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

def analyze_pca_variance(csv_path, dataset_label):
    """Run PCA, report number of components for >95% variance, and save cumulative variance plot."""
    data = pd.read_csv(csv_path)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(data.values)

    pca_model = PCA()
    pca_model.fit(features_scaled)

    cum_var = np.cumsum(pca_model.explained_variance_ratio_)
    num_needed = np.argmax(cum_var > 0.95) + 1

    print(f"\n=== PCA Analysis for '{dataset_label}' ===")
    print(f"Variance (per component):\n{pca_model.explained_variance_ratio_}")
    print(f"Cumulative variance:\n{cum_var}")
    print(f"Number of components for >95% variance: {num_needed}")

    plt.figure(figsize=(8, 5))
    plt.plot(np.arange(1, len(cum_var) + 1), cum_var, marker='o', linestyle='--')
    plt.axhline(0.95, color='red', linestyle='-', label='95% Threshold')
    plt.axvline(num_needed, color='black', linestyle=':', label=f'{num_needed} Components')
    plt.title(f'Cumulative Explained Variance: {dataset_label}')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.legend()
    plt.grid(True)
    plot_name = RESULTS / f'pca_plot_{dataset_label}.png'
    plt.savefig(plot_name)
    plt.close()
    print(f"Cumulative explained variance plot saved as '{plot_name.name}'.")

    return num_needed

if __name__ == "__main__":
    data_file = BASE / "data" / "EE467_EDA_ICA2_PCA_Group3.csv"
    dataset_name = "DS 3"
    analyze_pca_variance(data_file, dataset_name)
