import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

def heatmaps(correlation_path, save_dir='/home/kotikos/Education/UoG/Earth Science Master/Thesis/analysis/heatmaps'):
    cor_data = pd.read_csv(correlation_path)
    
    # Replace -1 with NaN
    filtered_data = cor_data.replace(-1, np.nan)
    
    # Select only the relevant columns for correlation
    correlation_data = filtered_data[['total_population', 'air_pressure_values', 'air_temperature_values', 
                                      'wind_values', 'sea_temp_values', 'seawater_level_values', 
                                      'wave_height_values']]
    
    # Calculate the correlation matrix, automatically ignoring NaN values
    pearsons_corr = correlation_data.corr()
    
    # Calculate Spearman correlation
    spearman_corr = correlation_data.corr(method='spearman')

    # Calculate Kendall Tau correlation
    kendall_corr = correlation_data.corr(method='kendall')


    # Plot the Pearsons
    plt.figure(figsize=(10, 8))
    sns.heatmap(pearsons_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Pearson Correlation Heatmap')
    plt.savefig(os.path.join(save_dir,'pearson_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # Plot Spearman correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(spearman_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Spearman Correlation Heatmap')
    plt.savefig(os.path.join(save_dir,'spearman_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    # Plot Kendall Tau correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(kendall_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Kendall Tau Correlation Heatmap')
    plt.savefig(os.path.join(save_dir,'kendall_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f'Maps were saved and moved to {save_dir}')

if __name__=='__main__':
    
    cor_path = 'data_for_correlation.csv'
    heatmaps(cor_path)