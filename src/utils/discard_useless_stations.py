import os
from shutil import move
import pandas as pd
import folium

# Function to check coordinates and move files
def check_and_move_files(folder_path):
    
    # Create a folder for discarded files if it doesn't exist
    discarded_folder = os.path.join(folder_path, 'Discarded')
    if not os.path.exists(discarded_folder):
        os.makedirs(discarded_folder)

    files_moved = 0
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Read latitude and longitude from the specified cells (assuming 0-indexed)
            if 'airtemperatureInstant' in folder_path or 'airPressure' in folder_path:
                df = pd.read_csv(file_path, sep=';', skiprows=7, nrows=1, header=None)
                latitude = df.iloc[0, 3]  
                longitude = df.iloc[0, 4]
            elif 'wind' in folder_path:
                df = pd.read_csv(file_path, sep=';', skiprows=8, nrows=1, header=None)
                latitude = df.iloc[0, 3]  
                longitude = df.iloc[0, 4]
                print(latitude, longitude)
                
            # Check if coordinates are within specified ranges

            CONDITIONS = [(57.6678 <= latitude <= 68.4324 and 12.1218 <= longitude <= 16.6843) or (latitude >= 66.0689)
                          or (latitude >= 64.0744 and longitude <= 20.15) or (56.38 <= latitude <= 57.4981 and  13.0601 <= longitude <= 15.8009)]
            if any(CONDITIONS):
                print(f"Moving file '{filename}' to 'Discarded' folder (lat:{latitude}, lon:{longitude}.")
                move(file_path, os.path.join(discarded_folder, filename))
                files_moved += 1
            else:
                print(f"File '{filename}' coordinates are ok.")
    print(f'Moved {files_moved} files')

def visualize_stations(folder_path):
    m = folium.Map(location=[62, 14], zoom_start=5)

    def add_marker(latitude, longitude, filename, color):
        popup_text = f"<b>File:</b> {filename}<br><b>Latitude:</b> {latitude}<br><b>Longitude:</b> {longitude}"
        folium.Marker(location=[latitude, longitude], popup=popup_text, icon=folium.Icon(color=color)).add_to(m)


    def process_folder(folder_path, color):
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                 file_path = os.path.join(folder_path, filename)
                             
                 # Read latitude and longitude from the specified cells (assuming 0-indexed)
                 if 'airtemperatureInstant' in folder_path or 'airPressure' in folder_path:
                     df = pd.read_csv(file_path, sep=';', skiprows=7, nrows=1, header=None)
                     latitude = df.iloc[0, 3]  
                     longitude = df.iloc[0, 4]
                 elif 'wind' in folder_path:
                     df = pd.read_csv(file_path, sep=';', skiprows=8, nrows=1, header=None)
                     latitude = df.iloc[0, 3]  
                     longitude = df.iloc[0, 4]
                        
                 add_marker(latitude, longitude, filename, color)

    # Process kept stations (blue)
    process_folder(folder_path, 'blue')

    # Process discarded stations (red)
    discarded_folder = os.path.join(folder_path, 'Discarded')
    if os.path.exists(discarded_folder):
        process_folder(discarded_folder, 'red')

    m.save('stations_map.html')


# Specify the folder containing Excel files
folder_path = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/meteorologi/airtemperatureInstant'

# Call the function to check and move files
check_and_move_files(folder_path)

# Specify the folder containing Excel files
visualize_stations(folder_path)
