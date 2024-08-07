import folium
import polars as pl

def parse_nearest_station(nearest_station):
    # Split by underscore to extract lat and lon
    lat, lon = nearest_station.split('_')
    return float(lat), float(lon)

def visualize_bird_stations(bird_data, map_filename='bird_stations_map.html'):
    # Convert relevant columns to a list of tuples for easier iteration
    bird_locations = bird_data.select(['lat', 'lon', 'Date', 'total_population', 'nearest_station']).to_numpy()

    # Initialize the map centered around the average latitude and longitude
    map_center = [bird_data['lat'].mean(), bird_data['lon'].mean()]
    bird_map = folium.Map(location=map_center, zoom_start=6)

    # Add bird locations to the map
    for row in bird_locations:
        lat, lon, date, population, nearest_station = row
        nearest_station = nearest_station.decode() if isinstance(nearest_station, bytes) else str(nearest_station)
        
        # Parse the nearest_station string to extract lat and lon
        station_lat, station_lon = parse_nearest_station(nearest_station)

        folium.Marker(
            location=[lat, lon],
            popup=f"Bird Location ({lat}, {lon})\nDate: {date}\nPopulation: {population}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(bird_map)

        folium.Marker(
            location=[station_lat, station_lon],
            popup=f"Station: {station_lat}, {station_lon}",
            icon=folium.Icon(color='red', icon='cloud')
        ).add_to(bird_map)

        # Draw a line connecting the bird location to the nearest station
        folium.PolyLine([(lat, lon), (station_lat, station_lon)], color="green", weight=2.5, opacity=1).add_to(bird_map)

    # Save the map to an HTML file
    bird_map.save(map_filename)
    print(f"Map has been saved as {map_filename}")

# Example usage:

# Load your data as a Polars DataFrame
bird_data = pl.read_csv('filtered_bird_data.csv')

# Visualize the bird locations and their nearest stations
visualize_bird_stations(bird_data)
