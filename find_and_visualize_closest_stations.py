import os
import pandas as pd
import geopy.distance
from useful_methods import find_observation_coords

def match_bird_and_observation_data(bird_data, folder_path, distance_limit=30):
    # Create a dictionary to store file information (coordinates and filenames)
    file_info = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Extract latitude and longitude values from the cell below and next to it
            latitude, longitude = find_observation_coords(file_path)
            file_info[filename] = {'latitude': latitude, 'longitude': longitude}

    # Use unique bird coordinates
    all_bird_stations = list(zip(bird_data['lat'].unique(), bird_data['lon'].unique()))

    # Initialize variables to store the closest file name and distance
    pairs = []

    # Iterate through each bird data location
    for bird_coords in all_bird_stations:
        min_distance = None
        closest_file = None
        obs_coords = None
        
        # Iterate through each file in the folder
        for filename, obs_info in file_info.items():
            obs_coords = (obs_info['latitude'], obs_info['longitude'])
            
            # Calculate distance using geopy
            distance = geopy.distance.distance(bird_coords, obs_coords)
            
            # Check if the current file is closer than the previous closest file
            if min_distance is None or distance < min_distance:
                min_distance = distance
                closest_file = filename

        # Check if the minimum distance is within the limit
        if min_distance.km < distance_limit:
            obs_coords = (file_info[closest_file]['latitude'], file_info[closest_file]['longitude'])
            bird_matches = bird_data[(bird_data['lat'] == bird_coords[0]) & (bird_data['lon'] == bird_coords[1])]
            
            for index, bird_row in bird_matches.iterrows():
                pairs.append({
                    'obs_file': closest_file,
                    'obs_lat': file_info[closest_file]['latitude'],
                    'obs_lon': file_info[closest_file]['longitude'],
                    'bird_lat': bird_coords[0],
                    'bird_lon': bird_coords[1],
                    'individualCount': bird_row['individualCount'],
                    'eventDate': bird_row['eventDate'],
                    'lifeStage': bird_row['lifeStage']
                })

    # Create a DataFrame from the list of dictionaries
    result_df = pd.DataFrame(pairs)
    
    # Group the pairs as very records are from the same area. So basically add all the populations of specific bird locations
    result_df.eventDate = pd.to_datetime(result_df.eventDate)
    result_df['year'] = result_df['eventDate'].dt.year
    result_df['month'] = result_df['eventDate'].dt.month
    result_df = result_df.groupby(by=['obs_file','obs_lat', 'obs_lon', 'bird_lat', 'bird_lon', 'lifeStage', 'year', 'month'])['individualCount'].sum().reset_index()

    return result_df

def create_paired_stations_map(pairs_df, output_file_name):   
    """
    Parameters
    ----------
    pairs_df : pandas DataFrame
        DataFrame containing paired station data. It should have columns 'obs_lat', 'obs_lon', 'bird_lat', 'bird_lon'.
    output_file_name : str
        Name of the output HTML file.

    Returns
    -------
    .html file

    """
    import folium
    from folium import PolyLine
    
    # Calculate average coordinates
    average_obs_lat = pairs_df['obs_lat'].mean()
    average_obs_lon = pairs_df['obs_lon'].mean()
    average_bird_lat = pairs_df['bird_lat'].mean()
    average_bird_lon = pairs_df['bird_lon'].mean()
    average_coords = [(average_obs_lat + average_bird_lat) / 2, (average_obs_lon + average_bird_lon) / 2]
    
    # Create a folium map centered around the average coordinates
    mymap = folium.Map(location=average_coords, zoom_start=8)
    
    # Add markers and connecting lines for each pair
    for index, row in pairs_df.iterrows():
        obs_coords = (row['obs_lat'], row['obs_lon'])
        bird_coords = (row['bird_lat'], row['bird_lon'])
        
        # Add red marker for observation coordinates
        folium.Marker(
            location=obs_coords,
            icon=folium.Icon(color='red'),
            popup=f"Pair: {index}<br>Obs Coords: {obs_coords}",
        ).add_to(mymap)
    
        # Add blue marker for bird coordinates
        folium.Marker(
            location=bird_coords,
            icon=folium.Icon(color='blue'),
            popup=f"Pair: {index}<br>Bird Coords: {bird_coords}",
        ).add_to(mymap)
    
        # Add connecting lines between bird and observation coordinates
        PolyLine(locations=[bird_coords, obs_coords], color="black").add_to(mymap)
    
    # Save the map to an HTML file
    mymap.save(output_file_name)
    

if __name__ == '__main__':
        
    filename = 'data/all_bird_data/all_birds_cleaned.csv'
    bird_data = pd.read_csv(filename)
    grouped_bird_data = bird_data.groupby(['eventDate', 'lifeStage', 'lat', 'lon']).agg({'individualCount': 'sum'}).reset_index()

    
    # Choose folder to load climate data
    # CLIMATE_FOLDER_OPTIONS = "meteorologi", "oceanografi"
    CLIMATE_FOLDER= "oceanografi"
    
    # CLIMATE_VARIABLE_OPTIONS = "wind", "air_temperature", "air_pressure", "sea_temp", "seawater_level", "wave_height"
    CLIMATE_VARIABLE = "seawater_level"
    
    folder_path = os.path.join('data', 'SMHI', CLIMATE_FOLDER, CLIMATE_VARIABLE)

    DISTANCE_LIMIT = 10
    # Match observation stations with bird observations
    pairs = match_bird_and_observation_data(grouped_bird_data, folder_path, DISTANCE_LIMIT)
    
    # Visualize
    output_name = f'all_nestlings_paired_stations_map_{CLIMATE_VARIABLE}_{DISTANCE_LIMIT}km.html'
    create_paired_stations_map(pairs, output_name)

