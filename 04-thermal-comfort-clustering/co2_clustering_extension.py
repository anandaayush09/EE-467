#!/usr/bin/env python3
"""
CO2 Time Series Clustering Assignment - Complete Solution

This script provides a complete, reproducible workflow for clustering CO2 time series data
from three different rooms. It includes data preprocessing, feature engineering, clustering
analysis, and evaluation.

Required Libraries:
- pandas
- numpy 
- scikit-learn

Input Files Expected:
- co2_room_1.csv
- co2_room_2.csv
- co2_room_3.csv

Author: Generated for Academic Assignment
Date: October 2025
"""

import pandas as pd
import numpy as np
import warnings
from datetime import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

warnings.filterwarnings('ignore')

print("="*80)
print("CO2 TIME SERIES CLUSTERING - COMPLETE WORKFLOW")
print("="*80)
print(f"Script started at: {datetime.now()}\n")

from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "original"
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

# STEP 1: DATA LOADING
print("STEP 1: Loading CO2 datasets...")
room1 = pd.read_csv(DATA / 'co2_room_1.csv')
room2 = pd.read_csv(DATA / 'co2_room_2.csv')
room3 = pd.read_csv(DATA / 'co2_room_3.csv')
print(f"✓ Loaded Room 1: {room1.shape}, Room 2: {room2.shape}, Room 3: {room3.shape}")

print("\n" + "="*80)

# STEP 2: CREATE DATETIME FIELD
print("STEP 2: Creating unified DateTime field...")
def create_datetime_sequential(df, start_date='2018-03-01'):
    df = df.sort_values(['DayId', 'Time']).reset_index(drop=True)
    base_date = pd.to_datetime(start_date)
    dates = []
    for idx, row in df.iterrows():
        day_offset = row['DayId']
        current_date = base_date + pd.Timedelta(days=day_offset)
        date_str = current_date.strftime('%Y-%m-%d')
        datetime_str = f"{date_str} {row['Time']}"
        dates.append(datetime_str)
    df['DateTime'] = pd.to_datetime(dates, format='mixed')
    return df

room1 = create_datetime_sequential(room1.copy())
room2 = create_datetime_sequential(room2.copy())
room3 = create_datetime_sequential(room3.copy())
print(f"✓ DateTime field created. Date range: {room1['DateTime'].min()} to {room1['DateTime'].max()}")

print("\n" + "="*80)

# STEP 3: MERGE DATASETS
print("STEP 3: Merging datasets...")
room1_merge = room1[['DateTime', 'Workday', 'room_1']].copy()
room2_merge = room2[['DateTime', 'Workday', 'room_2']].copy()
room3_merge = room3[['DateTime', 'Workday', 'room_3']].copy()

df_combined = room1_merge.merge(room2_merge, on=['DateTime', 'Workday'], how='outer')
df_combined = df_combined.merge(room3_merge, on=['DateTime', 'Workday'], how='outer')
df_combined = df_combined.sort_values('DateTime').reset_index(drop=True)
print(f"✓ Datasets merged: {df_combined.shape}")

print("\n" + "="*80)

# STEP 4: RESAMPLING
print("STEP 4: Resampling to uniform 5-minute intervals...")
def resample_room_data(df, room_col):
    df_room = df[['DateTime', room_col]].dropna().copy()
    df_room = df_room.set_index('DateTime')
    df_resampled = df_room.resample('5min').mean()
    df_resampled = df_resampled.ffill(limit=3)
    return df_resampled

room1_resampled = resample_room_data(df_combined, 'room_1')
room2_resampled = resample_room_data(df_combined, 'room_2')
room3_resampled = resample_room_data(df_combined, 'room_3')

df_resampled = pd.DataFrame({
    'room_1': room1_resampled['room_1'],
    'room_2': room2_resampled['room_2'],
    'room_3': room3_resampled['room_3']
})

df_complete = df_resampled.dropna()
print(f"✓ Complete cases: {len(df_complete)} at 5-min intervals")

print("\n" + "="*80)

# STEP 5: FEATURE ENGINEERING
print("STEP 5: Feature engineering...")
def extract_time_series_features(df):
    features_list = []
    for idx in df.index:
        row = df.loc[idx]
        hour = idx.hour
        day_of_week = idx.dayofweek
        is_weekend = 1 if day_of_week >= 5 else 0
        is_workday = 1 - is_weekend
        if 6 <= hour < 12:
            period = 0
        elif 12 <= hour < 18:
            period = 1
        elif 18 <= hour < 22:
            period = 2
        else:
            period = 3
        room1_co2 = row['room_1']
        room2_co2 = row['room_2']
        room3_co2 = row['room_3']
        co2_values = [room1_co2, room2_co2, room3_co2]
        features_list.append({
            'timestamp': idx,
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'is_workday': is_workday,
            'period': period,
            'room1_co2': room1_co2,
            'room2_co2': room2_co2,
            'room3_co2': room3_co2,
            'mean_co2': np.mean(co2_values),
            'std_co2': np.std(co2_values),
            'max_co2': np.max(co2_values),
            'min_co2': np.min(co2_values),
            'range_co2': np.max(co2_values)-np.min(co2_values)
        })
    return pd.DataFrame(features_list)

features_df = extract_time_series_features(df_complete)
features_df = features_df.set_index('timestamp')

def add_rolling_features(features_df, df_complete, window=12):
    room_mapping = {
        'room1_co2': 'room_1',
        'room2_co2': 'room_2',
        'room3_co2': 'room_3'
    }
    for feature_name, df_col in room_mapping.items():
        features_df[f'{feature_name}_diff'] = df_complete[df_col].diff().fillna(0)
        features_df[f'{feature_name}_rolling_mean'] = df_complete[df_col].rolling(window=window, min_periods=1).mean()
        features_df[f'{feature_name}_rolling_std'] = df_complete[df_col].rolling(window=window, min_periods=1).std().fillna(0)
    return features_df

features_df = add_rolling_features(features_df, df_complete, window=12)
print(f"✓ Features engineered: {features_df.shape[1]} features")

print("\n" + "="*80)

# STEP 6: FEATURE SELECTION & STANDARDIZATION
print("STEP 6: Feature selection and standardization...")
clustering_features = [
    'hour', 'day_of_week', 'is_workday', 'period',
    'room1_co2', 'room2_co2', 'room3_co2', 
    'mean_co2', 'std_co2', 'range_co2',
    'room1_co2_rolling_mean', 'room1_co2_rolling_std',
    'room2_co2_rolling_mean', 'room2_co2_rolling_std', 
    'room3_co2_rolling_mean', 'room3_co2_rolling_std'
]
X = features_df[clustering_features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✓ Feature matrix shape:", X_scaled.shape)

print("\n" + "="*80)

# STEP 7: CLUSTERING
print("STEP 7: Clustering with K-Means and Hierarchical...")
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10, max_iter=300)
kmeans_labels = kmeans.fit_predict(X_scaled)
features_df['kmeans_cluster'] = kmeans_labels
print("✓ K-Means clustering complete")

hierarchical = AgglomerativeClustering(n_clusters=optimal_k, linkage='ward')
hier_labels = hierarchical.fit_predict(X_scaled)
features_df['hierarchical_cluster'] = hier_labels
print("✓ Hierarchical clustering complete")

print("\n" + "="*80)

# STEP 8: EVALUATION
print("STEP 8: Clustering evaluation metrics...")
sil_km = silhouette_score(X_scaled, kmeans_labels)
db_km = davies_bouldin_score(X_scaled, kmeans_labels)
ch_km = calinski_harabasz_score(X_scaled, kmeans_labels)
sil_hier = silhouette_score(X_scaled, hier_labels)
db_hier = davies_bouldin_score(X_scaled, hier_labels)
ch_hier = calinski_harabasz_score(X_scaled, hier_labels)
print(f"K-Means:  Silhouette={sil_km:.4f}, DB={db_km:.4f}, CH={ch_km:.2f}")
print(f"Hierarchical:  Silhouette={sil_hier:.4f}, DB={db_hier:.4f}, CH={ch_hier:.2f}")

print("\n" + "="*80)

# STEP 9: ANALYSIS AND SAVE
print("STEP 9: Cluster analysis and save results...")
features_df.to_csv(RESULTS / 'clustered_co2_features.csv')
print("✓ Full labeled feature set saved as clustered_co2_features.csv")

print("K-Means Cluster Counts:\n", features_df['kmeans_cluster'].value_counts())
print("Hierarchical Cluster Counts:\n", features_df['hierarchical_cluster'].value_counts())

print("\nAnalysis complete! All results saved. Script ended at:", datetime.now())
print("="*80)
