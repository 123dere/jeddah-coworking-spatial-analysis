# Reproducibility workflow

## RQ1 — Spatial clustering

Inputs:
- coworking point locations;
- Jeddah municipal observation window.

Methods:
1. Monte Carlo average nearest-neighbour analysis.
2. Kernel density estimation.
3. Centered Ripley's L-function using CSR simulations.

## RQ2 — Urban correlates

Input:
- 1-km analytical grid.

Methods:
1. Bivariate screening.
2. Binary logistic generalized linear model:
   `cw_presence ~ business_density + built_up_pct + road_density`
3. Global Moran's I on deviance residuals.

## RQ3 — Scale robustness

Input:
- 2-km analytical grid.

Methods:
1. Re-estimate the same three-predictor model.
2. Compare coefficient direction and inferential support.
3. Repeat residual Moran's I.

## Rare-event robustness

The 1-km and 2-km models are additionally estimated using Firth's bias-reduced penalized likelihood logistic regression.

The Firth model is a robustness analysis and does not change the predictor specification.
