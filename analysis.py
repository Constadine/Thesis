import os
import pandas as pd
from climate_configs import configs
from useful_methods import load_climate_data, load_bird_data
from analysis_methods import calculate_concecutive_differences
from find_and_visualize_closest_stations import match_bird_and_observation_data

# ME TO MALAKO ALKIKO MH MAS G@M@S KIOLAS
if __name__ == '__main__':
    
    # Load bird data
    bird_filename =  os.path.join('data', 'all_bird_data', 'all_birds_cleaned.csv')
    bird_data = load_bird_data(bird_filename)

    # Choose folder to load climate data
    ### CLIMATE_FOLDER_OPTIONS = "meteorologi", "oceanografi"
    CLIMATE_FOLDER = "oceanografi"
    
    ### CLIMATE_VARIABLE_OPTIONS = "wind", "air_temperature", "air_pressure", "sea_temp", "seawater_level", "wave_height"
    CLIMATE_VARIABLE = "wave_height"
    folder_path = os.path.join('data', 'SMHI', CLIMATE_FOLDER, CLIMATE_VARIABLE)
    
    config = configs[CLIMATE_VARIABLE]
    
    # Match observation stations with bird observations
    distance_limit = config['distance_limit'] # Depending on climate variable chosen, distance limit should be adjusted. Measured in km.
    
    # Link bird observation locations with closest climate observation station
    pairs = match_bird_and_observation_data(bird_data, folder_path, distance_limit)
    
    # Initialize an empty list to store the results
    result_list = []

    # Initialize an empty list to keep unusable stations (not paired with any bird observation record)
    no_data_for_nesting_window = []

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            if filename in pairs['obs_file'].values:
    
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
                    n_hours = config['n_hours_for_mean_conc_diff']  # You can adjust this based on your requirements
                    
                    # Calculate the maximum concecutive differences
                    if CLIMATE_VARIABLE == 'air_pressure':
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
            
                    # Add the DataFrame to the dictionary with the filename as the key
                    result_list.append(yearly_df)
                else:
                    print(f"{filename} is not in pairs so skiiip")
            else:
                # print(f"No data for April in {filename}")
                no_data_for_nesting_window.append(filename)
    
    # Concatenate all DataFrames in the list into a single DataFrame
    result_df = pd.concat(result_list, ignore_index=True)

    ##### CONTINUE HERE #####
    
    ## SEE WHAT IS GOING ON WITH THE ANALYSIS ## 11-04
    
    # Changed the nhours and diff threshold to be taken by config. Implement analysis for all the variables nexT!!
    
    ## Create two groups one with the extreme events and one with the normal and compare the populations. 
    ### Check if the climate during nesting is affectiing the population more than after the period of nesting.

    df_extremes = result_df[result_df['Above Threshold Values'].apply(lambda x: len(x) > 0)]
    
    df_normal = result_df[result_df['Above Threshold Values'].apply(lambda x: len(x) == 0)]
    
    merged_data_extremes = pd.merge(df_extremes, pairs, left_on='Station', right_on='obs_file', how='inner')
    merged_data_normals = pd.merge(df_normal, pairs, left_on='Station', right_on='obs_file', how='inner')
    
    
