import pandas as pd

def calculate_engagement_metrics(data):
    # Aggregate metrics per MSISDN
    metrics = data.groupby('MSISDN/Number').agg(
        session_frequency=('Bearer Id', 'count'),
        session_duration=('Dur. (ms)', 'sum'),
        total_traffic=('Total DL (MB)', 'sum') + ('Total UL (MB)', 'sum')
    ).reset_index()
    
    return metrics

def normalize_metrics(metrics):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(metrics[['session_frequency', 'session_duration', 'total_traffic']])
    
    return pd.DataFrame(normalized, columns=['normalized_frequency', 'normalized_duration', 'normalized_traffic'])