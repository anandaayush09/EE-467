import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import warnings
warnings.filterwarnings('ignore')
sns.set_style('whitegrid')

def create_datetime(df):
    # Combine Year, Month, Time to create proper datetime
    df['DateTime'] = pd.to_datetime(
        df['Year'].astype(str) + '-' + 
        df['Month'].astype(str) + '-01 ' + 
        df['Time']
    )
    # Adjust for DayId
    df['DateTime'] = df['DateTime'] + pd.to_timedelta(df['DayId'], unit='D')
    return df

df1 = create_datetime(df1)
df2 = create_datetime(df2)
df3 = create_datetime(df3)

merged_df = df1[['DateTime', 'DayId', 'Workday', 'room_1']].merge(
    df2[['DateTime', 'room_2']], on='DateTime', how='outer'
).merge(
    df3[['DateTime', 'room_3']], on='DateTime', how='outer'
)

# Sort by DateTime
merged_df = merged_df.sort_values('DateTime').reset_index(drop=True)

# Extract time-based features
merged_df['Hour'] = merged_df['DateTime'].dt.hour
merged_df['DayOfWeek'] = merged_df['DateTime'].dt.dayofweek
merged_df['IsWeekend'] = merged_df['DayOfWeek'].isin([5, 6]).astype(int)

print(merged_df.head())
print(f"\nDataset shape: {merged_df.shape}")

# Feature Engineering

# Time-based features
merged_df['TimeOfDay'] = pd.cut(merged_df['Hour'], 
                                bins=[0, 6, 12, 18, 24],
                                labels=['Night', 'Morning', 'Afternoon', 'Evening'])

# Calculate rolling statistics (if you want to capture temporal patterns)
window = 12  # 12 time points (adjust based on your data frequency)
for room in ['room_1', 'room_2', 'room_3']:
    merged_df[f'{room}_rolling_mean'] = merged_df[room].rolling(window=window, center=True).mean()
    merged_df[f'{room}_rolling_std'] = merged_df[room].rolling(window=window, center=True).std()

# Calculate rate of change
for room in ['room_1', 'room_2', 'room_3']:
    merged_df[f'{room}_diff'] = merged_df[room].diff()

# Drop NaN values created by rolling windows
merged_df_clean = merged_df.dropna()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Select features for clustering
# Approach 1: Cluster by time patterns and CO2 levels
features_temporal = merged_df_clean[['Hour', 'DayOfWeek', 'IsWeekend', 
                                     'room_1', 'room_2', 'room_3']].copy()

# Standardize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_temporal)

# Determine optimal number of clusters using elbow method
inertias = []
silhouette_scores = []
K_range = range(2, 11)

from sklearn.metrics import silhouette_score

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(features_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(features_scaled, kmeans.labels_))

# Plot elbow curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(K_range, inertias, 'bo-')
ax1.set_xlabel('Number of Clusters (k)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method')
ax1.grid(True)

ax2.plot(K_range, silhouette_scores, 'ro-')
ax2.set_xlabel('Number of Clusters (k)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score Method')
ax2.grid(True)
plt.tight_layout()
plt.savefig('optimal_clusters.png', dpi=300, bbox_inches='tight')
plt.show()

# K Means Clustering

# Choose optimal k (let's say 4 based on the plots)
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
merged_df_clean['Cluster'] = kmeans.fit_predict(features_scaled)

# Analyze cluster characteristics
cluster_summary = merged_df_clean.groupby('Cluster').agg({
    'Hour': ['mean', 'min', 'max'],
    'room_1': ['mean', 'std', 'min', 'max'],
    'room_2': ['mean', 'std', 'min', 'max'],
    'room_3': ['mean', 'std', 'min', 'max'],
    'Workday': 'mean',
    'IsWeekend': 'mean'
})

print("\nCluster Characteristics:")
print(cluster_summary)

# When you have all parameters
# features_multi = merged_df_clean[['room_1', 'room_2', 'room_3', 
#                                   'temp_1', 'temp_2', 'temp_3',
#                                   'humidity_1', 'humidity_2', 'humidity_3',
#                                   'VAV_1', 'VAV_2', 'VAV_3']].copy()
# 
# scaler_multi = StandardScaler()
# features_multi_scaled = scaler_multi.fit_transform(features_multi)
# 
# kmeans_multi = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
# merged_df_clean['Cluster_Multi'] = kmeans_multi.fit_predict(features_multi_scaled)

# Visualize clusters in 2D using PCA
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(features_pca[:, 0], features_pca[:, 1], 
                     c=merged_df_clean['Cluster'], cmap='viridis', 
                     alpha=0.6, s=50)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
plt.title('K-means Clustering Results (PCA Projection)')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)
plt.savefig('cluster_pca.png', dpi=300, bbox_inches='tight')
plt.show()

# Time series plot with cluster colors
fig, axes = plt.subplots(3, 1, figsize=(15, 10))
sample_data = merged_df_clean.sample(min(2000, len(merged_df_clean)))  # Sample for clarity

for idx, room in enumerate(['room_1', 'room_2', 'room_3']):
    scatter = axes[idx].scatter(sample_data['DateTime'], sample_data[room],
                               c=sample_data['Cluster'], cmap='viridis', 
                               alpha=0.6, s=20)
    axes[idx].set_ylabel(f'{room} CO2 (ppm)')
    axes[idx].set_title(f'{room} CO2 Levels Colored by Cluster')
    axes[idx].grid(True, alpha=0.3)
    
axes[-1].set_xlabel('DateTime')
plt.colorbar(scatter, ax=axes, label='Cluster')
plt.tight_layout()
plt.savefig('timeseries_clusters.png', dpi=300, bbox_inches='tight')
plt.show()

# Box plots by cluster
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, room in enumerate(['room_1', 'room_2', 'room_3']):
    merged_df_clean.boxplot(column=room, by='Cluster', ax=axes[idx])
    axes[idx].set_title(f'{room} CO2 by Cluster')
    axes[idx].set_xlabel('Cluster')
    axes[idx].set_ylabel('CO2 (ppm)')
plt.suptitle('')
plt.tight_layout()
plt.savefig('boxplots_by_cluster.png', dpi=300, bbox_inches='tight')
plt.show()

# Interpretation framework
print("\n=== HVAC System Performance Analysis ===\n")

for cluster_id in range(optimal_k):
    cluster_data = merged_df_clean[merged_df_clean['Cluster'] == cluster_id]
    
    print(f"\nCluster {cluster_id} Analysis:")
    print(f"  - Number of observations: {len(cluster_data)}")
    print(f"  - Typical time: Hour {cluster_data['Hour'].mean():.1f}")
    print(f"  - Workday ratio: {cluster_data['Workday'].mean():.2%}")
    
    # CO2 levels (indicator of occupancy)
    print(f"  - Average CO2 levels:")
    for room in ['room_1', 'room_2', 'room_3']:
        mean_co2 = cluster_data[room].mean()
        print(f"    {room}: {mean_co2:.1f} ppm")
    
    # Interpretation guidelines:
    # - CO2 > 1000 ppm: High occupancy, may need more ventilation
    # - CO2 < 600 ppm: Low/no occupancy
    # - CO2 600-1000 ppm: Moderate occupancy
    
    if cluster_data['room_1'].mean() > 1000:
        print("  ⚠️  High CO2 - Potential ventilation issue or high occupancy")
    
    # When VAV data is available:
    # Compare CO2 levels with VAV damper position to assess AC efficiency
