"""Compare the same logistic specification across 1-km and 2-km public tables."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import statsmodels.api as sm

PREDICTORS = ["business_density", "built_up_pct", "road_density"]

def fit(path, scale):
    df = pd.read_csv(path).dropna(subset=["cw_presence"] + PREDICTORS)
    X = sm.add_constant(df[PREDICTORS], has_constant="add")
    y = df["cw_presence"].astype(int)
    model = sm.GLM(y, X, family=sm.families.Binomial()).fit()
    rows = []
    for p in PREDICTORS:
        rows.append({
            "scale": scale,
            "predictor": p,
            "beta": model.params[p],
            "odds_ratio": np.exp(model.params[p]),
            "p_value": model.pvalues[p],
            "n": len(df),
            "events": int(y.sum()),
        })
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_1km", type=Path)
    parser.add_argument("csv_2km", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/scale_sensitivity_public.csv"))
    args = parser.parse_args()

    rows = fit(args.csv_1km, "1-km") + fit(args.csv_2km, "2-km")
    out = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(out.to_string(index=False))
    print(f"\nSaved: {args.output}")

if __name__ == "__main__":
    main()
