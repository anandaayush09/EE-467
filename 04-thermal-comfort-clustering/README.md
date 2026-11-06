# 04 — Thermal-comfort clustering (Class Project 2, Group 16)

Clustering of building-sensor time series (CO₂, temperature, illuminance, occupancy) from three rooms of a university building (Mar 2018 – Apr 2019; Room 1 is a lecture hall, Rooms 2–3 are study zones).

Goals: identify typical usage modes (empty / lightly / fully occupied), flag ventilation or comfort problems (high CO₂ and rising temperature despite occupancy), and derive operational recommendations. See `report/Group16_Report.pdf`.

## Scripts
- `co2_clustering_extension.py` — end-to-end CO₂ workflow for all three rooms: load, build a datetime axis, merge, feature engineering, K-Means and hierarchical clustering, evaluated with silhouette, Davies-Bouldin and Calinski-Harabasz scores. Runnable as is:
  ```bash
  python co2_clustering_extension.py
  ```
- `clustering_kmeans_dbscan.py` — multi-sensor K-Means / DBSCAN / PCA analysis with plots. **Incomplete:** it starts from `df1/df2/df3`, which are never loaded (see `FUTURE_SCOPE.md`).

## Data
`data/original/` — raw sensor CSVs, Brick schema graph (`brick_graph.ttl`, `brick_generator.py`) and the occupant-behaviour ontology. `data/README.txt` and `data/roominfo.txt` describe the files and rooms.
`data/filleddata/` (upsampled version) is git-ignored and not part of the repository.
