def gaussian_mixture_model(data, number_of_classes : int = 2):
    # model training
    from sklearn import mixture

    # fit a Gaussian Mixture Model with two components
    clf = mixture.GaussianMixture(n_components=number_of_classes, covariance_type='full')
    clf.fit(data)

    return clf
