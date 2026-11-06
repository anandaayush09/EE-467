# 03 — PCA on power-system variables (Individual Assignment 2)

Principal component analysis of four datasets (DS 1–4) of electrically related variables (voltage, current, impedance components, power quantities, …). Question: how many components capture more than 95% of the variance?

| Dataset | Components for >95% variance |
|---------|------------------------------|
| DS 1 | 1 |
| DS 2 | 2 |
| DS 3 | 3 |
| DS 4 | 4 |

The count tracks the number of independently varied quantities: Ohm's law and the power relations couple the variables, so only independent drivers add new variance directions. See the report for the full discussion.

## Run
```bash
python pca_variance.py
```
Analyses DS 3 by default (edit `data_file` at the bottom of the script for the other datasets). The plot is written to `results/`; the submitted figure is `results/DS3_cumulative_variance.png`.

## Files
- `pca_variance.py`
- `data/EE467_EDA_ICA2_PCA_Group{1..4}.csv`
- `report/Assignment2_Aayush.pdf`
