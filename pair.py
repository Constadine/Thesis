import polars as pl
import numpy as np
# from geopy.distance import geodesic
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

# Load the bird population data
bird_data = pl.read_csv("data/all_bird_data/bird_data.csv")

# Load the air pressure data
air_pressure_data = pl.read_csv("data/SMHI/sea_temp_combined_data.csv")

# Strip the time part and keep only the date
bird_data = bird_data.with_columns([
    pl.col("Date").str.slice(0, 10).str.strptime(pl.Date, "%Y-%m-%d")
])

air_pressure_data = air_pressure_data.with_columns([
    pl.col("Date").str.slice(0, 10).str.strptime(pl.Date, "%Y-%m-%d")
])

# Extract unique bird coordinates
bird_coords = bird_data.select(['lat', 'lon']).unique().to_numpy()

# Extract station coordinates
station_coords = np.array([(float(lat), float(lon)) for lat, lon in 
                           (coord.split('_') for coord in air_pressure_data.columns if coord != 'Date')])

### USE THIS FOR MAXIMUM ACCURACY
### -----------------------------
# # Vectorized distance calculation using broadcasting
# distances = np.array([[geodesic(bird, station).kilometers for station in station_coords] for bird in bird_coords])

# # Find the index of the nearest station for each bird
# nearest_station_indices = np.argmin(distances, axis=1)

# # Retrieve the nearest station coordinates and distances
# nearest_stations = station_coords[nearest_station_indices]
# nearest_distances = distances[np.arange(distances.shape[0]), nearest_station_indices]

### -----------------------------


distances = haversine(
    bird_coords[:, 1][:, np.newaxis], bird_coords[:, 0][:, np.newaxis],
    station_coords[:, 1], station_coords[:, 0]
)

# Find the index of the nearest station for each bird
nearest_station_indices = np.argmin(distances, axis=1)

# Retrieve the nearest station coordinates and distances
nearest_stations = station_coords[nearest_station_indices]
nearest_distances = distances[np.arange(distances.shape[0]), nearest_station_indices]

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
distance_limit = 10
filtered_bird_data = bird_data.filter(pl.col('nearest_distance') <= distance_limit)


# Comment or uncomment this to create the csv:
filtered_bird_data.write_csv("filtered_bird_data.csv")


end_time = time.time()
print(f"Script executed in {end_time - start_time} seconds")

