import polars as pl
import numpy as np
# from geopy.distance import geodesic
from climate_configs import configs
import time
start_time = time.time()

def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    distance = R * c
    return distance

## ...:::Choose climate variable:::...
'''
OPTIONS = 'air_pressure' | 'air_temperature' | 'seawater_level' | 'sea_temp' | 'wave_height' | 'wind'
'''
climate_variable = 'wind'
config = configs[climate_variable]

## ..::Load datasets::..

'''The bird dataset used for this script need to have been prepared by the 'prepare_bird_data.py' script'''
# Load the bird population data
bird_data = pl.read_csv("data/all_bird_data/bird_data.csv")

# Load the climate variable data
climate_data = pl.read_csv(f"data/SMHI/{climate_variable}.csv")

## ..::Clean bird data::.. 

# Strip the time part and keep only the date
bird_data = bird_data.with_columns([
    pl.col("Date").str.slice(0, 10).str.strptime(pl.Date, "%Y-%m-%d")
])

climate_data = climate_data.with_columns([
    pl.col("Date").str.slice(0, 10).str.strptime(pl.Date, "%Y-%m-%d")
])

# Extract unique bird coordinates
bird_coords = bird_data.select(['lat', 'lon']).unique().to_numpy()

# Extract station coordinates
station_coords = np.array([(float(lat), float(lon)) for lat, lon in 
                           (coord.split('_')[0:2] for coord in climate_data.columns if coord != 'Date')])

''' OPTIONS FOR DISTANCE CALCULATION '''

''' 1) USE THIS FOR MAXIMUM ACCURACY '''
### 1-----------------------------
# # Vectorized distance calculation using broadcasting (Uncomment the geopy import)
# distances = np.array([[geodesic(bird, station).kilometers for station in station_coords] for bird in bird_coords])

# # Find the index of the nearest station for each bird
# nearest_station_indices = np.argmin(distances, axis=1)

# # Retrieve the nearest station coordinates and distances
# nearest_stations = station_coords[nearest_station_indices]
# nearest_distances = distances[np.arange(distances.shape[0]), nearest_station_indices]
### 1-----------------------------1

''' 2) USE THIS FOR SPEED  '''

### 2-----------------------------2
distances = haversine(
    bird_coords[:, 1][:, np.newaxis], bird_coords[:, 0][:, np.newaxis],
    station_coords[:, 1], station_coords[:, 0]
)

# Find the index of the nearest station for each bird
nearest_station_indices = np.argmin(distances, axis=1)

# Retrieve the nearest station coordinates and distances
nearest_stations = station_coords[nearest_station_indices]
nearest_distances = distances[np.arange(distances.shape[0]), nearest_station_indices]
### 2-----------------------------2

# Convert nearest_stations to the format 'lat_lon'
nearest_stations_str = [f"{lat}_{lon}" for lat, lon in nearest_stations]


# Map back to the original bird data to include the nearest station info for all birds
bird_coords_df = pl.DataFrame({
    'lat': bird_coords[:, 0],
    'lon': bird_coords[:, 1],
    'nearest_station': nearest_stations_str,
    'nearest_distance': nearest_distances
})

# Join with the original bird data to map nearest station info
bird_data = bird_data.join(bird_coords_df, on=['lat', 'lon'])

# Filter based on the distance limit
distance_limit = config['distance_limit']
paired_bird_data = bird_data.filter(pl.col('nearest_distance') <= distance_limit)

# Comment or uncomment this to create the csv:
paired_bird_data.write_csv(f"paired_birds_with_{climate_variable}.csv")

end_time = time.time()
print(f"Script executed in {end_time - start_time} seconds")

