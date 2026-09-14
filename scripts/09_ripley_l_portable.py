"""Centered Ripley's L with pointwise Monte Carlo CSR envelopes.

This compact implementation is for portfolio/reproducibility use.
All coordinates must use a projected metric CRS.

Important:
- CSR simulations are constrained to the same polygon window.
- The output envelope is pointwise, not global.
- No explicit analytical edge correction is applied.
"""

from pathlib import Path
import argparse
import numpy as np
import geopandas as gpd
from scipy.spatial.distance import pdist
from shapely.geometry import Point

def random_points(poly, n, rng):
    minx, miny, maxx, maxy = poly.bounds
    out = []
    while len(out) < n:
        x, y = rng.uniform(minx,maxx), rng.uniform(miny,maxy)
        p = Point(x,y)
        if poly.contains(p):
            out.append((x,y))
    return np.asarray(out)

def centered_L(coords, area, radii):
    n = len(coords)
    d = pdist(coords)
    pairs = np.array([(d <= r).sum() for r in radii], dtype=float)
    # unordered pairs -> multiply by 2 for ordered i != j pairs
    K = area * (2.0 * pairs) / (n * (n - 1))
    return np.sqrt(K / np.pi) - radii

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("points")
    parser.add_argument("boundary")
    parser.add_argument("--simulations", type=int, default=999)
    parser.add_argument("--rmin", type=float, default=250)
    parser.add_argument("--rmax", type=float, default=10000)
    parser.add_argument("--step", type=float, default=250)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("outputs/ripley_l_public.csv"))
    args = parser.parse_args()

    pts = gpd.read_file(args.points)
    boundary = gpd.read_file(args.boundary).to_crs(pts.crs)
    poly = boundary.geometry.union_all()
    coords = np.column_stack([pts.geometry.x, pts.geometry.y])
    area = poly.area
    radii = np.arange(args.rmin, args.rmax + args.step, args.step)

    observed = centered_L(coords, area, radii)
    rng = np.random.default_rng(args.seed)
    sims = np.vstack([
        centered_L(random_points(poly, len(coords), rng), area, radii)
        for _ in range(args.simulations)
    ])

    import pandas as pd
    out = pd.DataFrame({
        "radius_m": radii,
        "observed_centered_L": observed,
        "csr_median": np.median(sims, axis=0),
        "csr_p025": np.quantile(sims, 0.025, axis=0),
        "csr_p975": np.quantile(sims, 0.975, axis=0),
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(out.head())
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
