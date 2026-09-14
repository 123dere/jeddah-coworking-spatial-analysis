"""Fit the three-predictor binary logistic model on a public analytical CSV."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import statsmodels.api as sm

PREDICTORS = ["business_density", "built_up_pct", "road_density"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/logistic_results_public.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv).dropna(subset=["cw_presence"] + PREDICTORS)
    X = sm.add_constant(df[PREDICTORS], has_constant="add")
    y = df["cw_presence"].astype(int)

    model = sm.GLM(y, X, family=sm.families.Binomial()).fit()
    ci = model.conf_int()

    out = pd.DataFrame({
        "term": model.params.index,
        "beta": model.params.values,
        "se": model.bse.values,
        "odds_ratio": np.exp(model.params.values),
        "ci_low": np.exp(ci[0].values),
        "ci_high": np.exp(ci[1].values),
        "p_value": model.pvalues.values,
    })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(model.summary())
    print(f"\nSaved: {args.output}")

if __name__ == "__main__":
    main()
