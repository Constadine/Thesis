import pandas as pd

def calculate_concecutive_differences(df, n_values, climate_variable_column, diffs_threshold=None):
    """
    Parameters
    ----------
    df : pd.DataFrame
        Climate variable dataframe.
    n_values : int
        The hour interval span. The window represented is double this value. For example if I select 
        12 hour n_values that means the extreme could have happened in the span of the last 24 hours.
    climate_variable_column : str
        Column name for Sea Level values.

    Returns
    -------
    pd.DataFrame
        DataFrame with max difference for each year.
    """
    differences_above_threshold = []

    # Group by year
    for year, year_df in df.groupby(df['Date'].dt.year):
        # Calculate differences within each year
        diffs = year_df[climate_variable_column].rolling(window=n_values, min_periods=n_values, step=n_values).mean().diff()
        
        # Find the index of the maximum difference
        diffs_above_threshold = diffs[diffs > diffs_threshold]
        diffs_above_threshold_indexes = diffs_above_threshold.index
        max_difference_index = diffs.idxmax()
        
        ##### CONTINUE HERE. DETECT ALL THE OCCURENCES OF EXTREMES
        
        # Extract the corresponding date and value
        above_threshold_dates = list(year_df.loc[diffs_above_threshold_indexes, 'Date'].values)
        above_threshold_values = list(diffs_above_threshold.values)

        max_difference_date = year_df.loc[max_difference_index, 'Date']
        max_difference_value = diffs.loc[max_difference_index]
        
        # Extract the corresponding dates and values

        # Append the results for the current year to the list
        differences_above_threshold.append({
            'Year': year,
            'Above Threshold Dates': above_threshold_dates,
            'Above Threshold Values': above_threshold_values,
            'All Time Max Diff Date': max_difference_date,
            'All Time Max Diff Value': max_difference_value
        })

    # Create a DataFrame with results for each year
    differences_above_threshold = pd.DataFrame(differences_above_threshold)
    
    return differences_above_threshold


