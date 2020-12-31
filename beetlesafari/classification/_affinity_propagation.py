
def affinity_propagation(data):
    from sklearn.cluster import AffinityPropagation

    ap = AffinityPropagation()
    ap.fit(data)
