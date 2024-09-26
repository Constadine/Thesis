import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

def heatmaps(data_file_path, name_suffix='', save_dir='/home/kotikos/Education/UoG/Earth Science Master/Thesis/results/heatmaps', save_images=False):
    print(f"Reading data from {data_file_path}...")
    cor_data = pd.read_csv(data_file_path)
    
    # Replace -1 with NaN
    filtered_data = cor_data.replace(-1, np.nan)
    
    # Select only the relevant columns for correlation
    correlation_data = filtered_data[['total_population', 'air_pressure_values', 'air_temperature_values', 
                                      'wind_values', 'sea_temp_values', 'seawater_level_values', 
                                      'wave_height_values']]
    
    print("Calculating correlation matrices...")
    # Calculate the correlation matrices
    pearsons_corr = correlation_data.corr()
    spearman_corr = correlation_data.corr(method='spearman')
    kendall_corr = correlation_data.corr(method='kendall')

    # Plot and optionally save Pearson correlation heatmap
    print("Generating Pearson correlation heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(pearsons_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Pearson Correlation Heatmap')
    if save_images:
        plt.savefig(os.path.join(save_dir, f'pearson_correlation_heatmap{f"_{name_suffix}"}.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # Plot and optionally save Spearman correlation heatmap
    print("Generating Spearman correlation heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(spearman_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Spearman Correlation Heatmap')
    if save_images:
        plt.savefig(os.path.join(save_dir, f'spearman_correlation_heatmap{f"_{name_suffix}"}.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    # Plot and optionally save Kendall Tau correlation heatmap
    print("Generating Kendall Tau correlation heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(kendall_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Kendall Tau Correlation Heatmap')
    if save_images:
        plt.savefig(os.path.join(save_dir, f'kendall_correlation_heatmap{f"_{name_suffix}"}.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    if save_images:
        print(f'Heatmaps were saved and moved to {save_dir}')
    else:
        print('Heatmaps were displayed but not saved.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate and save heatmaps for Pearson, Spearman, and Kendall Tau correlations.',
        epilog='Example usage: python heatmap_script.py --data_path data/final_datasets/data_for_correlation_apr_jun.csv --suffix apr_jun'
    )
    parser.add_argument('--data_path', type=str, required=True, help='Path to the CSV file containing the data.')
    parser.add_argument('--suffix', type=str, default='', help='Optional suffix for the output heatmap filenames.')
    parser.add_argument('--save_dir', type=str, default='/home/kotikos/Education/UoG/Earth Science Master/Thesis/results/heatmaps', help='Directory where the heatmaps will be saved.')
    parser.add_argument('--save_images', action='store_true', help='Include this flag to save the heatmaps. By default, the images will not be saved.')

    args = parser.parse_args()

    print(f"Running the heatmap generation script with the following options:\nData path: {args.data_path}\nSuffix: {args.suffix}\nSave directory: {args.save_dir}\nSave images: {args.save_images}")
    
    heatmaps(data_file_path=args.data_path, name_suffix=args.suffix, save_dir=args.save_dir, save_images=args.save_images)
