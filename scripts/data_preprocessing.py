import pandas as pd
import numpy as np

def clean_data(df):
    """Clean the dataset by handling duplicates, missing values, and dropping unnecessary columns."""
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)
    
    # Convert ID fields to objects
    id_columns = ['Bearer Id', 'IMSI', 'MSISDN/Number', 'IMEI']
    df[id_columns] = df[id_columns].astype('object')
    
    # Convert timestamps
    timestamp_columns = ['Start', 'End']
    df[timestamp_columns] = df[timestamp_columns].apply(pd.to_datetime)

    
    # Convert text-based columns to category if appropriate
    text_columns = ['Last Location Name','Handset Manufacturer', 'Handset Type']
    df[text_columns] = df[text_columns].astype('category')
    
    return df

def handle_outliers(df, columns):
    """Replace outliers with mean values."""
    for col in columns:
        df[col] = np.where(df[col] > df[col].quantile(0.99), df[col].mean(), df[col])
    return df
