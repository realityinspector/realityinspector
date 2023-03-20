import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

# read the CSV file into a DataFrame
df = pd.read_csv('merged_malibu_schools_data.csv')

# remove rows without address
df = df.dropna(subset=['Business Address'])

# create a geometry column
df['geometry'] = df.apply(lambda x: Point(x.lon, x.lat), axis=1)

# create a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# get the x and y coordinates of the centroid of each geometry
x = gdf.geometry.centroid.x
y = gdf.geometry.centroid.y

# calculate the mean x and y coordinates
centroid_x = x.mean()
centroid_y = y.mean()

# create a map with a 100 mile radius
ax = gdf.to_crs(epsg=3857).plot(figsize=(10, 10), alpha=0.5, color='blue')
ctx.add_basemap(ax, zoom=8, source=ctx.providers.CartoDB.Positron, extent=(centroid_x - 50000, centroid_x + 50000, centroid_y - 50000, centroid_y + 50000))


# plot the points on the map
gdf.plot(ax=ax, markersize=20, color='red', marker='o')

# display the map
plt.show()
