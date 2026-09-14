# Data dictionary

| Variable | Type | Unit | Description |
|---|---|---|---|
| `grid_id` | string/integer | — | Unique grid-cell identifier |
| `cw_presence` | binary | 0/1 | 1 if at least one coworking facility occurs in the grid cell; otherwise 0 |
| `business_density` | numeric | POIs/km² | Business/commercial POI density |
| `built_up_pct` | numeric | % | Percentage of grid-cell area classified as built-up |
| `road_density` | numeric | km/km² | Total road length divided by grid-cell area |
| `geometry` | polygon | projected CRS | Optional geometry for spatial residual analysis |

## Spatial reference

The original metric analysis used **WGS 84 / UTM Zone 37N (EPSG:32637)** for distance, area, density, KDE, nearest-neighbour, and Ripley's L calculations.

## Outcome definition

The public regression workflow uses a binary outcome because coworking observations are sparse at grid level.

- 1-km grid: 1,412 cells; 39 presence cells.
- 2-km grid: 381 cells; 29 presence cells.
