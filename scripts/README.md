# Scripts

Portable public scripts are provided for portfolio/reproducibility purposes.

| Script | Purpose |
|---|---|
| `01_validate_inputs.py` | Check public analytical-table schema |
| `02_exploratory_screening.py` | Spearman + Mann-Whitney screening |
| `03_logistic_glr.py` | Three-predictor binary logistic model |
| `04_residual_moran.py` | Moran's I of deviance residuals |
| `05_scale_sensitivity.py` | Compare 1-km and 2-km models |
| `06_firth_logistic.py` | Firth bias-reduced logistic regression |
| `07_monte_carlo_ann.py` | Monte Carlo average nearest-neighbour |
| `08_kde_portable.py` | Portable KDE implementation |
| `09_ripley_l_portable.py` | Pointwise Monte Carlo centered Ripley's L |
| `10_make_odds_ratio_plot.py` | Odds-ratio figure |

The publication used ArcGIS Pro for several spatial steps. The portable scripts are intended to make the analytical logic inspectable and reusable without embedding local ArcGIS project paths.
