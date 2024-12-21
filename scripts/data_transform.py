import pandas as pd

def convert_bytes_to_mb(df, columns):
    """Convert byte columns to MB."""
    for col in columns:
        df[col] = df[col] / 1048576
    return df

def rename_columns(df, rename_dict):
    """Rename columns based on a dictionary."""
    df.rename(columns=rename_dict, inplace=True)
    return df
