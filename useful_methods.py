import os
import shutil
import pandas as pd




def load_bird_data(file_path):
    bird_data = pd.read_csv(file_path)
    bird_data.drop(columns='Unnamed: 0', inplace=True)

    return bird_data
  
def discard_files_with_old_data(folder_path, config, oldest_data_to_keep=2015):    
    # Directory to move discarded files
    discarded_dir = os.path.join(folder_path, 'discarded_old_stations')

    # Create the directory if it doesn't exist
    if not os.path.exists(discarded_dir):
        os.makedirs(discarded_dir)

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = load_climate_data_file(file_path, config, 1800)
            date_column = config['date_column']
            max_year = df[date_column].dt.year.max()
            if max_year < oldest_data_to_keep:
                file_name = os.path.basename(file_path)
                new_path = os.path.join(discarded_dir, file_name)
                print(f'Moving {file_name} to {discarded_dir} since it contains data until {max_year}.')
                shutil.move(file_path, new_path)
            else:
                print(f'Max year {df[date_column].dt.year.max()} - OK')

if __name__ == '__main__':
    
    from climate_configs import configs
    
    data_folder = 'data/SMHI/'
    for main_folder in os.listdir(data_folder):
        for folder in os.listdir(data_folder+main_folder):
            variable_folder = os.path.join(data_folder+main_folder+'/'+folder)
            print(variable_folder)
            config = configs[folder]
        
            discard_files_with_old_data(variable_folder, config)
        