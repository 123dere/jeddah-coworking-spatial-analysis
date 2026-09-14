"""Exploratory screening for the public 1-km analytical table."""

from pathlib import Path
import argparse
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

DEFAULT_PREDICTORS = ["business_density", "built_up_pct", "road_density"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/exploratory_screening_public.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    y = df["cw_presence"]
    rows = []

    for col in DEFAULT_PREDICTORS:
        x = df[col]
        rho, p_rho = spearmanr(x, y, nan_policy="omit")
        present = df.loc[y == 1, col].dropna()
        absent = df.loc[y == 0, col].dropna()
        u, p_u = mannwhitneyu(present, absent, alternative="two-sided")
        rows.append({
            "predictor": col,
            "mean_present": present.mean(),
            "mean_absent": absent.mean(),
            "spearman_rho": rho,
            "spearman_p": p_rho,
            "mannwhitney_u": u,
            "mannwhitney_p": p_u,
        })

    out = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(out.to_string(index=False))
    print(f"\nSaved: {args.output}")

if __name__ == "__main__":
    main()
