import os
import pandas as pd
import geopy.distance
from math import radians, sin, cos, sqrt, atan2
from handle_data import load_and_clean_nestling_data

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of Earth in kilometers

    return distance

def match_bird_and_observation_data(bird_data, folder_path, distance_limit=30):
    """
    Parameters
    ----------
    bird_data : pd.DataFrame
        DESCRIPTION.
    folder_path : str
        DESCRIPTION.

    Returns
    -------
    pairs : dict
        Detect closest observation stations to the bird observation locations and pair them in dictionary 
        so they can be used for correlation.

    """
    all_bird_stations = list(zip(list(bird_data['lat'].unique()), list(bird_data['lon'].unique())))
    
    # Initialize variables to store the closest file name and distance
    closest_file = None
    pairs = dict()
    pair_number = 1
    times_in_sus_station = 0
    # Iterate through each file in the folder for each bird data location
    for coords in all_bird_stations:
        min_distance = None
        target_latitude, target_longitude = coords[0], coords[1]
        
        for filename in os.listdir(folder_path):  ###### MISTAKE IS HERE. TAKES SAME FILE FOR DIFFERENT COORDS
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                
                # Read latitude and longitude from the specified cells (assuming 0-indexed)
                df = pd.read_csv(file_path, sep=';', nrows=1)
                
                latitude = df.iloc[0, 2]  # Assuming latitude is in C2
                longitude = df.iloc[0, 3]  # Assuming longitude is in D2
                
                # distance = haversine(target_latitude, target_longitude, latitude, longitude)
                """
                FIX CALCULATION OF DISTANCE
                """
                distance = geopy.distance.distance((target_latitude, target_longitude), (latitude, longitude))
                
                # Check if the current file is closer than the previous closest file
                if min_distance:
                    if distance < min_distance:
                        bird_coords = (target_latitude, target_longitude)
                        obs_coords = (latitude, longitude)
                        min_distance = distance
                        closest_file = filename
                else:
                    bird_coords = (target_latitude, target_longitude)
                    obs_coords = (latitude, longitude)
                    min_distance = distance
                    closest_file = filename
        """
        FIX. min_distance is being calculated again before going in the if
        """
        
        if min_distance.km < distance_limit:
            key_name = f"Pair_{pair_number}"
            """
            Check if obs station exists. If they exist just append the bird coords there so many bird locations
            are linked with one obs station
            """
            # print(f"The coords I'm searcing are: {obs_coords}")
            for key, value in pairs.items():
                # print(f" and key {key} has these coords: {value['obs_coords']}")
                if obs_coords == value['obs_coords']:
    
                    # print(f"FOUND! I'm at {pair_number}. I'll add {bird_coords} to this key {key}")
                    pairs[key]['bird_coords'].append(bird_coords)
                    # print(f"and now I have these birds coords: {pairs[key]['bird_coords']}")
                    # print('----')
                    break
            else:
                # print(f"So I didnt replace anything but I created a new pair named with key name {key_name}")
                # print("----")
                pairs[key_name] = {'bird_coords': [bird_coords], 'obs_coords': obs_coords, 'obs_file': closest_file}
                pair_number += 1


    return pairs
    
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
    nestlings = pd.read_csv(filename)
    
    folder_path = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/wave-height'

    pairs = match_bird_and_observation_data(nestlings, folder_path)
    
    # Visualize
    create_paired_stations_map(pairs, 'WH-all_birds_paired_stations_map.html')

