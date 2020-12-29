import pyclesperanto_prototype as cle

def collect_statistics(
        image : cle.Image,
        cells : cle.Image,
        subsequent_image : cle.Image = None,
        subsequent_cells : cle.Image = None,
        neighbor_statistics : bool = True,
        intensity_statistics : bool = True,
        delta_statistics : bool = True
):
    from ..processing import distances, neighbors
    import numpy as np

    dict = {}

    touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = neighbors(cells)

    pointlist = cle.centroids_of_labels(cells)
    #print("pointlist", pointlist.shape)
    distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)

    # topology measurements
    dict['nearest_neighbor_distance_n1'] = cle.average_distance_of_n_closest_points(distance_matrix, n=1)
    dict['nearest_neighbor_distance_n4'] = cle.average_distance_of_n_closest_points(distance_matrix, n=4)
    dict['nearest_neighbor_distance_n6'] = cle.average_distance_of_n_closest_points(distance_matrix, n=6)
    dict['nearest_neighbor_distance_n8'] = cle.average_distance_of_n_closest_points(distance_matrix, n=8)
    dict['nearest_neighbor_distance_n20'] = cle.average_distance_of_n_closest_points(distance_matrix, n=20)

    dict['nearest_neighbor_distance'] = cle.average_distance_of_n_closest_points(distance_matrix, n=1)
    dict['touching_neighbor_count'] = cle.count_touching_neighbors(touch_matrix)

    # intensity based measurements
    regionprops = cle.statistics_of_background_and_labelled_pixels(image, cells)
    dict['size'] = cle.push_zyx(np.asarray([[r.area for r in regionprops]]))
    dict['mean_intensity'] = cle.push_zyx(np.asarray([[r.mean_intensity for r in regionprops]]))
    dict['standard_deviation_intensity'] = cle.push_zyx(np.asarray([[r.standard_deviation_intensity for r in regionprops]]))
    dict['minimum_intensity'] = cle.push_zyx(np.asarray([[r.min_intensity for r in regionprops]]))
    dict['maximum_intensity'] = cle.push_zyx(np.asarray([[r.max_intensity for r in regionprops]]))

    # intensity measurements related to second timepoint
    if delta_statistics and subsequent_image is not None:
        # determine local changes
        squared_difference_image = cle.squared_difference(image, subsequent_image)
        regionprops2 = cle.statistics_of_background_and_labelled_pixels(squared_difference_image, cells)
        dict['mean_squared_error_intensity'] = cle.push_zyx(np.asarray([[r.mean_intensity for r in regionprops2]]))

    # shape measurements
    dict['major_axis_length'] = cle.push_zyx(np.asarray([[r.major_axis_length for r in regionprops]]))
    dict['minor_axis_length'] = cle.push_zyx(np.asarray([[r.minor_axis_length for r in regionprops]]))

    dict['sum_distance_to_centroid'] = cle.push_zyx(np.asarray([[r.sum_distance_to_centroid for r in regionprops]]))
    dict['mean_distance_to_centroid'] = cle.push_zyx(np.asarray([[r.mean_distance_to_centroid for r in regionprops]]))
    dict['mean_max_distance_to_centroid_ratio'] = cle.push_zyx(np.asarray([[r.mean_max_distance_to_centroid_ratio for r in regionprops]]))

    # measurements related to second timepoint
    if delta_statistics and subsequent_cells is not None:
        # measure distance to closest cell centroid in the other image
        other_pointlist = cle.centroids_of_labels(subsequent_cells)
        displacement_matrix = cle.generate_distance_matrix(pointlist, other_pointlist)
        dict['displacement_estimation'] = cle.average_distance_of_n_closest_points(displacement_matrix)

    # ignore measurements with background
    for key in dict.keys():
        cle.set_column(dict[key], 0, 0)

    return dict
