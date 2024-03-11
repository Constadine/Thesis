import matplotlib.pyplot as plt
import pandas as pd



bird_filename = 'data/all_bird_data/all_birds_cleaned.csv'
bird_data = pd.read_csv(bird_filename)
bird_data.drop(columns='Unnamed: 0', inplace=True)
bird_data['eventDate'] = pd.to_datetime(bird_data['eventDate'])  


# Filter bird_data for Nestling lifeStage
nestling_data = bird_data[bird_data['lifeStage'] == 'Nestling']

# Create subplots with two rows (one for each month)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Extract day counts for each month
day_counts_month5 = nestling_data[nestling_data['eventDate'].dt.month == 5]['eventDate'].dt.day.value_counts().sort_index()
day_counts_month6 = nestling_data[nestling_data['eventDate'].dt.month == 6]['eventDate'].dt.day.value_counts().sort_index()

# Plot scatter plots for each month in the subplots
ax1.scatter(day_counts_month5.index, day_counts_month5.values, color='blue', marker='o', label='May')
ax2.scatter(day_counts_month6.index, day_counts_month6.values, color='red', marker='o', label='June')

# Set titles and labels for each subplot
ax1.set_title('Nestling Events - May')
ax1.set_xlabel('Day of the Month')
ax1.set_ylabel('Number of Nestling Events')

ax2.set_title('Nestling Events - June')
ax2.set_xlabel('Day of the Month')
ax2.set_ylabel('Number of Nestling Events')

# Add legends to each subplot
ax1.legend()
ax2.legend()

# Show both x and y-axis grids
ax1.grid(True)
ax2.grid(True)


# Adjust layout for better spacing
plt.tight_layout()

# Show the plots
plt.show()