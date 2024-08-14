import polars as pl
import numpy as np

def calculate_yearly_average(climate_data, station_col):
    # Convert Date to Year and ensure it's the same dtype across dataframes
    
    climate_data = climate_data.with_columns(
        pl.col('Date').str.strptime(pl.Date, '%Y-%m-%d %H:%M:%S')
    )
    climate_data = climate_data.with_columns(
        pl.col('Date').dt.year().cast(pl.Int64).alias('Year')
    )

    # Calculate yearly average for the specified station column
    yearly_avg_df = climate_data.group_by('Year').agg(
        pl.col(station_col).mean().alias(f'{station_col}_yearly_avg')
    )

    return yearly_avg_df

def integrate_climate_data(bird_data, climate_variable, climate_data):
    # Ensure date format is correct and extract year
    bird_data = bird_data.with_columns(
        pl.col('Date').str.strptime(pl.Date, '%Y-%m-%d')
    ).with_columns(
        pl.col('Date').dt.year().cast(pl.Int64).alias('Year')
    )
    
    # Use the nearest_station column for the current climate variable
    nearest_station_col = f'{climate_variable}_nearest_station'
    
    # Initialize an empty list to collect results
    results = []

    # Iterate through each row in the bird data
    for row in bird_data.iter_rows(named=True):
        station_col = row[nearest_station_col]
        row_df = pl.DataFrame(row)

        if station_col in climate_data.columns:
            yearly_avg_df = calculate_yearly_average(climate_data, station_col)
            # Cast the Year column to Int64 to match data types
            yearly_avg_df = yearly_avg_df.with_columns(pl.col('Year').cast(pl.Int64))
            # Join the yearly average data with the bird data
            row_df = row_df.join(yearly_avg_df, on='Year', how='left')
        else:
            # Add a column with Null values to maintain structure
            row_df = row_df.with_columns(pl.Series(name=f'{station_col}_yearly_avg', values=[None], dtype=pl.Float64))
        
        # Ensure consistent data types across all rows
        row_df = row_df.with_columns([pl.col(nearest_station_col).cast(pl.Utf8, strict=False)])
        results.append(row_df)
    
    # Concatenate all results into a single DataFrame
    bird_data = pl.concat(results, how='vertical')

    return bird_data

# Example usage
bird_data = pl.read_csv("paired_birds_all_climate_data.csv")
climate_variables = ['air_pressure', 'air_temperature', 'seawater_level', 'sea_temp', 'wave_height', 'wind']

# Integrate each climate variable into the bird data
for climate_variable in climate_variables:
    climate_data = pl.read_csv(f"data/SMHI/{climate_variable}.csv")
    
    bird_data = integrate_climate_data(bird_data, climate_variable, climate_data)

# Save the final integrated data
bird_data.write_csv("final_paired_birds_all_climate_data.csv")
