"""Validate the minimum public analytical-table schema."""

from pathlib import Path
import argparse
import pandas as pd

REQUIRED = [
    "grid_id",
    "cw_presence",
    "business_density",
    "built_up_pct",
    "road_density",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    if not set(df["cw_presence"].dropna().unique()).issubset({0, 1}):
        raise SystemExit("cw_presence must contain only 0/1 values.")

    print(f"Rows: {len(df):,}")
    print(f"Presence cells: {int(df['cw_presence'].sum()):,}")
    print("Schema: PASS")

if __name__ == "__main__":
    main()
