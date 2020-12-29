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