import pandas as pd
import os

def find_observation_coords(file_path):
    """
    Each climate variable has differently structured csv files. This function 
    returns the coordinates of the station dynamically. 
    Parameters
    ----------
    file_path : TYPE
        Filepath of the csv file.

    Returns
    -------
    latitude : float
    longitude : float
    """
    # Initialize a flag to indicate whether the target cell is found
    target_found = False
    
    # Initialize row index
    row_index = 0

    while not target_found:
        # Read a single row from the CSV file
        df = pd.read_csv(file_path, sep=';', skiprows=row_index, nrows=1)
        
        # Check if any column contains the substring "latitud"
        lat_column = [col for col in df.columns if 'latitud' in col.lower()]
        lon_column = [col for col in df.columns if 'longitud' in col.lower()]

        # Check if the target column is present in the current row
        if lat_column and lon_column:
            # Get the first column containing "latitud"
            target_columns = [lat_column[0], lon_column[0]]
            
            # Get the value of the target cell
            target_values = df[target_columns].iloc[0].values
            
            # If the target cell is not NaN or not null, the target is found
            if (pd.notna(target_values[0]) & (pd.notna(target_values[1]))):
                target_found = True
                next_row = pd.read_csv(file_path, sep=';', skiprows=row_index, nrows=1)
                latitude, longitude = next_row[target_columns].iloc[0].values
            else:
                # Increment row index to read the next row
                row_index += 1
        else:
            # Increment row index to read the next row
            row_index += 1
            
    return latitude, longitude



def load_climate_data(file_path, config, oldest_data_to_keep=2015):
    # Read the first few lines of the file to determine the number of rows to skip
    num_skip_rows = 0
    with open(file_path, 'r') as file:
        for line in file:
            num_skip_rows += 1
            if "Datum" in line:
                break
    
    # Reading the file based on the dynamically determined number of rows to skip
    df = pd.read_csv(file_path, skiprows=num_skip_rows - 1, delimiter=config['delimiter'], engine='python')

    # Check if 'Datum' and 'Tid (UTC)' columns exist
    if 'Datum' in df.columns and 'Tid (UTC)' in df.columns:
        # Merge 'Datum' and 'Tid (UTC)' columns into a new 'Date' column
        df['Date'] = pd.to_datetime(df['Datum'] + ' ' + df['Tid (UTC)'], format='%Y-%m-%d %H:%M:%S')
        # Drop the original 'Datum' and 'Tid (UTC)' columns
        df.drop(columns=['Datum', 'Tid (UTC)'], inplace=True)
    elif 'Datum Tid (UTC)' in df.columns:
        # Rename the column 'Datum Tid (UTC)' to 'Date'
        df.rename(columns={'Datum Tid (UTC)': 'Date'}, inplace=True)
    
 # Filter the DataFrame to include only rows where the year in the 'Date' column is greater than or equal to oldest_data_to_keep
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' column is in datetime format
    df = df[df['Date'].dt.year >= oldest_data_to_keep]

    # Make 'Date' first column again
    df = df[['Date'] + [col for col in df.columns if col != 'Date']]

    # Slice and rename columns after filtering
    df = df.iloc[:, :2]
    df.columns = config['column_names']

    # Make Date first column again
    df = df[['Date'] + [col for col in df.columns if col != 'Date']]
    

    return df



def combine_climate_data(folder_path, config, oldest_data_to_keep=2015):
    combined_df = pd.DataFrame()

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full file path for the CSV file
            file_path = os.path.join(folder_path, filename)
            

            # Load the climate data
            climate_data = load_climate_data(file_path, config, oldest_data_to_keep)
            
            coords = find_observation_coords(file_path)
            
            # Rename the climate data column to the station name
            climate_data.columns = ['Date', coords]
            
            # Merge the data into the combined DataFrame
            if combined_df.empty:
                combined_df = climate_data
            else:
                combined_df = pd.merge(combined_df, climate_data, on='Date', how='outer')
    
    # Ensure the Date column is the first column
    combined_df = combined_df[['Date'] + [col for col in combined_df.columns if col != 'Date']]
    
    return combined_df