import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_histograms(df, numeric_columns):
    """Plot histograms for numerical columns."""
    for col in numeric_columns:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[col], kde=True)
        plt.title(f'Histogram of {col}')
        plt.show()

def plot_scatter(x, y, df):
    """Plot scatterplot for two columns."""
    plt.figure(figsize=(8, 4))
    sns.scatterplot(x=x, y=y, data=df)
    plt.title(f'{x} vs {y}')
    plt.show()

def plot_correlation_matrix(df):
    """Plot the correlation matrix as a heatmap."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()



def plot_top_3_applications(data):
    # Define application pairs (upload + download) for each app
    application_pairs = {
        'Social Media': ['Social Media DL (Bytes)', 'Social Media UL (Bytes)'],
        'Google': ['Google DL (Bytes)', 'Google UL (Bytes)'],
        'Youtube': ['Youtube DL (Bytes)', 'Youtube UL (Bytes)'],
        'Netflix': ['Netflix DL (Bytes)', 'Netflix UL (Bytes)'],
        'Gaming': ['Gaming DL (Bytes)', 'Gaming UL (Bytes)'],
        'Other': ['Other DL (Bytes)', 'Other UL (Bytes)']
    }
    
    # Dictionary to store total traffic for each application
    total_traffic_per_application = {}
    
    # Calculate total traffic (upload + download) for each application
    for app, columns in application_pairs.items():
        # Calculate total traffic for each application
        data[f'{app} Total Traffic (Bytes)'] = data[columns[0]] + data[columns[1]]
        
        # Sum total traffic for the entire dataset for this application
        total_traffic_per_application[app] = data[f'{app} Total Traffic (Bytes)'].sum()
    
    # Convert the dictionary to a DataFrame for easier plotting
    total_traffic_df = pd.DataFrame(list(total_traffic_per_application.items()), columns=['Application', 'Total Traffic (Bytes)'])
    
    # Sort by total traffic and get the top 3 most used applications
    top_3_apps = total_traffic_df.nlargest(3, 'Total Traffic (Bytes)')
    
    # Plot the top 3 most used applications using a bar chart
    plt.figure(figsize=(7, 6))
    plt.bar(top_3_apps['Application'], top_3_apps['Total Traffic (Bytes)'], color=['blue', 'orange', 'green'])
    plt.title('Top 3 Most Used Applications Based on Total Traffic')
    plt.xlabel('Application')
    plt.ylabel('Total Traffic (Bytes)')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()


def visualize_clusters(data, x_col, y_col, cluster_col='Cluster'):
    """
    Visualize the clusters using a scatter plot.
    
    Parameters:
        data (pd.DataFrame): Data with cluster labels.
        x_col (str): The column to use for the x-axis.
        y_col (str): The column to use for the y-axis.
        cluster_col (str): The column containing cluster labels.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(data[x_col], data[y_col], c=data[cluster_col], cmap='viridis', marker='o')
    plt.title('K-Means Clustering of Users')
    plt.xlabel(x_col.replace('_', ' ').title())
    plt.ylabel(y_col.replace('_', ' ').title())
    plt.colorbar(label='Cluster')
    plt.show()