import pandas as pd

def aggregate_top_users_per_application(data):
    """
    Aggregate user total traffic per application (upload + download) 
    and derive the top 10 most engaged users per application.
    
    Parameters:
    - data (DataFrame): The input DataFrame containing application traffic data.
    
    Returns:
    - dict: A dictionary where keys are application names, and values are DataFrames of the top 10 users.
    """
    # Define upload and download pairs for each application
    application_pairs = {
        'Social Media': ['Social Media DL (Bytes)', 'Social Media UL (Bytes)'],
        'Google': ['Google DL (Bytes)', 'Google UL (Bytes)'],
        'Youtube': ['Youtube DL (Bytes)', 'Youtube UL (Bytes)'],
        'Netflix': ['Netflix DL (Bytes)', 'Netflix UL (Bytes)'],
        'Gaming': ['Gaming DL (Bytes)', 'Gaming UL (Bytes)'],
        'Other': ['Other DL (Bytes)', 'Other UL (Bytes)']
    }
    
    # Dictionary to store top 10 users per application
    top_users_per_application = {}
    
    for app, columns in application_pairs.items():
        # Check if both columns exist in the data
        missing_columns = [col for col in columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in data for {app}: {missing_columns}")
        
        # Calculate total traffic (upload + download) for the application
        data[f'{app} Total Traffic (Bytes)'] = data[columns[0]] + data[columns[1]]
        
        # Group by user and sum total traffic for the application
        user_traffic = data.groupby('MSISDN/Number')[f'{app} Total Traffic (Bytes)'].sum()
        
        # Get the top 10 users for the application
        top_users = user_traffic.nlargest(10).reset_index()
        top_users.columns = ['MSISDN/Number', f'{app} Total Traffic (Bytes)']
        
        # Store in the dictionary
        top_users_per_application[app] = top_users
    
    return top_users_per_application


