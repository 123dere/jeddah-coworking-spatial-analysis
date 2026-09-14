"""Global Moran's I for logistic deviance residuals on a polygon GeoPackage.

Expected attributes:
  cw_presence, business_density, built_up_pct, road_density

Queen contiguity and row standardization match the manuscript diagnostic.
"""

from pathlib import Path
import argparse
import numpy as np
import geopandas as gpd
import statsmodels.api as sm
from libpysal.weights import Queen
from esda.moran import Moran

PREDICTORS = ["business_density", "built_up_pct", "road_density"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gpkg", type=Path)
    parser.add_argument("--layer", default=None)
    args = parser.parse_args()

    gdf = gpd.read_file(args.gpkg, layer=args.layer)
    gdf = gdf.dropna(subset=["cw_presence"] + PREDICTORS).copy()

    X = sm.add_constant(gdf[PREDICTORS], has_constant="add")
    y = gdf["cw_presence"].astype(int)
    fit = sm.GLM(y, X, family=sm.families.Binomial()).fit()

    residuals = fit.resid_deviance.to_numpy()
    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = "R"

    moran = Moran(residuals, w)
    print(f"Moran's I: {moran.I:.6f}")
    print(f"Expected I: {moran.EI:.6f}")
    print(f"z (normal): {moran.z_norm:.6f}")
    print(f"p (normal): {moran.p_norm:.6g}")

if __name__ == "__main__":
    main()
