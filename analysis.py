import pandas as pd
from find_and_visualize_closest_stations_original import match_bird_and_observation_data
import os


def calculate_concecutive_differences(df, n_values, climate_variable_column, diffs_threshold=None):
    """
    Parameters
    ----------
    df : pd.DataFrame
        Climate variable dataframe.
    n_values : int
        The hour interval span.
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
        max_difference_date = year_df.loc[max_difference_index, 'Date']
        max_difference_value = diffs.loc[max_difference_index]
        
        
        
        # Append the results for the current year to the list
        max_differences_data.append({
            'Year': year,
            'April Max Diff Date': max_difference_date,
            'April Max Diff Value': max_difference_value
        })

    # Create a DataFrame with results for each year
    max_differences_df = pd.DataFrame(max_differences_data)
    
    return max_differences_df


if __name__ == '__main__':
    no_data_for_nesting_window = []
    
    bird_filename = 'data/all_bird_data/all_birds_cleaned.csv'
    bird_data = pd.read_csv(bird_filename)
    bird_data.drop(columns='Unnamed: 0', inplace=True)

    # Choose variable folder
    CLIMATE_VARIABLE = "seawater-level"
    CLIMATE_FOLDER = "oceanografi"
    folder_path = f'/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/{CLIMATE_FOLDER}/{CLIMATE_VARIABLE}'

    DISTANCE_LIMIT = 20
    # Match observation stations with bird observations
    pairs = match_bird_and_observation_data(bird_data, folder_path, DISTANCE_LIMIT)
    pairs.eventDate = pd.to_datetime(pairs.eventDate)
    
    # Calculate population by grouping observation stations and bird locations
    pairs['year'] = pairs['eventDate'].dt.year
    pairs['month'] = pairs['eventDate'].dt.month
    
    grouped_pairs = pairs.groupby(by=['obs_lat', 'obs_lon', 'bird_lat', 'bird_lon', 'lifeStage', 'year', 'month'])['individualCount'].sum().reset_index()
   
    # Initialize an empty list to store the results
    result_list = []
    
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
    
            # Read the CSV file
            df = pd.read_csv(file_path, skiprows=6, delimiter=';', low_memory=False)       
            df.rename(columns={'Datum Tid (UTC)': 'Date', 'Havsvattenstånd': 'Sea Level'}, inplace=True)
            df = df.iloc[:, :2]

            df['Date'] = pd.to_datetime(df['Date']) 
    
            # Filter data for April
            df_nesting_window = df[(df['Date'].dt.month.isin([4,5,6])) & (df['Date'].dt.year.isin(range(2017, 2023)))]
    
            df_nesting_window.reset_index(drop=True, inplace=True)

            if not df_nesting_window.empty:
                # Group by year and calculate the mean and max for each year
                yearly_mean = df_nesting_window.groupby(df_nesting_window['Date'].dt.year)['Sea Level'].mean()
                yearly_max = df_nesting_window.groupby(df_nesting_window['Date'].dt.year)['Sea Level'].max()
    
                # Specify the number of hours for the average
                n_hours = 12  # You can adjust this based on your requirements
                climate_variable_column = 'Sea Level'
                # Calculate the maximum difference
                max_difference_df = calculate_concecutive_differences(df_nesting_window, n_hours, climate_variable_column)
                
                # Convert the results to a DataFrame
                yearly_df = pd.DataFrame({
                    'Year': yearly_mean.index,
                    'April Mean': yearly_mean.values,
                    'April Max': yearly_max.values,
                    'April Max Diff Date': max_difference_df['April Max Diff Date'].values,
                    'April Max Diff Value': max_difference_df['April Max Diff Value'].values
                })
        
                # Add the DataFrame to the dictionary with the filename as the key
                result_list.append(yearly_df)
            else:
                # print(f"No data for April in {filename}")
                no_data_for_nesting_window.append(filename)
    
    # Concatenate all DataFrames in the list into a single DataFrame
    result_df = pd.concat(result_list, ignore_index=True)

    ##### CONTINUE HERE #####
        
        
        ## Create two groups one with the extreme events and one with the normal and compare the populations. 
        
        ### Check if the climate during nesting is affectiing the population more than after the period of nesting.
        
        # CONTINUE ANALYSIS     

