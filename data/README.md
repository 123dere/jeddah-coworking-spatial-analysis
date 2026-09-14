# Data

## What is intentionally excluded

This repository should not automatically redistribute:

- raw Google Maps / third-party POI exports;
- private API responses;
- full ArcGIS geodatabases;
- source files whose license does not permit redistribution;
- reviewer correspondence or submission-system files.

## Recommended public analytical data

If permitted, export the minimum derived variables required to reproduce the statistical models.

### 1-km analytical table

Recommended filename:

`processed_public/jeddah_grid_1km_public.csv`

Required columns:

- `grid_id`
- `cw_presence`
- `business_density`
- `built_up_pct`
- `road_density`

### 2-km analytical table

Recommended filename:

`processed_public/jeddah_grid_2km_public.csv`

Use the same required columns.

For spatial residual analysis, a GeoPackage can additionally contain the grid geometry, but publish it only after confirming that all derived attributes can legally be redistributed.

## Why derived tables are useful

They allow readers to reproduce:

- binary logistic regression;
- Firth bias-reduced logistic regression;
- scale-sensitivity comparisons;
- non-spatial exploratory statistics.

Point-pattern analyses additionally require shareable coworking-point coordinates and a municipal boundary. If coordinate redistribution is restricted, publish the methods and aggregate results rather than the raw points.
