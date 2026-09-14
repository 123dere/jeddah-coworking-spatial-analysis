"""Create a compact odds-ratio plot from a result CSV."""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/odds_ratio_plot.png"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df = df[df["term"] != "const"].copy() if "term" in df.columns else df.copy()
    label_col = "term" if "term" in df.columns else "predictor"

    y = range(len(df))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.errorbar(
        df["odds_ratio"], y,
        xerr=[df["odds_ratio"] - df["ci_low"], df["ci_high"] - df["odds_ratio"]],
        fmt="o", capsize=3
    )
    ax.axvline(1.0, linestyle="--", linewidth=1)
    ax.set_yticks(list(y))
    ax.set_yticklabels(df[label_col])
    ax.set_xlabel("Odds ratio (95% CI)")
    ax.set_title("Adjusted odds ratios")
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=200, bbox_inches="tight")
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
