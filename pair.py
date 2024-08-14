import polars as pl
import numpy as np
from climate_configs import configs
import time

start_time = time.time()

def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    distance = R * c
    return distance

CLIMATE_VARIABLES = ['air_pressure', 'air_temperature', 'seawater_level', 'sea_temp', 'wave_height', 'wind']

# Load the bird population data
bird_data = pl.read_csv("data/all_bird_data/bird_data.csv")

# Convert bird data Date column to datetime and strip time part
bird_data = bird_data.with_columns([
    pl.col("Date").str.slice(0, 10).str.strptime(pl.Date, "%Y-%m-%d")
])

# Extract unique bird coordinates
bird_coords = bird_data.select(['lat', 'lon']).unique().to_numpy()

# Initialize the combined data with the original bird data
combined_bird_data = bird_data

for variable in CLIMATE_VARIABLES:
    # Load the climate variable data
    climate_data = pl.read_csv(f"data/SMHI/{variable}.csv")
    config = configs[variable]
    # Convert climate data Date column to datetime
    climate_data = climate_data.with_columns([
        pl.col("Date").str.slice(0, 10).str.strptime(pl.Date, "%Y-%m-%d")
    ])
    
    # Extract station coordinates
    station_coords = np.array([
        (float(lat), float(lon)) 
        for coord in climate_data.columns if coord != 'Date'
        for lat, lon in [coord.split('_')[:2]]  # Only take the first two parts
    ])

    # Calculate distances using Haversine function
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
    
    # Create a DataFrame to store the nearest station info for this variable
    bird_coords_df = pl.DataFrame({
        'lat': bird_coords[:, 0],
        'lon': bird_coords[:, 1],
        f'{variable}_nearest_station': nearest_stations_str,
        f'{variable}_nearest_distance': nearest_distances
    })
    
    # Filter out stations that are too distant according to the configuration
    distance_limit = config['distance_limit']
    bird_coords_df = bird_coords_df.filter(pl.col(f'{variable}_nearest_distance') <= distance_limit)
    
    # Perform a left join to ensure all bird locations are included
    combined_bird_data = combined_bird_data.join(bird_coords_df, on=['lat', 'lon'], how='left')

# Save the final combined data to a CSV file
combined_bird_data.write_csv("paired_birds_all_climate_data.csv")

end_time = time.time()
print(f"Script executed in {end_time - start_time} seconds")
