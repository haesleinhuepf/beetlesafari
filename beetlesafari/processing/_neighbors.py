def neighbors(cells):
    import pyclesperanto_prototype as cle

    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(cells)

    # ignore touching the background
    cle.set_column(touch_matrix, 0, 0)
    cle.set_row(touch_matrix, 0, 0)

    print(touch_matrix.shape)
    #show(touch_matrix)

    # determine neighbors of neigbors
    neighbors_of_neighbors = cle.neighbors_of_neighbors(touch_matrix)
    #show(neighbors_of_neighbors)

    # determine neighbors of neighbors of neighbors
    neighbors_of_neighbors_of_neighbors = cle.neighbors_of_neighbors(neighbors_of_neighbors)
    #show(neighbors_of_neighbors_of_neighbors)

    return touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors

def neighborize(raw_data, touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors):
    import pyclesperanto_prototype as cle

    neighborhoods = [touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors]

    preproc_data = []

    for element in raw_data:
        # print(element[0].size)
        preproc_data.append(element[0])

        for neighborhood in neighborhoods:
            median = cle.median_of_touching_neighbors(element, neighborhood)
            preproc_data.append(median[0])

            stddev = cle.standard_deviation_of_touching_neighbors(element, neighborhood)
            preproc_data.append(stddev[0])

            mean = cle.mean_of_touching_neighbors(element, neighborhood)
            preproc_data.append(mean[0])

            minimum = cle.minimum_of_touching_neighbors(element, neighborhood)
            preproc_data.append(minimum[0])

            maximum = cle.maximum_of_touching_neighbors(element, neighborhood)
            preproc_data.append(maximum[0])
    import numpy as np

    data = np.asarray(preproc_data).T
    print(data.shape)

    return data