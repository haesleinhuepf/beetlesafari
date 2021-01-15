
def spectral_clustering(data, num_classes):
    from sklearn.cluster import SpectralClustering

    sc = SpectralClustering(n_clusters=num_classes)
    sc.fit(data)

    return sc
