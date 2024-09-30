import folium
import polars as pl
import os

def parse_nearest_station(nearest_station):
    # Split by underscore to extract lat and lon
    lat, lon = nearest_station.split('_')
    return float(lat), float(lon)

def visualize_bird_stations(bird_data, map_filename='bird_stations_map.html'):
    # Initialize the map centered around the average latitude and longitude
    map_center = [bird_data['lat'].mean(), bird_data['lon'].mean()]
    bird_map = folium.Map(location=map_center, zoom_start=6)

    # Define a color map for different variables
    color_map = {
        'air_pressure': 'red',
        'air_temperature': 'orange',
        'seawater_level': 'blue',
        'sea_temp': 'green',
        'wave_height': 'purple',
        'wind': 'pink'
    }

    # Iterate over all rows in the DataFrame
    for row in bird_data.iter_rows(named=True):
        lat = row['lat']
        lon = row['lon']
        date = row['Date']
        population = row['total_population']

        # Add bird location marker
        folium.Marker(
            location=[lat, lon],
            popup=f"Bird Location ({lat}, {lon})\nDate: {date}\nPopulation: {population}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(bird_map)

        # Iterate over all climate variables to add corresponding station markers
        for variable, color in color_map.items():
            station_key = f'{variable}_nearest_station'
            distance_key = f'{variable}_nearest_distance'
            if station_key in row and row[station_key] is not None:
                station_lat, station_lon = parse_nearest_station(row[station_key])
                distance = float(row[distance_key])  # Convert distance to float

                # Add station marker
                folium.Marker(
                    location=[station_lat, station_lon],
                    popup=f"Station ({variable}): {station_lat}, {station_lon}\nDistance: {distance:.2f} km",
                    icon=folium.Icon(color=color, icon='cloud')
                ).add_to(bird_map)

                # Draw a line connecting the bird location to the nearest station
                folium.PolyLine([(lat, lon), (station_lat, station_lon)], color=color, weight=2.5, opacity=1).add_to(bird_map)

    # Save the map to an HTML file
    bird_map.save(map_filename)
    print(f"Map has been saved as {map_filename}")

if __name__ == '__main__':
    rootfile = '/home/kotikos/Education/UoG/Earth Science Master/Thesis/'
    filename = 'paired_birds_all_climate_data.csv'  # Assuming this is the combined dataset filename
    file_path = os.path.join(rootfile, filename)

    # Load your data as a Polars DataFrame
    bird_data = pl.read_csv(file_path)
    
    # Visualize the bird locations and their nearest stations for all variables
    visualize_bird_stations(bird_data, 'paired_bird_all_stations_map.html')
