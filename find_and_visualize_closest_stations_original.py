import os
import pandas as pd
import geopy.distance

# def match_bird_and_observation_data(bird_data, folder_path, distance_limit=30):
#     """
#     Parameters
#     ----------
#     bird_data : pd.DataFrame
#         DESCRIPTION.
#     folder_path : str
#         DESCRIPTION.

#     Returns
#     -------
#     pairs : dict
#         Detect closest observation stations to the bird observation locations and pair them in dictionary 
#         so they can be used for correlation.

#     """
#     # Create a dictionary to store file information (coordinates and filenames)
#     file_info = {}
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".csv"):
#             file_path = os.path.join(folder_path, filename)
            
#             # Read latitude and longitude from the specified cells (assuming 0-indexed)
#             if 'meteorologi' in folder_path:
#                 df = pd.read_csv(file_path, sep=';', skiprows=8, nrows=1, header=None)
#                 latitude = df.iloc[0, 3]  
#                 longitude = df.iloc[0, 4] 
#             elif 'oceanografi' in folder_path:    
#                 df = pd.read_csv(file_path, sep=';', nrows=1)
#                 latitude = df.iloc[0, 2]  
#                 longitude = df.iloc[0, 3]  
            
#             file_info[filename] = {'latitude': latitude, 'longitude': longitude}

#     # Use unique bird coordinates
#     all_bird_stations = list(zip(bird_data['lat'].unique(), bird_data['lon'].unique()))

#     # Initialize variables to store the closest file name and distance
#     pairs = dict()
#     pair_number = 1

#     # Iterate through each bird data location
#     for bird_coords in all_bird_stations:
#         min_distance = None
#         closest_file = None
        
#         # Iterate through each file in the folder
#         for filename, obs_info in file_info.items():
#             obs_coords = (obs_info['latitude'], obs_info['longitude'])
            
#             # Calculate distance using geopy
#             distance = geopy.distance.distance(bird_coords, obs_coords)
            
#             # Check if the current file is closer than the previous closest file
#             if min_distance is None or distance < min_distance:
#                 min_distance = distance
#                 closest_file = filename

#         # Check if the minimum distance is within the limit
#         if min_distance.km < distance_limit:
#             obs_coords = (file_info[closest_file]['latitude'], file_info[closest_file]['longitude'])
#             key_name = f"Pair_{pair_number}"
            
#             # Check if observation station already exists in pairs dictionary
#             if obs_coords in [value['obs_coords'] for value in pairs.values()]:
#                 for key, value in pairs.items():
#                     if value['obs_coords'] == obs_coords:
#                         pairs[key]['bird_coords'].append(bird_coords)
#                         break
#             else:
#                 pairs[key_name] = {'bird_coords': [bird_coords], 'obs_coords': obs_coords, 'obs_file': closest_file}
#                 pair_number += 1

#     return pairs
    

def match_bird_and_observation_data(bird_data, folder_path, distance_limit=30):
    # Create a dictionary to store file information (coordinates and filenames)
    file_info = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Read latitude and longitude from the specified cells (assuming 0-indexed)
            if 'meteorologi' in folder_path:
                df = pd.read_csv(file_path, sep=';', skiprows=8, nrows=1, header=None)
                latitude = df.iloc[0, 3]  
                longitude = df.iloc(0, 4)
            elif 'oceanografi' in folder_path:    
                df = pd.read_csv(file_path, sep=';', nrows=1)
                latitude = df.iloc[0, 2]  
                longitude = df.iloc[0, 3]  
            
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

    return result_df

def create_paired_stations_map(pairs, output_file_name):   
    """
    Parameters
    ----------
    pairs : dict
        DESCRIPTION.
    output_file_name : str
        Should be an .html file.

    Returns
    -------
    .html file

    """
    import folium
    from folium import PolyLine
    
    # Create a folium map centered around the average coordinates
    average_coords = [
        sum(coord[0] for pair in pairs.values() for coord in pair['bird_coords']) / len([coord for pair in pairs.values() for coord in pair['bird_coords']]),
        sum(coord[1] for pair in pairs.values() for coord in pair['bird_coords']) / len([coord for pair in pairs.values() for coord in pair['bird_coords']])
    ]
    
    mymap = folium.Map(location=average_coords, zoom_start=8)
    
    # Add markers and connecting lines for each pair
    for pair_key, pair_value in pairs.items():
        obs_coords = pair_value['obs_coords']
        
        # Add red marker for observation coordinates
        folium.Marker(
            location=obs_coords,
            icon=folium.Icon(color='red'),
            popup=f"Pair: {pair_key}<br>Obs Coords: {obs_coords}",
        ).add_to(mymap)
    
        # Add blue markers for bird coordinates
        for bird_coord in pair_value['bird_coords']:
            folium.Marker(
                location=bird_coord,
                icon=folium.Icon(color='blue'),
                popup=f"Pair: {pair_key}<br>Bird Coords: {bird_coord}",
            ).add_to(mymap)
    
            # Add connecting lines between bird and observation coordinates
            PolyLine(locations=[bird_coord, obs_coords], color="black").add_to(mymap)
    
    # Save the map to an HTML file
    output_file_name = output_file_name
    mymap.save(output_file_name)

if __name__ == '__main__':
        
    filename = 'data/all_bird_data/all_birds_cleaned.csv'
    bird_data = pd.read_csv(filename)
    grouped_bird_data = bird_data.groupby(['eventDate', 'lifeStage', 'lat', 'lon']).agg({'individualCount': 'sum'}).reset_index()

    
    # Choose variable folder
    CLIMATE_VARIABLE = "seawater-level"
    CLIMATE_FOLDER = ['oceanografi' ,'meteorologi']
    folder_path = f'/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/{CLIMATE_FOLDER[0]}/{CLIMATE_VARIABLE}'

    DISTANCE_LIMIT = 20
    # Match observation stations with bird observations
    pairs = match_bird_and_observation_data(grouped_bird_data, folder_path, DISTANCE_LIMIT)
    
    # Visualize
    # output_name = f'all_nestlings_paired_stations_map_{CLIMATE_VARIABLE}_{DISTANCE_LIMIT}km.html'
    # create_paired_stations_map(pairs, output_name)

