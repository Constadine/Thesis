climate_data = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/'

configs = {
    'air_temperature': {
        'file_path_pattern': f'{climate_data}/meteorologi/air_temperature/*.csv',
        'skiprows': 10,
        'usecols': [0, 2],
        'delimiter': ';',
        'column_names': ['Date', 'Temperature'],
        'date_column': 'Date',
        'value_column': 'Temperature',
        'metrics': {
            'mean': {
                'monthly_metric_name': 'Monthly Mean Air Temperature',
                'yearly_metric_name': 'Yearly Mean Air Temperature'
            },
            'std': {
                'monthly_metric_name': 'Monthly Std Dev Air Temperature',
                'yearly_metric_name': 'Yearly Std Dev Air Temperature'
            }
        }
    },

    'air_pressure': {
        'file_path_pattern': f'{climate_data}/meteorologi/air_pressure/*.csv',
        'skiprows': 10,
        'usecols': [0, 2],
        'delimiter': ';',
        'column_names': ['Date', 'Air Pressure'],
        'date_column': 'Date',
        'value_column': 'Air Pressure',
        'metrics': {
            'mean': {
                'monthly_metric_name': 'Monthly Mean Air Pressure',
                'yearly_metric_name': 'Yearly Mean Air Pressure'
            },
            'std': {
                'monthly_metric_name': 'Monthly Std Dev Air Pressure',
                'yearly_metric_name': 'Yearly Std Dev Air Pressure'
            },
        },
    },

    'sea_temp': {
        'file_path_pattern': f'{climate_data}/oceanografi/sea_temp/*.csv',
        'skiprows': 6,
        'usecols': [0, 1],
        'delimiter': ';',
        'column_names': ['Date', 'Sea Temperature'],
        'date_column': 'Date',
        'value_column': 'Sea Temperature',
        'metrics': {
            'mean': {
                'monthly_metric_name': 'Monthly Mean Sea Temperature',
                'yearly_metric_name': 'Yearly Mean Sea Temperature'
            },
            'std': {
                'monthly_metric_name': 'Monthly Std Dev Sea Temperature',
                'yearly_metric_name': 'Yearly Std Dev Sea Temperature'
            },
        },
    },

    'seawater_level': {
        'file_path_pattern': f'{climate_data}/oceanografi//*.csv',
        'skiprows': 6,
        'usecols': [0, 1],
        'delimiter': ';',
        'column_names': ['Date', 'Sea water level'],
        'date_column': 'Date',
        'value_column': 'Sea water level',
        'metrics': {
            'mean': {
                'monthly_metric_name': 'Monthly Mean Sea Water Level',
                'yearly_metric_name': 'Yearly Mean Sea Water Level'
            },
            'std': {
                'monthly_metric_name': 'Monthly Std Dev Sea Water Level',
                'yearly_metric_name': 'Yearly Std Dev Sea Water Level'
            },
        },
    },

    'wave_height': {
        'file_path_pattern': f'{climate_data}/oceanografi/wave_height/*.csv',
        'skiprows': 10,
        'usecols': [0, 1],
        'delimiter': ';',
        'column_names': ['Date', 'Wave Height'],
        'date_column': 'Date',
        'value_column': 'Wave Height',
        'metrics': {
            'mean': {
                'monthly_metric_name': 'Monthly Mean Wave Height',
                'yearly_metric_name': 'Yearly Mean Wave Height'
            },
            'std': {
                'monthly_metric_name': 'Monthly Std Dev Wave Height',
                'yearly_metric_name': 'Yearly Std Dev Wave Height'
            },
        },
    },
    # FIX DELIMITER HERE
    'wind': {
        'file_path_pattern': f'{climate_data}/meteorologi/wind/*.csv',
        'skiprows': 10,
        'usecols': [0, 4],
        'delimiter': ';',
        'column_names': ['Date', 'Wind Speed'],
        'date_column': 'Date',
        'value_column': 'Wind Speed',
        'metrics': {
            'mean': {
                'monthly_metric_name': 'Monthly Mean Wind Speed',
                'yearly_metric_name': 'Yearly Mean Wind Speed'
            },
            'std': {
                'monthly_metric_name': 'Monthly Std Dev Wind Speed',
                'yearly_metric_name': 'Yearly Std Dev Wind Speed'
            },
        },
    },
    # Add other variables with similar structure
}
