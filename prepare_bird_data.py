import polars as pl

# Load the bird dataset
bird_data = pl.read_csv('data/all_bird_data/all_birds_cleaned.csv')

# Perform the group_by and aggregation
aggregated_data = bird_data.group_by(['eventDate', 'lat', 'lon']).agg(
    pl.col('individualCount').sum().alias('total_population')
)

# Sort the data by latitude, longitude, and date
sorted_data = aggregated_data.sort(['lat', 'lon', 'eventDate'])

# Save the cleaned and sorted data
sorted_data.write_csv('aggregated_bird_data_sorted.csv')

# Display the first few rows of the sorted and aggregated data
print(sorted_data.head())

