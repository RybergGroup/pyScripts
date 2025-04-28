import sys
import geopandas as gpd
import pandas as pd

# 1. Get points file from command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} points.csv")
    sys.exit(1)

points_file = sys.argv[1]

# 2. Paths
polygon_file = 'sockenstad.gpkg'  # assuming it is in the same folder
polygon_layer = 'sockenstad'      # you can adjust if your layer name is different
output_file = 'points_with_sockenstad.csv'

# 3. Load polygons
polygons = gpd.read_file(polygon_file, layer=polygon_layer)

# 4. Load points
points_df = pd.read_csv(points_file)
points = gpd.GeoDataFrame(
    points_df,
    geometry=gpd.points_from_xy(points_df.longitude, points_df.latitude),
    crs="EPSG:4326"
)

# 5. Reproject points to match polygons, if needed
if points.crs != polygons.crs:
    points = points.to_crs(polygons.crs)

# 6. Spatial join: find sockenstadname for each point
joined = gpd.sjoin(points, polygons[['sockenstadnamn', 'geometry']], how="left", predicate='within')

# 7. Drop geometry column and output to CSV
joined.drop(columns=['geometry', 'index_right']).to_csv(output_file, index=False)

print(f"Finished! Output saved to {output_file}")

