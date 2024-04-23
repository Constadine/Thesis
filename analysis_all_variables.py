import os
import pandas as pd
from climate_configs import configs
from useful_methods import load_climate_data, load_bird_data
from analysis_methods import calculate_concecutive_differences
from find_and_visualize_closest_stations import match_bird_and_observation_data
import time

# Get the start time
start_time = time.time()

# Load bird data
bird_filename = os.path.join('data', 'all_bird_data', 'all_birds_cleaned.csv')
bird_data = load_bird_data(bird_filename)

# Define climate folders and variables
climate_folders = {
    "meteorologi": ["wind", "air_temperature", "air_pressure"],
    "oceanografi": ["sea_temp", "seawater_level", "wave_height"]
}

# Dictionary to store pairs DataFrames for each climate variable
pairs_dict = {}

# Initialize dictionaries to store extreme and normal DataFrames for each climate variable
extreme_data_dict = {}
normal_data_dict = {}

# Iterate over climate folders and variables
for climate_folder, climate_variables in climate_folders.items():
    for climate_variable in climate_variables:
        
        folder_path = os.path.join('data', 'SMHI', climate_folder, climate_variable)
        
        config = configs[climate_variable]
            
        # Match observation stations with bird observations
        distance_limit = config['distance_limit'] # Depending on climate variable chosen, distance limit should be adjusted. Measured in km.
        
        # Link bird observation locations with closest climate observation station
        pairs_dict[climate_variable] = match_bird_and_observation_data(bird_data, folder_path, distance_limit)
        
        # Initialize lists to store yearly DataFrames and unusable stations
        result_list = []
        no_data_for_nesting_window = []
    
        # Iterate through each file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                if filename in pairs_dict[climate_variable]['obs_file'].values:
        
                    file_path = os.path.join(folder_path, filename)
                
                    df = load_climate_data(file_path, config, 2015)
                    
                    climate_variable_column = config['value_column']
                    date_column = config['date_column']
        
                    # Filter data for period of interest
                    df_nesting_window = df[(df[date_column].dt.month.isin([4,5,6]))]
                    df_nesting_window.reset_index(drop=True, inplace=True)
    
                    if not df_nesting_window.empty:
    
                        # Group by year and calculate the mean and max for each year
                        yearly_mean = df_nesting_window.groupby(df_nesting_window[date_column].dt.year)[climate_variable_column].mean()
                        yearly_max = df_nesting_window.groupby(df_nesting_window[date_column].dt.year)[climate_variable_column].max()
            
                        # Specify the number of hours for the average
                        n_hours = config['n_hours_for_mean_conc_diff']  
                        
                        # Calculate the maximum concecutive differences
                        if climate_variable == 'air_pressure':
                            # In the case of air pressure I need to calculate std t0 account for the specific characteristics and variability of air pressure in each location.
                            difference_threshold = df_nesting_window[climate_variable_column].std()
                        else:
                            difference_threshold = config['value_threshold_for_conc_diff']
                            
                        max_difference_df = calculate_concecutive_differences(df_nesting_window, n_hours, climate_variable_column, difference_threshold)
                        
                        ## MAKE IT A FUNCTION DUDE ## 03-04
                        
                        # Convert the results to a DataFrame
                        yearly_df = pd.DataFrame({
                            'Year': yearly_mean.index,
                            'Station': filename,
                            'Mean': yearly_mean.values,
                            'Max': yearly_max.values,
                            'All Time Max Diff Date': max_difference_df['All Time Max Diff Date'].values,
                            'All Time Max Diff Value': max_difference_df['All Time Max Diff Value'].values,
                            'Above Threshold Dates': max_difference_df['Above Threshold Dates'],
                            'Above Threshold Values': max_difference_df['Above Threshold Values'],
                        })
                
                        # Define the variable name dynamically
                        variable_name = f"{climate_variable}_{climate_folder}"
                        
                        # Add the DataFrame to the dictionary with the filename as the key
                        result_list.append(yearly_df)
                    else:
                        print(f"{filename} is not in pairs so skiiip")
                else:
                    # print(f"No data for April in {filename}")
                    no_data_for_nesting_window.append(filename)
        
        # Concatenate all DataFrames in the list into a single DataFrame
        result_df = pd.concat(result_list, ignore_index=True)
        
        # Store extreme and normal data for the current climate variable
        extreme_data_dict[climate_variable] = result_df[result_df['Above Threshold Values'].apply(lambda x: len(x) > 0)]
        normal_data_dict[climate_variable] = result_df[result_df['Above Threshold Values'].apply(lambda x: len(x) == 0)]
        
         # Initialize a list to store the merged extreme events
        merged_extremes_list = []
 
    
 
 ### TO FIX. Now I don't merge the extremes and pairs right. I need to somehow
# get the unique bird locations and then the year of interest.    
 
    
 
        # Iterate over each row in the extreme events DataFrame
        for index, row in extreme_data_dict[climate_variable].iterrows():
            # Extract the station from the extreme event
            station = row['Station']
            
            # Filter the pairs DataFrame to include only records for the same station
            station_pairs = pairs_dict[climate_variable][pairs_dict[climate_variable]['obs_file'] == station]
            
            # Merge the extreme event with the pairs DataFrame based on unique bird coordinates
            merged_extreme = pd.merge(pd.DataFrame(row).T, station_pairs[['bird_lat', 'bird_lon']].drop_duplicates(), how='inner')
 
            # Filter the merged DataFrame to only include the years where extreme events have occurred
            merged_extreme_years = merged_extreme[merged_extreme['Year'].isin(row['Year'])]
            
            # Append the filtered merged DataFrame to the list
            merged_extremes_list.append(merged_extreme_years)
 
        # Concatenate all merged extreme events into a single DataFrame
        merged_extremes = pd.concat(merged_extremes_list)
        
        # Initialize a list to store the merged normal events
        merged_normals_list = []
 
        # Iterate over each row in the normal events DataFrame
        for index, row in normal_data_dict[climate_variable].iterrows():
            # Extract the station from the normal event
            station = row['Station']
            
            # Filter the pairs DataFrame to include only records for the same station
            station_pairs = pairs_dict[climate_variable][pairs_dict[climate_variable]['obs_file'] == station]
            
            # Merge the normal event with the pairs DataFrame based on unique bird coordinates
            merged_normal = pd.merge(pd.DataFrame(row).T, station_pairs[['bird_lat', 'bird_lon']].drop_duplicates(), how='inner')
 
            # Filter the merged DataFrame to only include the years where normal events have occurred
            merged_normal_years = merged_normal[merged_normal['Year'].isin(row['Year'])]
            
            # Append the filtered merged DataFrame to the list
            merged_normals_list.append(merged_normal_years)
 
        # Concatenate all merged normal events into a single DataFrame
        merged_normals = pd.concat(merged_normals_list)
        
# Get the end time
end_time = time.time()

# Calculate the execution time
execution_time = end_time - start_time

# Print the execution time
print(f"Execution time: {execution_time} seconds")
