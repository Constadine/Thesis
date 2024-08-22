import pandas as pd
import os
import argparse

def filter_april_to_june(df):
    print("Filtering data for April to June...")
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    return df[df['Month'].isin([4, 5, 6])]

def add_lagged_population(data):
    print("Adding lagged population data...")
    data['lagged_population'] = data.groupby(['lat', 'lon'])['total_population'].shift(-1)
    return data.dropna(subset=['lagged_population'])

def main(filter_apr_jun=False, add_lagged=False):
    print("Starting the data processing...")

    climate_data_folder = '/home/kotikos/Education/UoG/Earth Science Master/Thesis/data/SMHI'
    bird_data_path = 'paired_birds_all_climate_data.csv'

    bird_data = pd.read_csv(bird_data_path)
    bird_data['Year'] = pd.to_datetime(bird_data['Date']).dt.year

    bird_data_list = []
    climate_variables = ['air_pressure', 'air_temperature', 'seawater_level', 'sea_temp', 'wave_height', 'wind']

    for variable in climate_variables:
        station_column = f'{variable}_nearest_station'
        if station_column in bird_data.columns:
            print(f"Processing climate variable: {variable}...")
            climate_data_path = os.path.join(climate_data_folder, f"{variable}.csv")
            climate_data = pd.read_csv(climate_data_path)
            
            if filter_apr_jun:
                climate_data = filter_april_to_june(climate_data)

            valid_stations = [station for station in bird_data[station_column].dropna().unique() if station in climate_data.columns]
            if valid_stations:
                relevant_climate_data = climate_data[['Date'] + valid_stations].copy()
                relevant_climate_data.loc[:, 'Year'] = pd.to_datetime(relevant_climate_data['Date']).dt.year
                relevant_climate_data.loc[:, valid_stations] = relevant_climate_data[valid_stations].apply(pd.to_numeric, errors='coerce')
                
                apr_jun_mean = relevant_climate_data.groupby('Year').mean(numeric_only=True).reset_index()
                apr_jun_mean_melted = apr_jun_mean.melt(id_vars='Year', var_name=f'{variable}_station', value_name=f'{variable}_values')

                bird_data_temp = bird_data.merge(apr_jun_mean_melted, left_on=['Year', station_column], right_on=['Year', f'{variable}_station'], how='left')
                bird_data_temp[f'{variable}_values'] = bird_data_temp[f'{variable}_values'].fillna(-1)
                bird_data_temp.drop(columns=[f'{variable}_station'], inplace=True)

                bird_data_list.append(bird_data_temp)

    final_bird_data = bird_data_list[0]
    for data in bird_data_list[1:]:
        final_bird_data = final_bird_data.combine_first(data)

    if add_lagged:
        final_bird_data = add_lagged_population(final_bird_data)

    columns_to_drop = [f'{variable}_nearest_station' for variable in climate_variables] + [f'{variable}_nearest_distance' for variable in climate_variables]
    final_bird_data = final_bird_data.drop(columns=columns_to_drop)

    new_column_order = ['Year', 'lat', 'lon', 'total_population', 'air_pressure_values', 'air_temperature_values', 'wind_values', 'sea_temp_values', 'seawater_level_values', 'wave_height_values']
    if add_lagged:
        new_column_order.append('lagged_population')
    
    final_bird_data = final_bird_data[new_column_order]

    # Set the output file name based on the options selected
    output_file = 'data_for_correlation'
    if filter_apr_jun:
        output_file += '_apr_jun'
    if add_lagged:
        output_file += '_with_lag'
    output_file += '.csv'

    final_bird_data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    print("Data processing completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process bird and climate data for correlation analysis.',
        epilog='Example usage: python script_name.py --apr_jun --lagged'
    )
    parser.add_argument('--apr_jun', action='store_true', help='Filter data for April to June.')
    parser.add_argument('--lagged', action='store_true', help='Add lagged population data.')

    args = parser.parse_args()

    if not (args.apr_jun or args.lagged):
        print("No flags provided. Running with default settings (no April-June filtering, no lagged population).")
    else:
        print(f"Running with the following options: apr_jun={args.apr_jun}, lagged={args.lagged}")

    main(filter_apr_jun=args.apr_jun, add_lagged=args.lagged)