import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import argparse
import os
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

def load_and_prepare_data(data_file_path, target_column='total_population', replace_negative_one=True, impute_method='mean'):
    """
    Load the data, handle missing values, and prepare predictors and target variables.

    Parameters:
    - data_file_path (str): Path to the CSV file containing the data.
    - target_column (str): Name of the target variable column.
    - replace_negative_one (bool): Whether to replace -1 with NaN.
    - impute_method (str): Method to impute missing values ('mean', 'median', etc.).

    Returns:
    - X (pd.DataFrame): Predictor variables.
    - y (pd.Series): Target variable.
    """
    try:
        data = pd.read_csv(data_file_path)
    except FileNotFoundError:
        print(f"Error: The file {data_file_path} does not exist.")
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"Error parsing {data_file_path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error loading {data_file_path}: {e}")
        sys.exit(1)
    
    # Replace -1 with NaN if specified
    if replace_negative_one:
        data.replace(-1, np.nan, inplace=True)
    
    # Check if target column exists
    if target_column not in data.columns:
        print(f"Error: Target column '{target_column}' not found in data.")
        sys.exit(1)
    
    # Select predictor columns
    predictor_columns = [
        'air_pressure_values', 'air_temperature_values', 
        'wind_values', 'sea_temp_values', 'seawater_level_values', 
        'wave_height_values'
    ]
    
    # Check if all predictor columns exist
    missing_predictors = [col for col in predictor_columns if col not in data.columns]
    if missing_predictors:
        print(f"Error: Missing predictor columns: {missing_predictors}")
        sys.exit(1)
    
    X = data[predictor_columns]
    y = data[target_column]
    
    # Impute missing values
    if impute_method == 'mean':
        X.fillna(X.mean(), inplace=True)
    elif impute_method == 'median':
        X.fillna(X.median(), inplace=True)
    else:
        print(f"Error: Unsupported impute_method '{impute_method}'. Use 'mean' or 'median'.")
        sys.exit(1)
    
    # Drop any remaining NaN in target
    y = y.dropna()
    X = X.loc[y.index]
    
    return X, y

def check_multicollinearity(X):
    """
    Check for multicollinearity using Variance Inflation Factor (VIF).

    Parameters:
    - X (pd.DataFrame): Predictor variables.

    Returns:
    - pd.DataFrame: DataFrame containing VIF for each predictor.
    """
    vif_data = pd.DataFrame()
    vif_data["Feature"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    return vif_data

def plot_predictions(y_test, y_pred, save_path=None):
    """
    Plot actual vs predicted values.

    Parameters:
    - y_test (pd.Series): Actual target values.
    - y_pred (np.ndarray): Predicted target values.
    - save_path (str): Path to save the plot. If None, does not save.
    """
    plt.figure(figsize=(8,6))
    sns.scatterplot(x=y_test, y=y_pred)
    plt.xlabel('Actual Population')
    plt.ylabel('Predicted Population')
    plt.title('Actual vs Predicted Bird Population')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # Diagonal line
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Prediction plot saved to {save_path}")
    plt.show()

def plot_residuals(y_test, y_pred, save_path=None):
    """
    Plot residuals vs predicted values.

    Parameters:
    - y_test (pd.Series): Actual target values.
    - y_pred (np.ndarray): Predicted target values.
    - save_path (str): Path to save the plot. If None, does not save.
    """
    residuals = y_test - y_pred
    plt.figure(figsize=(8,6))
    sns.scatterplot(x=y_pred, y=residuals)
    plt.xlabel('Predicted Population')
    plt.ylabel('Residuals')
    plt.title('Residuals vs Predicted Values')
    plt.axhline(0, color='r', linestyle='--')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Residuals plot saved to {save_path}")
    plt.show()

def perform_linear_regression(X_train, y_train, X_test, y_test, save_dir='results/linear_analysis', save_plots=False):
    """
    Perform linear regression, evaluate the model, and plot results.

    Parameters:
    - X_train (pd.DataFrame): Training predictor variables.
    - y_train (pd.Series): Training target variable.
    - X_test (pd.DataFrame): Testing predictor variables.
    - y_test (pd.Series): Testing target variable.
    - save_dir (str): Directory to save plots.
    - save_plots (bool): If True, save the plots.
    
    Returns:
    - model (LinearRegression): Trained linear regression model.
    - metrics (dict): Dictionary containing MSE and R-squared.
    - coefficients (pd.DataFrame): DataFrame of model coefficients.
    """
    # Create the linear regression model
    model = LinearRegression()
    
    # Fit the model on the training data
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    
    # Print the coefficients
    coefficients = pd.DataFrame({
        'Feature': X_train.columns,
        'Coefficient': model.coef_
    })
    print("Model Coefficients:")
    print(coefficients)
    
    # Create save directory if needed
    if save_plots and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    
    # Plot Actual vs Predicted
    if save_plots:
        plot_predictions(y_test, y_pred, save_path=os.path.join(save_dir, 'actual_vs_predicted.png'))
        plot_residuals(y_test, y_pred, save_path=os.path.join(save_dir, 'residuals.png'))
    else:
        plot_predictions(y_test, y_pred)
        plot_residuals(y_test, y_pred)
    
    metrics = {'Mean Squared Error': mse, 'R-squared': r2}
    
    return model, metrics, coefficients

def perform_statsmodels_regression(X_train, y_train, save_dir='results/linear_analysis', save_summary=False):
    """
    Perform linear regression using statsmodels and print the summary.

    Parameters:
    - X_train (pd.DataFrame): Training predictor variables.
    - y_train (pd.Series): Training target variable.
    - save_dir (str): Directory to save the summary.
    - save_summary (bool): If True, save the summary to a text file.
    
    Returns:
    - model_sm (statsmodels.regression.linear_model.RegressionResultsWrapper): Fitted model.
    """
    # Add a constant to the model (for the intercept)
    X_train_sm = sm.add_constant(X_train)
    
    # Fit the model using statsmodels
    model_sm = sm.OLS(y_train, X_train_sm).fit()
    
    # Print the model summary
    print(model_sm.summary())
    
    # Save the summary if required
    if save_summary:
        os.makedirs(save_dir, exist_ok=True)
        summary_path = os.path.join(save_dir, 'statsmodels_summary.txt')
        with open(summary_path, 'w') as f:
            f.write(model_sm.summary().as_text())
        print(f"Statsmodels summary saved to {summary_path}")
    
    return model_sm

def main(data_file_path, target_column='total_population', replace_negative_one=True, impute_method='mean', test_size=0.2, random_state=42, save_dir='results/linear_analysis', save_plots=False):
    """
    Main function to perform linear regression analysis.

    Parameters:
    - data_file_path (str): Path to the CSV file containing the data.
    - target_column (str): Name of the target variable column.
    - replace_negative_one (bool): Whether to replace -1 with NaN.
    - impute_method (str): Method to impute missing values ('mean', 'median', etc.).
    - test_size (float): Proportion of the dataset to include in the test split.
    - random_state (int): Random seed for reproducibility.
    - save_dir (str): Directory to save results and plots.
    - save_plots (bool): If True, save the plots.
    """
    # Load and prepare data
    X, y = load_and_prepare_data(data_file_path, target_column, replace_negative_one, impute_method)
    
    # Check for multicollinearity
    vif_df = check_multicollinearity(X)
    print("Variance Inflation Factor (VIF) for each predictor:")
    print(vif_df)
    
    # Optionally, handle multicollinearity by removing predictors with high VIF
    high_vif = vif_df[vif_df['VIF'] > 5]
    if not high_vif.empty:
        print("Warning: Some features have high VIF, indicating multicollinearity.")
        print(high_vif)
        # Here you can decide to remove them or keep them
        # For simplicity, we proceed without removing them
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Perform linear regression with scikit-learn
    model, metrics, coefficients = perform_linear_regression(
        X_train, y_train, X_test, y_test, save_dir=save_dir, save_plots=save_plots
    )
    
    # Perform linear regression with statsmodels
    model_sm = perform_statsmodels_regression(
        X_train, y_train, save_dir=save_dir, save_summary=True
    )
    
    # Save coefficients and metrics
    coefficients_path = os.path.join(save_dir, 'model_coefficients.csv')
    coefficients.to_csv(coefficients_path, index=False)
    print(f"Model coefficients saved to {coefficients_path}")
    
    metrics_path = os.path.join(save_dir, 'model_metrics.csv')
    metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
    metrics_df.to_csv(metrics_path)
    print(f"Model evaluation metrics saved to {metrics_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform linear regression analysis between climate variables and bird population.')
    parser.add_argument('--data_path', type=str, required=True, help='Path to the CSV file containing the data.')
    parser.add_argument('--target_column', type=str, default='total_population', help='Name of the target variable column.')
    parser.add_argument('--replace_negative_one', action='store_true', help='Replace -1 with NaN in the data.')
    parser.add_argument('--impute_method', type=str, default='mean', choices=['mean', 'median'], help='Method to impute missing values.')
    parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of the dataset to include in the test split.')
    parser.add_argument('--random_state', type=int, default=42, help='Random seed for reproducibility.')
    parser.add_argument('--save_dir', type=str, default='results/linear_analysis', help='Directory to save results and plots.')
    parser.add_argument('--save_plots', action='store_true', help='Include this flag to save the plots.')
    
    args = parser.parse_args()
    
    main(
        data_file_path=args.data_path,
        target_column=args.target_column,
        replace_negative_one=args.replace_negative_one,
        impute_method=args.impute_method,
        test_size=args.test_size,
        random_state=args.random_state,
        save_dir=args.save_dir,
        save_plots=args.save_plots
    )
