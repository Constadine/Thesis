import polars as pl
import time
# Measure the execution time
start_time = time.time()
'''
OPTIONS = 'air_pressure' | 'air_temperature' | 'seawater_level' | 'sea_temp' | 'wave_height' | 'wind'
'''

OPTIONS = ['air_pressure', 'air_temperature', 'seawater_level', 'sea_temp', 'wave_height', 'wind']

# Initialize a dictionary to store the correlation results for each option
all_correlation_results = {}

for option in OPTIONS:
    
    bird_path = f'data/paired_datasets/paired_birds_with_{option}.csv'
    climate_path = f'data/SMHI/{option}.csv'

    # Load the datasets
    bird_data = pl.read_csv(bird_path)
    climate_data = pl.read_csv(climate_path)
    
    # Ensure Date columns are correctly converted to datetime
    bird_data = bird_data.with_columns(
        pl.col('Date').str.strptime(pl.Datetime, format='%Y-%m-%d').alias('Date')
    )
    
    climate_data = climate_data.with_columns(
        pl.col('Date').str.strptime(pl.Datetime, format='%Y-%m-%d %H:%M:%S').alias('Date')
    )
    
    # Choose an appropriate strategy:
    # 1. Forward Fill
    # seawater_data = seawater_data.fill_null(strategy="forward")
    
    # 2. Interpolation (if necessary, using Pandas)
    climate_data_pandas = climate_data.to_pandas()
    climate_data_interpolated = climate_data_pandas.interpolate(method='linear')
    climate_data = pl.from_pandas(climate_data_interpolated)
    
    # Extract the year from the Date column
    bird_data = bird_data.with_columns(pl.col('Date').dt.year().alias('Year'))
    climate_data = climate_data.with_columns(pl.col('Date').dt.year().alias('Year'))
    
    # Aggregate seawater level data by year and station (taking the mean)
    climate_yearly = climate_data.group_by('Year').mean()
    

    
    # Initialize an empty list to store correlation results
    correlation_results = []
    
    # Iterate over each unique bird location
    unique_locations = bird_data.select(['lat', 'lon']).unique()
    
    for location in unique_locations.iter_rows(named=True):
        # Filter the bird data for the specific location
        filtered_bird_data = bird_data.filter(
            (pl.col('lat') == location['lat']) & (pl.col('lon') == location['lon'])
        )
        
        # Get the nearest station column
        station_col = filtered_bird_data['nearest_station'][0]
        
        if station_col in climate_yearly.columns:
            # Merge bird data with corresponding seawater level data
            merged_data = filtered_bird_data.join(
                climate_yearly.select(['Year', station_col]),
                left_on='Year',
                right_on='Year',
                how='inner'
            )
            merged_data = merged_data.rename({station_col: option})
            
            # Calculate the correlation
            correlation = merged_data.select(pl.corr('total_population', option)).to_numpy()[0, 0]
            
            # Store the result
            correlation_results.append({
                'lat': location['lat'],
                'lon': location['lon'],
                'correlation': correlation
            })
    
    # Convert the results to a DataFrame and store in the dictionary
    correlation_results_df = pl.DataFrame(correlation_results)
    # Remove NaN values from the correlation results
    correlation_results_df = correlation_results_df.filter(~pl.col('correlation').is_nan())

    all_correlation_results[option] = correlation_results_df
    
# Display the summary of the results for each option
for option, df in all_correlation_results.items():
    print(f"Summary of correlation results for {option}:")
    description = df['correlation'].describe()
    print(description)
    print("\n")

end_time = time.time()
print(f"Script executed in {end_time - start_time} seconds")
