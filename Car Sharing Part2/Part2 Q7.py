import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

df = pd.read_csv('CarSharing.csv')

# Filter data for the year 2017
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')
df_2017 = df[df['timestamp'].dt.year == 2017]

# Extract the temperature (temp) column and remove missing or NaN values
temp_data = df_2017['temp'].values
temp_data = temp_data[~np.isnan(temp_data)].reshape(-1, 1)  # Reshape for clustering

# Define k values for clustering
k_values = [2, 3, 4, 12]

# Perform k-means clustering for each k value
cluster_results = {}
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(temp_data)
    clusters = kmeans.labels_
    cluster_results[k] = clusters

# Calculate the number of samples in each cluster for each k value
cluster_counts = {}
for k, clusters in cluster_results.items():
    counts = pd.Series(clusters).value_counts().sort_index()
    cluster_counts[k] = counts

# Print the cluster counts for each k value
for k, counts in cluster_counts.items():
    print(f'Cluster counts for k={k}:')
    print(counts)
    print()

