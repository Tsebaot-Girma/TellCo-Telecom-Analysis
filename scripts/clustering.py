import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def perform_kmeans_clustering(normalized_data, k=3):
    kmeans = KMeans(n_clusters=k)
    normalized_data['cluster'] = kmeans.fit_predict(normalized_data)
    return normalized_data



def apply_kmeans_clustering(data, k):
    """
    Apply K-Means clustering to the normalized data.
    
    Parameters:
        data (pd.DataFrame): The normalized data containing engagement metrics.
        k (int): The number of clusters (optimal k).
    
    Returns:
        pd.DataFrame: Data with an additional 'Cluster' column.
        np.ndarray: Cluster centers.
    """
    kmeans = KMeans(n_clusters=k, random_state=42)
    data['Cluster'] = kmeans.fit_predict(data[['normalized_frequency', 'normalized_duration', 'normalized_traffic']])
    return data, kmeans.cluster_centers_



def elbow_method(data):
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    
    inertia = []
    k_range = range(1, 10)
    for k in k_range:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)
        inertia.append(kmeans.inertia_)
    
    plt.plot(k_range, inertia)
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method')
    plt.show()

def cluster_statistics(data):
    stats = data.groupby('cluster').agg(
        min_frequency=('session_frequency', 'min'),
        max_frequency=('session_frequency', 'max'),
        avg_frequency=('session_frequency', 'mean'),
        total_frequency=('session_frequency', 'sum'),
        min_duration=('session_duration', 'min'),
        max_duration=('session_duration', 'max'),
        avg_duration=('session_duration', 'mean'),
        total_duration=('session_duration', 'sum'),
        min_traffic=('total_traffic', 'min'),
        max_traffic=('total_traffic', 'max'),
        avg_traffic=('total_traffic', 'mean'),
        total_traffic=('total_traffic', 'sum')
    ).reset_index()
    
    return stats