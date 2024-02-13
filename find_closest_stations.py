import os
import pandas as pd
import geopy.distance
from collections import defaultdict
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

def match_bird_and_observation_data(bird_data, folder_path):
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
        DESCRIPTION.

    """
    all_bird_stations = list(zip(list(bird_data['lat'].unique()), list(bird_data['lon'].unique())))

    # Folder containing CSV files
    
    # Initialize variables to store the closest file name and distance
    closest_file = None
    min_distance = float('inf')  # Initialize with positive infinity
    pairs = dict()
    
    #### TESTING ####

    # discarded_distances = dict()
    
    #### TESTING ####

    pair_number = 1
    # Iterate through each file in the folder
    for coords in all_bird_stations:
        min_distance = None
        target_latitude, target_longitude = coords[0], coords[1]
        
        for filename in os.listdir(folder_path):  ###### MISTAKE IS HERE. TAKES SAME FILE FOR DIFFERENT COORDS
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                # print(file_path)
                with open(file_path, 'r') as file:
                    for i, line in enumerate(file):
                        if i == 8:  # Print line 5 (0-indexed)
                            # print(line)
                            break
                
                # Read latitude and longitude from the specified cells (assuming 0-indexed)
                df = pd.read_csv(file_path, sep=';', nrows=1)
                
                latitude = df.iloc[0, 2]  # Assuming latitude is in C2
                longitude = df.iloc[0, 3]  # Assuming longitude is in D2
                
                # print(f'lat: {latitude}, lon:{longitude}')
                # Calculate distance
                # distance = haversine(target_latitude, target_longitude, latitude, longitude)
                """
                FIX CALCULATION OF DISTANCE
                """
                distance = geopy.distance.distance((target_latitude, target_longitude), (latitude, longitude))
                
                # Check if the current file is closer than the previous closest file
                if min_distance:
                    if distance < min_distance:
                        
                        #### TESTING ####
                        
                        # key_name_test = f"Old_distance{pair_number}"
                        # if key_name_test in discarded_distances:
                        #     discarded_distances[key_name_test].append(distance.km)
                        # else:
                        #     discarded_distances[key_name_test] = [distance.km]
                        
                        #### TESTING ####
                        bird_coords = (target_latitude, target_longitude)
                        obs_coords = (latitude, longitude)
                        min_distance = distance
                        closest_file = filename
                else:
                    min_distance = distance
    
        key_name = f"Pair_{pair_number}"
        """
        Check if obs station exists. If they exist just append the bird coords there so many bird locations
        are linked with one obs station
        """
        print(f"The coords I'm searcing are: {obs_coords}")
        for key, value in pairs.items():
            print(f" and key {key} has these coords: {value['obs_coords']}")
            if obs_coords == value['obs_coords']:

                print(f"FOUND! I'm at {pair_number} I'll add {bird_coords} to this key {key}")
                pairs[key]['bird_coords'].append(bird_coords)
                print(f"and now I have these birds coords: {pairs[key]['bird_coords']}")
                print('----')
                break
        else:
            print(f"So I didnt replace anything but I created a new pair named with key name {key_name}")
            print("----")
            pairs[key_name] = {'bird_coords': [bird_coords], 'obs_coords': obs_coords, 'obs_file': closest_file}
            pair_number += 1

        
        # Print the closest file name and distance
        # if closest_file is not None:
        #     print(f"Bird coords: {target_latitude},{target_longitude}. File coords: {obs_coords}")
        #     print(f"The closest file is: {closest_file} with a distance of {min_distance} km.")
        # else:
        #     print("No file found.")
     # Create a dictionary to store grouped results

    return pairs
    
def create_paired_stations_map(pairs):    
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
    mymap.save("bird_map.html")

if __name__ == '__main__':
        
    filename = 'data/bird_data/nestlings_cleaned.csv'
    nestlings = pd.read_csv(filename)
    
    folder_path = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/wave-height'

    pairs = match_bird_and_observation_data(nestlings, folder_path)
    
    # Visualize
    create_paired_stations_map(pairs)

