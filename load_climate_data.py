import pandas as pd
import os
from climate_configs import configs
# def find_observation_coords(file_path):
#     """
#     Each climate variable has differently structured csv files. This function 
#     returns the coordinates of the station dynamically. 
#     Parameters
#     ----------
#     file_path : TYPE
#         Filepath of the csv file.

#     Returns
#     -------
#     latitude : float
#     longitude : float
#     """
#     # Initialize a flag to indicate whether the target cell is found
#     target_found = False
    
#     # Initialize row index
#     row_index = 0

#     while not target_found:
#         # Read a single row from the CSV file
#         df = pd.read_csv(file_path, sep=';', skiprows=row_index, nrows=1)
        
#         # Check if any column contains the substring "latitud"
#         lat_column = [col for col in df.columns if 'latitud' in col.lower()]
#         lon_column = [col for col in df.columns if 'longitud' in col.lower()]

#         # Check if the target column is present in the current row
#         if lat_column and lon_column:
#             # Get the first column containing "latitud"
#             target_columns = [lat_column[0], lon_column[0]]
            
#             # Get the value of the target cell
#             target_values = df[target_columns].iloc[0].values
            
#             # If the target cell is not NaN or not null, the target is found
#             if (pd.notna(target_values[0]) & (pd.notna(target_values[1]))):
#                 target_found = True
#                 next_row = pd.read_csv(file_path, sep=';', skiprows=row_index, nrows=1)
#                 latitude, longitude = next_row[target_columns].iloc[0].values
#             else:
#                 # Increment row index to read the next row
#                 row_index += 1
#         else:
#             # Increment row index to read the next row
#             row_index += 1
            
#     return latitude, longitude


# def load_climate_data_file(file_path, config, oldest_data_to_keep=2015):
#     # Read the first few lines of the file to determine the number of rows to skip
#     num_skip_rows = 0
#     with open(file_path, 'r') as file:
#         for line in file:
#             num_skip_rows += 1
#             if "Datum" in line:
#                 break
    
#     # Reading the file based on the dynamically determined number of rows to skip
#     df = pd.read_csv(file_path, skiprows=num_skip_rows - 1, delimiter=config['delimiter'], engine='python')

#     # Check if 'Datum' and 'Tid (UTC)' columns exist
#     if 'Datum' in df.columns and 'Tid (UTC)' in df.columns:
#         # Merge 'Datum' and 'Tid (UTC)' columns into a new 'Date' column
#         df['Date'] = pd.to_datetime(df['Datum'] + ' ' + df['Tid (UTC)'], format='%Y-%m-%d %H:%M:%S')
#         # Drop the original 'Datum' and 'Tid (UTC)' columns
#         df.drop(columns=['Datum', 'Tid (UTC)'], inplace=True)
#     elif 'Datum Tid (UTC)' in df.columns:
#         # Rename the column 'Datum Tid (UTC)' to 'Date'
#         df.rename(columns={'Datum Tid (UTC)': 'Date'}, inplace=True)
    
#     # Filter the DataFrame to include only rows where the year in the 'Date' column is greater than or equal to oldest_data_to_keep
#     df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' column is in datetime format
#     df = df[df['Date'].dt.year >= oldest_data_to_keep]

#     # Make 'Date' first column again
#     df = df[['Date'] + [col for col in df.columns if col != 'Date']]

#     # Slice and rename columns after filtering
#     df = df.iloc[:, :2]
#     df.columns = config['column_names']

#     # Make Date first column again
#     df = df[['Date'] + [col for col in df.columns if col != 'Date']]
    
#     return df

# def combine_climate_data(folder_path, config, oldest_data_to_keep=2015):
#     combined_df = pd.DataFrame()

#     # Iterate over all files in the folder
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".csv"):
#             # Construct the full file path for the CSV file
#             file_path = os.path.join(folder_path, filename)
            
#             # Load the climate data
#             climate_data = load_climate_data_file(file_path, config, oldest_data_to_keep)
            
#             coords = find_observation_coords(file_path)
            
#             # Rename the climate data column to the station name
#             climate_data.columns = ['Date', coords]
            
#             # Merge the data into the combined DataFrame
#             if combined_df.empty:
#                 combined_df = climate_data
#             else:
#                 combined_df = pd.merge(combined_df, climate_data, on='Date', how='outer')
    
#     # Ensure the Date column is the first column
#     combined_df = combined_df[['Date'] + [col for col in combined_df.columns if col != 'Date']]
    
#     return combined_df


def extract_station_info(lines):
    """
    Extracts the station name and coordinates from the lines of the CSV file.
    """
    latitude = None
    longitude = None

    for idx, line in enumerate(lines):
        # Split the line by semicolons
        columns = line.split(";")
        
        # Check if "Latitud" is in the current line
        if any("latitud" in col.lower() for col in columns):
            lat_index = columns.index(next(col for col in columns if "latitud" in col.lower()))
            latitude = lines[idx + 1].split(";")[lat_index].strip()
        
        # Check if "Longitud" is in the current line
        if any("longitud" in col.lower() for col in columns):
            lon_index = columns.index(next(col for col in columns if "longitud" in col.lower()))
            longitude = lines[idx + 1].split(";")[lon_index].strip()
    
        if latitude and longitude:
            return latitude, longitude

def load_climate_data(df, config, oldest_data_to_keep=2015):
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

    return df

def combine_climate_data(folder_path, config, oldest_data_to_keep=2015):
    combined_df = pd.DataFrame()
    file_coords = {}  # Dictionary to store file names and their coordinates
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full file path for the CSV file
            file_path = os.path.join(folder_path, filename)

            # Read the file line-by-line to find the number of rows to skip and extract station info
            lines = []
            with open(file_path, 'r') as file:
                for i in range(15):
                    line = file.readline()
                    if not line:
                        break  # Stop if we reach the end of the file before 15 lines
                    lines.append(line)
            
            latitude, longitude = extract_station_info(lines)
            file_coords[filename] = (latitude, longitude)  # Store filename and its coordinates
            
            coords = f"{latitude}_{longitude}"
            print(coords)
            num_skip_rows = 0
            for line in lines:
                num_skip_rows += 1
                if "Datum" in line:
                    break
            

            # Read the DataFrame based on the number of rows to skip
            df = pd.read_csv(file_path, skiprows=num_skip_rows - 1, delimiter=config['delimiter'], engine='python')
            
            # Load and process the climate data
            climate_data = load_climate_data(df, config, oldest_data_to_keep)
            
            # Rename the climate data column to the station coordinates
            climate_data.columns = ['Date', coords]

            # Ensure unique column names to avoid merging conflicts
            combined_df_columns = set(combined_df.columns)
            climate_data_columns = set(climate_data.columns)

            duplicate_columns = combined_df_columns.intersection(climate_data_columns)
            for col in duplicate_columns:
                if col != 'Date':
                    new_col_name = col + f"_{filename.split('.')[0]}"
                    climate_data.rename(columns={col: new_col_name}, inplace=True)

            # Merge the data into the combined DataFrame
            if combined_df.empty:
                combined_df = climate_data
            else:
                combined_df = pd.merge(combined_df, climate_data, on='Date', how='outer')

    # Ensure the Date column is the first column
    combined_df = combined_df[['Date'] + [col for col in combined_df.columns if col != 'Date']]

    return combined_df, file_coords

if __name__ == '__main__':
    root_folder='/home/kotikos/Education/UoG/Earth Science Master/Thesis/data/SMHI'
    coords_dict = {}  # Dictionary to store filenames and their corresponding coordinates
    for category_folder in os.listdir(root_folder):
        category_path = os.path.join(root_folder, category_folder)

        # Ensure we are only processing directories
        if os.path.isdir(category_path):
            # Iterate over the variable folders within each category (e.g., air_pressure, sea_temp, etc.)
            for variable_folder in os.listdir(category_path):
                variable_path = os.path.join(category_path, variable_folder)

                if os.path.isdir(variable_path):
                    print(f"Processing: {variable_path}")
                    config = configs.get(variable_folder, {})  # Fetch the config for the variable
                    combined_climate_data, file_coords = combine_climate_data(variable_path, config)
                    # Save the combined data to a CSV file named after the variable
                    output_filename = f'{variable_folder}_combined_data.csv'
                    coords_dict_filename = f'{variable_folder}_coords.csv'
                    output_filepath = os.path.join(root_folder, output_filename)
                    combined_climate_data.to_csv(output_filepath, index=False)
                    
                    pd.DataFrame.from_dict(file_coords, orient='index', columns=['Latitude', 'Longitude']).to_csv(coords_dict_filename)
                    print(f"Saved: {output_filepath} and {coords_dict_filename}")
    
