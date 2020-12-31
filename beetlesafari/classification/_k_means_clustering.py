def k_means_clustering(data, num_classes):
    # inspired by https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

    from sklearn.cluster import KMeans
    import numpy as np

    return KMeans(n_clusters=num_classes, random_state=0).fit(data)
