from find_closest_stations import match_bird_and_observation_data
import pandas as pd

if __name__ == '__main__':
 
    filename = 'data/bird_data/nestlings_cleaned.csv'
    
    nestlings = pd.read_csv(filename, index_col=0)
    nestlings.reset_index(inplace=True, drop=True)
    
    folder_path = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/wave-height'
    
    test_results, discarded_values = match_bird_and_observation_data(nestlings, folder_path)
