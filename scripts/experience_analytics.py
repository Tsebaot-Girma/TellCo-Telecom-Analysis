import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Aggregate per customer
def aggregate_customer_data(df):
    # Aggregate data
    aggregated_data = df.groupby('MSISDN/Number').agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'TCP UL Retrans. Vol (Bytes)': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Avg RTT UL (ms)': 'mean',
        'Avg Bearer TP DL (kbps)': 'mean',
        'Avg Bearer TP UL (kbps)': 'mean',
        'Handset Type': 'first'  # assuming one handset type per user
    }).reset_index()
    
    return aggregated_data

# Compute top, bottom, and frequent values
def compute_top_bottom_frequent(df):
    tcp_top = df['TCP DL Retrans. Vol (Bytes)'].nlargest(10)
    tcp_bottom = df['TCP DL Retrans. Vol (Bytes)'].nsmallest(10)
    tcp_freq = df['TCP DL Retrans. Vol (Bytes)'].value_counts().nlargest(10)

    rtt_top = df['Avg RTT DL (ms)'].nlargest(10)
    rtt_bottom = df['Avg RTT DL (ms)'].nsmallest(10)
    rtt_freq = df['Avg RTT DL (ms)'].value_counts().nlargest(10)

    throughput_top = df['Avg Bearer TP DL (kbps)'].nlargest(10)
    throughput_bottom = df['Avg Bearer TP DL (kbps)'].nsmallest(10)
    throughput_freq = df['Avg Bearer TP DL (kbps)'].value_counts().nlargest(10)

    return {
        'tcp_top': tcp_top,
        'tcp_bottom': tcp_bottom,
        'tcp_freq': tcp_freq,
        'rtt_top': rtt_top,
        'rtt_bottom': rtt_bottom,
        'rtt_freq': rtt_freq,
        'throughput_top': throughput_top,
        'throughput_bottom': throughput_bottom,
        'throughput_freq': throughput_freq
    }

# Analyze distribution of throughput and average TCP retransmission

def analyze_throughput_per_handset(df):
    # Throughput statistics per handset
    throughput_distribution = df.groupby('Handset Type', observed=False)[
        ['Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']
    ].describe().reset_index()

    # Average TCP retransmission volumes per handset
    tcp_retransmission_per_handset = df.groupby('Handset Type', observed=False)[
        ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)']
    ].mean().reset_index()

    # Flatten the multi-index columns for throughput statistics
    throughput_distribution.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in throughput_distribution.columns.values]

    # Visualization: Top 10 Handsets by Downlink Throughput
    throughput_distribution_mean = throughput_distribution[['Handset Type', 'Avg Bearer TP DL (kbps) mean']]
    throughput_distribution_mean.sort_values(by='Avg Bearer TP DL (kbps) mean', ascending=False).head(10).plot(
        x='Handset Type', y='Avg Bearer TP DL (kbps) mean', kind='bar', figsize=(10, 6), title='Top 10 Handsets by Downlink Throughput'
    )
    plt.xlabel('Handset Type')
    plt.ylabel('Avg Downlink Throughput (kbps)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Visualization: Top 10 Handsets by UPlink Throughput
    throughput_distribution_mean = throughput_distribution[['Handset Type', 'Avg Bearer TP UL (kbps) mean']]
    throughput_distribution_mean.sort_values(by='Avg Bearer TP UL (kbps) mean', ascending=False).head(10).plot(
        x='Handset Type', y='Avg Bearer TP UL (kbps) mean', kind='bar', figsize=(10, 6), title='Top 10 Handsets by Downlink Throughput'
    )
    plt.xlabel('Handset Type')
    plt.ylabel('Avg Uplink Throughput (kbps)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Visualization: Top 10 Handsets by TCP Downlink Retransmission Volume
    tcp_retransmission_sorted = tcp_retransmission_per_handset.sort_values(
        by='TCP DL Retrans. Vol (Bytes)', ascending=False
    ).head(10)
    tcp_retransmission_sorted.plot(
        x='Handset Type', y='TCP DL Retrans. Vol (Bytes)', kind='bar', figsize=(10, 6), title='Top 10 Handsets by TCP Downlink Retransmission Volume'
    )
    plt.xlabel('Handset Type')
    plt.ylabel('TCP DL Retrans. Volume (Bytes)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

     # Visualization: Top 10 Handsets by TCP Uplink Retransmission Volume
    tcp_retransmission_sorted = tcp_retransmission_per_handset.sort_values(
        by='TCP UL Retrans. Vol (Bytes)', ascending=False
    ).head(10)
    tcp_retransmission_sorted.plot(
        x='Handset Type', y='TCP UL Retrans. Vol (Bytes)', kind='bar', figsize=(10, 6), title='Top 10 Handsets by TCP Uplink Retransmission Volume'
    )
    plt.xlabel('Handset Type')
    plt.ylabel('TCP UL Retrans. Volume (Bytes)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return throughput_distribution, tcp_retransmission_per_handset


# Task 3.4: K-Means clustering
def perform_kmeans_clustering(df, k=3):
    features = df[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']]
    kmeans = KMeans(n_clusters=k, random_state=42)
    df['Cluster'] = kmeans.fit_predict(features)
    return df, kmeans.cluster_centers_