import matplotlib.pyplot as plt
import seaborn as sns

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
