def distances(cells):
    import pyclesperanto_prototype as cle

    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(cells)
    print("pointlist", pointlist.shape)
    distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)
    #show(distance_matrix)

    return distance_matrix