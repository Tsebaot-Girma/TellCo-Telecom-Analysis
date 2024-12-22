import pandas as pd
import numpy as np

def clean_data(df):
    """Clean the dataset by handling duplicates, missing values, and dropping unnecessary columns."""
    # Drop duplicates
    df = df.drop_duplicates()

    # Drop Dur. (ms) and keep Dur. (ms).1
    df.drop(columns=['Dur. (ms)'], inplace=True) 

     # Convert ID fields to objects
    id_columns = ['Bearer Id', 'IMSI', 'MSISDN/Number', 'IMEI']
    df[id_columns] = df[id_columns].astype('object')
    
    # Convert timestamps
    timestamp_columns = ['Start', 'End']
    df[timestamp_columns] = df[timestamp_columns].apply(pd.to_datetime)

    
    # Convert text-based columns to category if appropriate
    text_columns = ['Last Location Name','Handset Manufacturer', 'Handset Type']
    df[text_columns] = df[text_columns].astype('category')
    

    #Drop Rows with Too Many Missing Values
    threshold = 17
    df = df[df.isnull().sum(axis=1) <= threshold]
    # Columns with > 50% missing values
    # Calculate the percentage of missing values
    missing_percentage = 100 * (df.isnull().sum(axis=0) / len(df.index))

    # Filter columns with more than 50% missing values
    columns_to_drop = missing_percentage[missing_percentage > 50].index

    # Drop these columns from the DataFrame
    df.drop(columns=columns_to_drop)

    # Handle missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # List of columns to check
    columns_to_check = ['Handset Manufacturer', 'Handset Type', 'Bearer Id', 
                    'IMSI', 'MSISDN/Number', 'IMEI', 'Last Location Name']

    # Filter rows where all the specified columns are NaN
    rows_with_all_missing = df[df[columns_to_check].isnull().all(axis=1)]
    df.drop(rows_with_all_missing.index)
   
    # Drop rows where the 'MSISDN/Number' column is NaN
    df = df.dropna(subset=['MSISDN/Number'])

    # Drop rows where the 'Bearer Id' column is NaN
    df = df.dropna(subset=['Bearer Id'])

    # Add 'Unknown' to the categories of Last Location Name
    df['Last Location Name'] = df['Last Location Name'].cat.add_categories('Unknown')

    # Replace missing values with 'Unknown' and reassign
    df['Last Location Name'] = df['Last Location Name'].fillna('Unknown')

    return df

def handle_outliers(df, columns):
    """Replace outliers with mean values."""
    #Outliers capped using 99th percentile and replaced with mean values              
    for col in columns:
        df[col] = np.where(df[col] > df[col].quantile(0.99), df[col].mean(), df[col])
    return df


