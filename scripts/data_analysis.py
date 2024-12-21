import pandas as pd

def aggregate_user_data(df):
    """Aggregate data per user for analysis."""
    user_behavior = df.groupby('MSISDN/Number').agg(
        num_sessions=('Bearer Id', 'count'),
        total_duration=('Dur. (ms)', 'sum'),
        total_dl_data=('Total DL (MB)', 'sum'),
        total_ul_data=('Total UL (MB)', 'sum'),
    )
    user_behavior['total_data'] = user_behavior['total_dl_data'] + user_behavior['total_ul_data']
    return user_behavior

def analyze_top_handsets(df):
    """Analyze top handsets and manufacturers."""
    top_10_handsets = df['Handset Type'].value_counts().head(10)
    df['Handset Manufacturer'] = df['Handset Type'].apply(lambda x: x.split(' ')[0])
    top_3_manufacturers = df['Handset Manufacturer'].value_counts().head(3)
    return top_10_handsets, top_3_manufacturers
