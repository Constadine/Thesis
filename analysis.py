import pandas as pd
from find_and_visualize_closest_stations_original import match_bird_and_observation_data
import os

def calculate_max_difference(df, n_values):
    """
    

    Parameters
    ----------
    df : pd.DataFrame
        Climate variable dataframe.
    n_values : TYPE
        The hour interval span.

    Returns
    -------
    None.

    """
    average_values = df.groupby((df.index // n_values) * n_values)['Sea Level'].mean()
    
    difference = average_values.diff()
    
    
    ###
    
    # Need to fix to not calculate averages of different years
    
    ###
    # Find the maximum difference and its corresponding date
    max_difference_index = difference.idxmax()
    max_difference_date = df.loc[max_difference_index, 'Date']
    max_difference_value = difference.loc[max_difference_index]
    
    return max_difference_date, max_difference_value


if __name__ == '__main__':
    filename = 'data/west_bird_data/nestlings_cleaned.csv'
    bird_data = pd.read_csv(filename)
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
            df = pd.read_csv(file_path, skiprows=6, delimiter=';')       
            df.rename(columns={'Datum Tid (UTC)': 'Date', 'Havsvattenstånd': 'Sea Level'}, inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])  

    
            # Filter data for April
            df_april = df[(df['Date'].dt.month == 4) & (df['Date'].dt.year.isin(range(2017, 2023)))].reset_index()
    
            df_april.reset_index(drop=True, inplace=True)
            df_april.drop(columns='index', inplace=True)    

            # Group by year and calculate the mean for each year
            yearly_mean = df_april.groupby(df_april['Date'].dt.year)['Sea Level'].mean()
            yearly_max = df_april.groupby(df_april['Date'].dt.year)['Sea Level'].max()
            yearly_max_difference

            # Convert the result to a DataFrame
            yearly_df = pd.DataFrame({'Year': yearly_mean.index, 'April Mean': yearly_mean.values, 'April Max': yearly_max.values})
    
            # Add the DataFrame to the dictionary with the filename as the key
            result_dict[filename] = yearly_df
    
    # Example of accessing the results
    for file_name, df in result_dict.items():
        print(f"File: {file_name}")
        print(df)