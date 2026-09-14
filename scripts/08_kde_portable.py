"""Simple planar KDE for point coordinates using scikit-learn.

This is a portable portfolio implementation. The publication used ArcGIS Pro KDE.
"""

from pathlib import Path
import argparse
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("points")
    parser.add_argument("boundary")
    parser.add_argument("--bandwidth", type=float, default=1500.0,
                        help="Bandwidth in CRS units (meters for EPSG:32637).")
    parser.add_argument("--resolution", type=int, default=250)
    parser.add_argument("--output", type=Path, default=Path("outputs/kde_public.png"))
    args = parser.parse_args()

    pts = gpd.read_file(args.points)
    boundary = gpd.read_file(args.boundary).to_crs(pts.crs)
    coords = np.column_stack([pts.geometry.x, pts.geometry.y])

    minx, miny, maxx, maxy = boundary.total_bounds
    xs = np.arange(minx, maxx + args.resolution, args.resolution)
    ys = np.arange(miny, maxy + args.resolution, args.resolution)
    xx, yy = np.meshgrid(xs, ys)
    sample = np.column_stack([xx.ravel(), yy.ravel()])

    kde = KernelDensity(bandwidth=args.bandwidth, kernel="gaussian").fit(coords)
    density = np.exp(kde.score_samples(sample)).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(7, 9))
    boundary.boundary.plot(ax=ax, linewidth=1)
    ax.imshow(density, extent=(minx,maxx,miny,maxy), origin="lower", aspect="equal")
    pts.plot(ax=ax, markersize=8)
    ax.set_title("Coworking-space KDE")
    ax.set_axis_off()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=200, bbox_inches="tight")
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
