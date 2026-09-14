"""Monte Carlo average nearest-neighbour analysis inside an irregular polygon.

Inputs:
- point GeoPackage / shapefile
- polygon GeoPackage / shapefile

All layers should use a projected metric CRS before analysis.
"""

from pathlib import Path
import argparse
import numpy as np
import geopandas as gpd
from scipy.spatial import cKDTree
from shapely.geometry import Point

def mean_nn(coords):
    tree = cKDTree(coords)
    d, _ = tree.query(coords, k=2)
    return float(d[:, 1].mean())

def random_points_in_polygon(poly, n, rng):
    minx, miny, maxx, maxy = poly.bounds
    pts = []
    while len(pts) < n:
        x = rng.uniform(minx, maxx)
        y = rng.uniform(miny, maxy)
        p = Point(x, y)
        if poly.contains(p):
            pts.append((x, y))
    return np.asarray(pts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("points")
    parser.add_argument("boundary")
    parser.add_argument("--simulations", type=int, default=999)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    pts = gpd.read_file(args.points)
    boundary = gpd.read_file(args.boundary).to_crs(pts.crs)
    poly = boundary.geometry.union_all()

    coords = np.column_stack([pts.geometry.x, pts.geometry.y])
    obs = mean_nn(coords)

    rng = np.random.default_rng(args.seed)
    sims = np.empty(args.simulations)
    for i in range(args.simulations):
        sims[i] = mean_nn(random_points_in_polygon(poly, len(coords), rng))

    expected = sims.mean()
    ratio = obs / expected
    p_cluster = (1 + np.sum(sims <= obs)) / (args.simulations + 1)
    z = (obs - sims.mean()) / sims.std(ddof=1)

    print(f"N: {len(coords)}")
    print(f"Observed mean NN: {obs:.3f}")
    print(f"Mean CSR NN: {expected:.3f}")
    print(f"NN ratio: {ratio:.4f}")
    print(f"Monte Carlo z: {z:.3f}")
    print(f"One-sided cluster p: {p_cluster:.4f}")

if __name__ == "__main__":
    main()
