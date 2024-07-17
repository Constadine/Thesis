

import pandas as pd

# Load climate data
filepath = "/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/oceanografi/wave-height/smhi-opendata_1_11_10_9_7_8_33001_20240205_201133.csv"
climate_data = pd.read_csv(filepath, sep=';') 
# Extract coordinates from the climate data (assuming coordinates are in C2 and D2)
climate_coordinates = climate_data.iloc[1, [2, 3]].tolist()

climate_data = pd.read_csv(filepath, sep=';', skiprows=11) 


# # Rename columns using the names from the 11th row
# climate_data.columns = climate_data.iloc[0]

# # Drop the first 11 rows
# climate_data = climate_data[11:].reset_index(drop=True)

# Load bird data
bird_data = pd.read_csv('/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/all_bird_data/all_nestlings_cleaned.csv')  # Replace with the actual file path

# Merge datasets based on common coordinates
merged_data = pd.merge(bird_data, climate_data, left_on=['lat', 'lon'], right_on=climate_coordinates, how='inner')

# Convert 'eventDate' to datetime format for further processing
merged_data['eventDate'] = pd.to_datetime(merged_data['eventDate'])

# Define the time window around nesting dates (e.g., two weeks)
time_window = pd.DateOffset(days=14)

# Create a function to filter data within the time window
def filter_within_time_window(group):
    start_date = group['eventDate'] - time_window
    end_date = group['eventDate'] + time_window
    return group[(group['Datum Tid (UTC)'] >= start_date) & (group['Datum Tid (UTC)'] <= end_date)]

# Apply the filtering function to each group (bird species)
filtered_data = merged_data.groupby(['lifeStage']).apply(filter_within_time_window).reset_index(drop=True)

# Calculate yearly mean for each bird species
yearly_mean = filtered_data.groupby(['lifeStage', 'Year']).mean()

# Display the result
print(yearly_mean)
