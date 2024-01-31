import pandas as pd
import numpy as np

ds = pd.read_csv('data/bird_data/occurrence.txt', sep="\t", on_bad_lines='skip')


# Clean dataset
ds.dropna(axis=1, how='all', inplace=True)

col_to_drop1 = ['recordedBy', 'organismQuantity', 'taxonomicStatus']
col_to_drop2 = [x for x in ds.columns if len(ds[x].unique()) == 1]
ds.rename(columns={'decimalLatitude': 'lat', 'decimalLongitude': 'lon'}, inplace=True)


ds = ds.drop(columns=col_to_drop1 + col_to_drop2)


nestlings = ds[ds.lifeStage == 'Nestling']

overten = nestlings.individualCount[nestlings.individualCount >= 10]
belowten = nestlings.individualCount[nestlings.individualCount < 10]

# Vizualize
# import plotly.express as px
# import plotly.io as pio
# pio.renderers.default='browser'


# color_scale = [(0, 'orange'), (1,'red')]

# fig = px.scatter_mapbox(nestlings, 
#                         lat="lat", 
#                         lon="lon", 
#                         hover_name="eventDate", 
#                         hover_data=["individualCount"],
#                         color="individualCount",
#                         color_continuous_scale=color_scale,
#                         size="individualCount",
#                         zoom=8, 
#                         height=800,
#                         width=800)

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # fig.show()

# fig = px.bar(nestlings['month'].value_counts().sort_index().reset_index(),
#              x='month',
#              y='count',
#              labels={'index': 'Month', 'month': 'Occurrences'},
#              title='Occurrences by Month')

# fig.update_layout(xaxis=dict(type='category'))

# fig.show()

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Set up the plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Set the map extent to Europe
ax.set_extent([8, 16, 54, 61], crs=ccrs.PlateCarree())

# Plot the temperature data
im = ax.pcolormesh(ds.lon, ds.lat, ds.individualCount, cmap='RdYlGn', transform=ccrs.PlateCarree())

fig.show()
