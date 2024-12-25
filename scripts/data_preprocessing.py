import pandas as pd
import numpy as np


def clean_data(df):
    """Clean the dataset by handling duplicates, missing values, and dropping unnecessary columns."""
    # Drop duplicates
    df = df.drop_duplicates()

    # Drop Dur. (ms) and keep Dur. (ms).1
    if 'Dur. (ms)' in df.columns:
        df.drop(columns=['Dur. (ms)'], inplace=True)

    # Convert ID fields to objects
    id_columns = ['Bearer Id', 'IMSI', 'MSISDN/Number', 'IMEI']
    for col in id_columns:
        if col in df.columns:
            df[col] = df[col].astype('object')

    # Convert timestamps
    timestamp_columns = ['Start', 'End']
    for col in timestamp_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Convert text-based columns to category if they exist
    text_columns = ['Last Location Name', 'Handset Manufacturer', 'Handset Type']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # Drop rows with too many missing values
    threshold = 17
    df = df[df.isnull().sum(axis=1) <= threshold]

    # Drop columns with > 50% missing values
    missing_percentage = 100 * (df.isnull().sum() / len(df))
    columns_to_drop = missing_percentage[missing_percentage > 50].index
    df.drop(columns=columns_to_drop, inplace=True)

    # Handle missing numeric values with the column mean
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Drop rows where key columns are NaN
    key_columns = ['MSISDN/Number', 'Bearer Id']
    for col in key_columns:
        if col in df.columns:
            df = df.dropna(subset=[col])

    # Add 'Unknown' to the categories of 'Last Location Name' if it exists
    if 'Last Location Name' in df.columns:
        df['Last Location Name'] = df['Last Location Name'].cat.add_categories('Unknown')
        df['Last Location Name'] = df['Last Location Name'].fillna('Unknown')

    return df



def handle_outliers(df, columns):
    """Replace outliers with mean values."""
    #Outliers capped using 99th percentile and replaced with mean values              
    for col in columns:
        df[col] = np.where(df[col] > df[col].quantile(0.99), df[col].mean(), df[col])
    return df


