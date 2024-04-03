import pandas as pd

def load_and_clean_climate_data(file_path, config):
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

    
    # Make Date first column again
    df = df[['Date'] + [col for col in df.columns if col != 'Date']]
    df = df.iloc[:, :2]
    df.columns = config['column_names']
    date_column = config['date_column']
    df[date_column] = pd.to_datetime(df[date_column]) 
    
    return df

def find_observation_coords(file_path):
    
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