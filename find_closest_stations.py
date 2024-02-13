import os
from handle_data import load_and_clean_nestling_data
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import geopy.distance

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
    discarded_distances = dict()
    # Folder containing CSV files
    
    # Initialize variables to store the closest file name and distance
    closest_file = None
    min_distance = float('inf')  # Initialize with positive infinity
    pairs = dict()
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
                        key_name_test = f"Old_distance{pair_number}"
                        if key_name_test in discarded_distances:
                            discarded_distances[key_name_test].append(distance)
                        else:
                            discarded_distances[key_name_test] = [distance]
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
        pairs[key_name] = {'bird_coords': (target_latitude,target_longitude), 'obs_coords': obs_coords, 'obs_file': closest_file}
        
        pair_number += 1
        # Print the closest file name and distance
        if closest_file is not None:
            print(f"Bird coords: {target_latitude},{target_longitude}. File coords: {obs_coords}")
            print(f"The closest file is: {closest_file} with a distance of {min_distance} km.")
        else:
            print("No file found.")
        
    # waves = pd.read_csv(f"data/SMHI/wave-height/{closest_file}", sep='[;,]', skiprows=8)
    
    return pairs, discarded_distances
    
def create_paired_stations_map(pairs):
    import folium
    
    """
    FIX THE ZOOM
    """
    # Create a folium map centered at a specific location (e.g., average of all coordinates)
    average_lat = sum(value[0] for pair_values in pairs.values() for key, value in pair_values.items() if 'coords' in key) / (len(pairs) * 2)
    average_lon = sum(value[1] for pair_values in pairs.values() for key, value in pair_values.items() if 'coords' in key) / (len(pairs) * 2)
    # max_lat = max()
    mymap = folium.Map(location=[average_lat, average_lon], zoom_start=2)
    for pair_key, pair_values in pairs.items():
        """
        Fix pairing stations
        """
        bird_coords = pair_values.get('bird_coords', (None, None))
        obs_coords = pair_values.get('obs_coords', (None, None))
    
        # Add markers for bird and observation coordinates
        if bird_coords != (None, None):
            folium.Marker(bird_coords, popup=f"{pair_key}: {bird_coords}", icon=folium.Icon(color='blue')).add_to(mymap)
        if obs_coords != (None, None):
            folium.Marker(obs_coords, popup=f"{pair_key}: {obs_coords}", icon=folium.Icon(color='red')).add_to(mymap)
    
        # Add line connecting bird and observation coordinates
        if bird_coords != (None, None) and obs_coords != (None, None):
            folium.PolyLine([bird_coords, obs_coords], color="purple").add_to(mymap)
    
    # Save the map as an HTML file or display it
    mymap.save('map_with_colored_markers.html')


if __name__ == '__main__':
        
    filename = 'data/bird_data/nestlings_cleaned.csv'
    nestlings = pd.read_csv(filename, nestlings=True)
    
    folder_path = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/wave-height'

    pairs = match_bird_and_observation_data(nestlings, folder_path)
    
    # Visualize
    create_paired_stations_map(pairs)

