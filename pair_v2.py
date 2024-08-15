import pandas as pd
import os


# Define the path to the climate data folder
climate_data_folder = '/home/kotikos/Education/UoG/Earth Science Master/Thesis/data/SMHI'

# Load the bird data CSV file
bird_data_path = '/home/kotikos/Education/UoG/Earth Science Master/Thesis/paired_birds_all_climate_data.csv'
bird_data = pd.read_csv(bird_data_path)

# Step 1: Extract year from the Date column in bird data
bird_data['Year'] = pd.to_datetime(bird_data['Date']).dt.year

# Initialize a list to hold results for merging later
bird_data_list = []

# Get the list of climate variables and corresponding CSV file names
climate_variables = ['air_pressure', 'air_temperature', 'seawater_level', 
                     'sea_temp', 'wave_height', 'wind']
climate_files = [f'{var}.csv' for var in climate_variables]

# Iterate over each climate variable to calculate yearly means for the closest stations
for variable, file_name in zip(climate_variables, climate_files):
    station_column = f'{variable}_nearest_station'
    
    # Load the corresponding climate data file
    climate_data_path = os.path.join(climate_data_folder, file_name)
    climate_data = pd.read_csv(climate_data_path)
    
    if station_column in bird_data.columns:
        # Identify valid stations that are present in the climate data
        valid_stations = [station for station in bird_data[station_column].dropna().unique() if station in climate_data.columns]
        
        if valid_stations:
            # Filter climate data for the valid stations
            relevant_climate_data = climate_data[['Date'] + valid_stations]
            relevant_climate_data['Year'] = pd.to_datetime(relevant_climate_data['Date']).dt.year
            
            # Ensure that the station data is numeric
            relevant_climate_data[valid_stations] = relevant_climate_data[valid_stations].apply(pd.to_numeric, errors='coerce')
            
            # Calculate yearly mean for each station
            yearly_mean = relevant_climate_data.groupby('Year').mean(numeric_only=True).reset_index()
            
            # Melt the yearly mean to have one station per row
            yearly_mean_melted = yearly_mean.melt(id_vars='Year', 
                                                  var_name=f'{variable}_station', 
                                                  value_name=f'{variable}_values')
            
            # Merge the calculated yearly means with the bird data based on the station and year
            bird_data_temp = bird_data.merge(yearly_mean_melted, 
                                             left_on=['Year', station_column], 
                                             right_on=['Year', f'{variable}_station'], 
                                             how='left')
            
            # Fill missing values with -1
            bird_data_temp[f'{variable}_values'] = bird_data_temp[f'{variable}_values'].fillna(-1)
            
            # Drop the extra station column after merging
            bird_data_temp.drop(columns=[f'{variable}_station'], inplace=True)
            
            bird_data_list.append(bird_data_temp)

# Combine all the merged data together
final_bird_data = bird_data_list[0]

for data in bird_data_list[1:]:
    final_bird_data = final_bird_data.combine_first(data)

# Step 4: Drop the columns related to the nearest station and distance
columns_to_drop = [f'{variable}_nearest_station' for variable in climate_variables] + \
                  [f'{variable}_nearest_distance' for variable in climate_variables]
final_bird_data = final_bird_data.drop(columns=columns_to_drop)

# Define the new column order
new_column_order = ['Year', 'lat', 'lon', 'total_population', 'air_pressure_values', 
                    'air_temperature_values', 'wind_values', 'sea_temp_values', 
                    'seawater_level_values', 'wave_height_values']

# Reorder the columns and drop the 'Date' column
final_bird_data = final_bird_data[new_column_order]
final_bird_data.to_csv('data_for_correlation.csv', index=False)