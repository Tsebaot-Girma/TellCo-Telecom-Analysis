import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Task 4.1: Assign engagement and experience scores
def calculate_scores(engagement_data, experience_data):
    # Define engagement features based on available columns
    engagement_feature_columns = ['session_frequency', 'session_duration', 'total_download_traffic', 'total_upload_traffic', 'total_traffic']
    
    # Define experience features based on available columns
    experience_feature_columns = ['Avg RTT DL (ms)', 'TCP DL Retrans. Vol (Bytes)', 'Avg Bearer TP DL (kbps)']

    # Calculate Euclidean distances for Engagement Score
    engagement_data['Engagement Score'] = np.linalg.norm(
        engagement_data[engagement_feature_columns].values - engagement_data[engagement_feature_columns].min().values, axis=1
    )
    
    # Calculate Euclidean distances for Experience Score
    experience_data['Experience Score'] = np.linalg.norm(
        experience_data[experience_feature_columns].values - experience_data[experience_feature_columns].max().values, axis=1
    )
    
    # Merge scores into one DataFrame
    scores = engagement_data[['MSISDN/Number', 'Engagement Score']].merge(
        experience_data[['MSISDN/Number', 'Experience Score']], on='MSISDN/Number'
    )
    
    return scores

# Task 4.2: Calculate satisfaction scores
def calculate_satisfaction(scores):
    scores['Satisfaction Score'] = (scores['Engagement Score'] + scores['Experience Score']) / 2
    top_satisfied = scores.nlargest(10, 'Satisfaction Score')
    return top_satisfied

# Task 4.3: Build regression model to predict satisfaction score
def build_regression_model(scores):
    X = scores[['Engagement Score', 'Experience Score']]
    y = scores['Satisfaction Score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, X_test, y_test

# Task 4.4: Run K-Means on engagement and experience scores
def run_kmeans(scores, k=2):
    kmeans = KMeans(n_clusters=k, random_state=42)
    scores['Cluster'] = kmeans.fit_predict(scores[['Engagement Score', 'Experience Score']])
    return scores, kmeans.cluster_centers_

# Task 4.5: Aggregate average scores per cluster
def aggregate_scores_per_cluster(scores):
    aggregated_scores = scores.groupby('Cluster').agg({
        'Satisfaction Score': 'mean',
        'Engagement Score': 'mean',
        'Experience Score': 'mean'
    }).reset_index()
    return aggregated_scores
