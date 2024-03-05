import pandas as pd
from find_and_visualize_closest_stations_original import match_bird_and_observation_data
import os


def calculate_max_difference(df, n_values, climate_variable_column):
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
    max_differences_data =[]

    # Group by year
    for year, year_df in df.groupby(df['Date'].dt.year):
        # Calculate differences within each year
        differences = year_df[climate_variable_column].rolling(window=n_values, min_periods=n_values, step=n_values).mean().diff()
        
        # Find the index of the maximum difference
        max_difference_index = differences.idxmax()
        
        # Extract the corresponding date and value
        max_difference_date = year_df.loc[max_difference_index, 'Date']
        max_difference_value = differences.loc[max_difference_index]
        
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
    no_data_for_april = []
    
    bird_filename = 'data/west_bird_data/nestlings_cleaned.csv'
    bird_data = pd.read_csv(bird_filename)
    bird_data.drop(columns='Unnamed: 0', inplace=True)

    # Choose variable folder
    CLIMATE_VARIABLE = "seawater-level"
    folder_path = f'/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/oceanografi/{CLIMATE_VARIABLE}'

    DISTANCE_LIMIT = 20
    # Match observation stations with bird observations
    pairs = match_bird_and_observation_data(bird_data, folder_path, DISTANCE_LIMIT)
    
    
    # Initialize an empty dictionary to store the results
    result_dict = {}
    
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
    
            # Read the CSV file
            df = pd.read_csv(file_path, skiprows=6, delimiter=';', low_memory=False)       
            df.rename(columns={'Datum Tid (UTC)': 'Date', 'Havsvattenstånd': 'Sea Level'}, inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])  

    
            # Filter data for April
            df_april = df[(df['Date'].dt.month == 4) & (df['Date'].dt.year.isin(range(2017, 2023)))]
    
            df_april.reset_index(drop=True, inplace=True)

            if not df_april.empty:
                # Group by year and calculate the mean and max for each year
                yearly_mean = df_april.groupby(df_april['Date'].dt.year)['Sea Level'].mean()
                yearly_max = df_april.groupby(df_april['Date'].dt.year)['Sea Level'].max()
    
                # Specify the number of hours for the average
                n_hours = 12  # You can adjust this based on your requirements
                
                # Calculate the maximum difference
                max_difference_df = calculate_max_difference(df_april, n_hours, 'Sea Level')
                
                # Convert the results to a DataFrame
                yearly_df = pd.DataFrame({
                    'Year': yearly_mean.index,
                    'April Mean': yearly_mean.values,
                    'April Max': yearly_max.values,
                    'April Max Diff Date': max_difference_df['April Max Diff Date'].values,
                    'April Max Diff Value': max_difference_df['April Max Diff Value'].values
                })
        
                # Add the DataFrame to the dictionary with the filename as the key
                result_dict[filename] = yearly_df
            else:
                # print(f"No data for April in {filename}")
                no_data_for_april.append(filename)
    
    # Find big changes in the climate variable and keep the station that produces it to investigate
    max_diff_station = None
    max_diff_value = 0
    
    # Find the station with the biggest April Max Difference value
    for filename, values in result_dict.items():
        current_max_diff_value = values['April Max Diff Value'].max()
        if current_max_diff_value > max_diff_value:
            max_diff_value = current_max_diff_value
            max_diff_station = filename
    
    selected_pair = None
    while not selected_pair and max_diff_station:
        # Check if the station is in any pair's 'obs_file' value in the pairs dictionary
        for pair, info in pairs.items():
            if info['obs_file'] == max_diff_station:
                selected_pair = pair
                break
    
        if not selected_pair:
            # If the selected station is not in pairs, find the next biggest difference station
            max_diff_value = 0
            for filename, values in result_dict.items():
                current_max_diff_value = values['April Max Diff Value'].max()
                if current_max_diff_value > max_diff_value and filename != max_diff_station:
                    max_diff_value = current_max_diff_value
                    max_diff_station = filename
                    break  # Exit the loop after finding the next station

    if selected_pair:
        print(f"Selected pair for analysis: {selected_pair}")
        
        
        selected_bird_coords = pairs[selected_pair]['bird_coords']
        selected_birds_dfs = []
        
        for bird_coord in selected_bird_coords:
            # Filter bird_data for each set of coordinates
            selected_birds_df = bird_data[(bird_data.lat == bird_coord[0]) & (bird_data.lon == bird_coord[1])]
            
            # Append the filtered DataFrame to the list
            selected_birds_dfs.append(selected_birds_df)

# Now, selected_birds_dfs is a list of DataFrames, each corresponding to a set of bird coordinates

        
        temporal_variability = result_dict[max_diff_station]['April Max Diff Value'].std()
        temporal_range = result_dict[max_diff_station]['April Max Diff Value'].max() - result_dict[max_diff_station]['April Max Diff Value'].min()
    
        ##### CONTINUE HERE #####
        
        # CONTINUE ANALYSIS 

    else:
        print("No suitable pair found.")
