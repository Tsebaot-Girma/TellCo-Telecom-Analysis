import pandas as pd


def calculate_engagement_metrics(data):
    # Aggregate metrics per MSISDN
    metrics = data.groupby('MSISDN/Number').agg(
        session_frequency=('Bearer Id', 'count'),
        session_duration=('Dur. (ms)', 'sum'),
        total_download_traffic=('Total DL (Bytes)', 'sum'),
        total_upload_traffic=('Total UL (Bytes)', 'sum')
    ).reset_index()
    
   # Calculate total traffic as a new column
    metrics['total_traffic'] = metrics['total_download_traffic'] + metrics['total_upload_traffic']
    
    return metrics

def normalize_metrics(metrics):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(metrics[['session_frequency', 'session_duration', 'total_traffic']])
    
    return pd.DataFrame(normalized, columns=['normalized_frequency', 'normalized_duration', 'normalized_traffic'])


def top_customers(metrics, top_n=10):
    top_frequency = metrics.nlargest(top_n, 'session_frequency')
    top_duration = metrics.nlargest(top_n, 'session_duration')
    top_traffic = metrics.nlargest(top_n, 'total_traffic')
    
    return top_frequency, top_duration, top_traffic