from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import silhouette_score

def kmeans(data, n_clusters):
    all_coords = []
    for d in data['data']:
        while d['count'] > 0:
            all_coords += [[d['lat'], d['lng']]]
            d['count'] -= 1
    da = np.array(all_coords)
    if n_clusters < 0:
        n_clusters = 1
    elif (n_clusters == 0):
        return {
            'centers': []
        }

    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')

    kmeans.fit(da)

    cluster_centers = kmeans.cluster_centers_
    return {
        'centers': cluster_centers
    }
