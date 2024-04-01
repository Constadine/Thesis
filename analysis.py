import pandas as pd
from find_and_visualize_closest_stations import match_bird_and_observation_data
import os
from climate_configs import configs
from useful_methods import load_and_clean_climate_data

def calculate_concecutive_differences(df, n_values, climate_variable_column, diffs_threshold=None):
    """
    Parameters
    ----------
    df : pd.DataFrame
        Climate variable dataframe.
    n_values : int
        The hour interval span. The window represented is double this value. For example if I select 
        12 hour n_values that means the extreme could have happened in the span of the last 24 hours.
    climate_variable_column : str
        Column name for Sea Level values.

    Returns
    -------
    pd.DataFrame
        DataFrame with max difference for each year.
    """
    max_differences_data = []

    # Group by year
    for year, year_df in df.groupby(df['Date'].dt.year):
        # Calculate differences within each year
        diffs = year_df[climate_variable_column].rolling(window=n_values, min_periods=n_values, step=n_values).mean().diff()
        
        # Find the index of the maximum difference
        diffs_above_threshold = diffs[diffs > diffs_threshold]
        diffs_above_threshold_indexes = diffs_above_threshold.index
        max_difference_index = diffs.idxmax()
        
        ##### CONTINUE HERE. DETECT ALL THE OCCURENCES OF EXTREMES
        
        # Extract the corresponding date and value
        above_threshold_dates = list(year_df.loc[diffs_above_threshold_indexes, 'Date'].values)
        above_threshold_values = list(diffs_above_threshold.values)

        max_difference_date = year_df.loc[max_difference_index, 'Date']
        max_difference_value = diffs.loc[max_difference_index]
        
        
        # Extract the corresponding dates and values

        # Append the results for the current year to the list
        max_differences_data.append({
            'Year': year,
            'Above Threshold Dates': above_threshold_dates,
            'Above Threshold Values': above_threshold_values,
            'All Time Max Diff Date': max_difference_date,
            'All Time Max Diff Value': max_difference_value
        })

    # Create a DataFrame with results for each year
    max_differences_df = pd.DataFrame(max_differences_data)
    
    return max_differences_df



if __name__ == '__main__':
    no_data_for_nesting_window = []
    
    # Load bird data
    bird_filename = 'data/all_bird_data/all_birds_cleaned.csv'
    bird_data = pd.read_csv(bird_filename)
    bird_data.drop(columns='Unnamed: 0', inplace=True)

    # Choose folder to load climate data
    # CLIMATE_FOLDER_OPTIONS = "meteorologi", "oceanografi"
    CLIMATE_FOLDER= "meteorologi"
    
    # CLIMATE_VARIABLE_OPTIONS = "wind", "air_temperature", "air_pressure", "sea_temp", "seawater_level", "wave_height"
    CLIMATE_VARIABLE = "air_temperature"
    folder_path = os.path.join('data', 'SMHI', CLIMATE_FOLDER, CLIMATE_VARIABLE)
    
    config = configs[CLIMATE_VARIABLE]
    
    # Match observation stations with bird observations
    DISTANCE_LIMIT = 10 # Depending on climate variable chosen, distance limit should be adjusted. Measured in km.
    
    # Link bird observation locations with closest climate observation station
    pairs = match_bird_and_observation_data(bird_data, folder_path, DISTANCE_LIMIT)
    pairs.eventDate = pd.to_datetime(pairs.eventDate)
    
    # Group the pairs as very records are from the same area. So basically add all the populations of specific bird locations
    pairs['year'] = pairs['eventDate'].dt.year
    pairs['month'] = pairs['eventDate'].dt.month
    grouped_pairs = pairs.groupby(by=['obs_lat', 'obs_lon', 'bird_lat', 'bird_lon', 'lifeStage', 'year', 'month'])['individualCount'].sum().reset_index()

    # Initialize an empty list to store the results
    result_list = []
  
    #######
    # I NEED TO KEEP WHICH STATION IS GIVING THE EXTREMES SO I CAN LATER CHECK WITH PAIRS
    
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            if filename in pairs['obs_file'].values:
    
                file_path = os.path.join(folder_path, filename)
           
                df = load_and_clean_climate_data(file_path, config)
                climate_variable_column = config['value_column']
                date_column = config['date_column']
    
                # Filter data for period of interest
                df_nesting_window = df[(df[date_column].dt.month.isin([4,5,6])) & (df[date_column].dt.year.isin(range(2017, 2023)))]
        
                df_nesting_window.reset_index(drop=True, inplace=True)

                if not df_nesting_window.empty:

                    # Group by year and calculate the mean and max for each year
                    yearly_mean = df_nesting_window.groupby(df_nesting_window[date_column].dt.year)[climate_variable_column].mean()
                    yearly_max = df_nesting_window.groupby(df_nesting_window[date_column].dt.year)[climate_variable_column].max()
        
                    # Specify the number of hours for the average
                    n_hours = 12  # You can adjust this based on your requirements
                    
                    # Calculate the maximum difference
                    max_difference_df = calculate_concecutive_differences(df_nesting_window, n_hours, climate_variable_column, diffs_threshold=10)
                    
                    # Convert the results to a DataFrame
                    yearly_df = pd.DataFrame({
                        'Year': yearly_mean.index,
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
        
        ## Create two groups one with the extreme events and one with the normal and compare the populations. 
        
        ### Check if the climate during nesting is affectiing the population more than after the period of nesting.
        
        # CONTINUE ANALYSIS