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
    #Top 10 Handsets
    # Filter out 'undefined' values from the 'Handset Type' column
    filtered_df = df[df['Handset Type'] != 'undefined']
    # Get the top 10 handsets excluding 'undefined'
    top_10_handsets = filtered_df['Handset Type'].value_counts().head(10)
    print(top_10_handsets)
    top_10_handsets = df['Handset Type'].value_counts().head(10)
    #Top 3 Handset Manufacturers
    df['Handset Manufacturer'] = df['Handset Type'].apply(lambda x: x.split(' ')[0])
    top_3_manufacturers = df['Handset Manufacturer'].value_counts().head(3)
    #Get the top 5 handsets for each of the top 3 manufacturers
    top_3_manufacturers = top_3_manufacturers.index
    for manufacturer in top_3_manufacturers:
        top_handsets_for_manufacturer = df[df['Handset Manufacturer'] == manufacturer]['Handset Type'].value_counts().head(5)
        print(f"Top 5 handsets for {manufacturer}:\n", top_handsets_for_manufacturer)
    return top_10_handsets, top_3_manufacturers




