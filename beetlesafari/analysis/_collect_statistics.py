import pyclesperanto_prototype as cle

def collect_statistics(
        image : cle.Image,
        cells : cle.Image,
        subsequent_image : cle.Image = None,
        subsequent_cells : cle.Image = None,
        neighbor_statistics : bool = True,
        intensity_statistics : bool = True,
        shape_statistics : bool = True,
        delta_statistics : bool = True,
        touch_matrix : cle.Image = None,
        neighbors_of_neighbors : cle.Image = None,
        neighbors_of_neighbors_of_neighbors : cle.Image = None,
        centroids : cle.Image = None
):
    from ..processing import distances, neighbors
    from ..utils import stopwatch
    import numpy as np

    dict = {}

    if neighbor_statistics or shape_statistics:
        # stopwatch()
        if touch_matrix is None or neighbors_of_neighbors is None or neighbors_of_neighbors_of_neighbors is None:
            touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = neighbors(cells)

        # stopwatch("init")
        if centroids is None:
            centroids = cle.centroids_of_labels(cells)
            # stopwatch("centroids")

        #print("pointlist", pointlist.shape)
        distance_matrix = cle.generate_distance_matrix(centroids, centroids)
        # stopwatch("dist matrix")

        if neighbor_statistics:
            # topology measurements
            dict['nearest_neighbor_distance_n1'] = _cle_to_1d_np(cle.average_distance_of_n_closest_points(distance_matrix, n=1))

            # stopwatch("avg dst 1")

            #dict['nearest_neighbor_distance_n4'] = _cle_to_1d_np(cle.average_distance_of_n_closest_points(distance_matrix, n=4))
            dict['nearest_neighbor_distance_n6'] = _cle_to_1d_np(cle.average_distance_of_n_closest_points(distance_matrix, n=6))

            # stopwatch("avg dst 2")

            #dict['nearest_neighbor_distance_n8'] = _cle_to_1d_np(cle.average_distance_of_n_closest_points(distance_matrix, n=8))
            dict['nearest_neighbor_distance_n20']= _cle_to_1d_np(cle.average_distance_of_n_closest_points(distance_matrix, n=20))

            # stopwatch("avg dst 3")

            dict['nearest_neighbor_distance'] = _cle_to_1d_np(cle.average_distance_of_n_closest_points(distance_matrix, n=1))

            # stopwatch("avg dst 4")

            dict['touching_neighbor_count'] = _cle_to_1d_np(cle.count_touching_neighbors(touch_matrix))

            # stopwatch("avg dst 5")
        if shape_statistics:
            dict['minimum_distance_of_touching_neighbors'] = _cle_to_1d_np(cle.minimum_distance_of_touching_neighbors(distance_matrix, touch_matrix))
            dict['maximum_distance_of_touching_neighbors'] = _cle_to_1d_np(cle.maximum_distance_of_touching_neighbors(distance_matrix, touch_matrix))
            dict['average_distance_of_touching_neighbors'] = _cle_to_1d_np(cle.average_distance_of_touching_neighbors(distance_matrix, touch_matrix))
            dict['aspect_ratio_between_touching_neighbors'] = _regionprops_to_1d_np(dict['maximum_distance_of_touching_neighbors'] / dict['minimum_distance_of_touching_neighbors'])

    if delta_statistics or intensity_statistics or shape_statistics:
        # stopwatch("B")

        # intensity based measurements
        regionprops = cle.statistics_of_background_and_labelled_pixels(image, cells)

        if intensity_statistics:
            dict['mean_intensity'] = _regionprops_to_1d_np(regionprops['mean_intensity'])
            dict['standard_deviation_intensity'] = _regionprops_to_1d_np(regionprops['standard_deviation_intensity'])
            dict['minimum_intensity'] = _regionprops_to_1d_np(regionprops['min_intensity'])
            dict['maximum_intensity'] = _regionprops_to_1d_np(regionprops['max_intensity'])

        # intensity measurements related to second timepoint
        if delta_statistics and subsequent_image is not None:
            # determine local changes
            squared_difference_image = cle.squared_difference(image, subsequent_image)
            regionprops2 = cle.statistics_of_background_and_labelled_pixels(squared_difference_image, cells)
            dict['mean_squared_error_intensity'] = _regionprops_to_1d_np(regionprops2['mean_intensity'])

        if shape_statistics:
            dict['size'] = _regionprops_to_1d_np(regionprops['area'])

            # shape measurements
            #dict['major_axis_length'] = _regionprops_to_1d_np(regionprops['major_axis_length'])
            #dict['minor_axis_length'] = _regionprops_to_1d_np(regionprops['minor_axis_length'])

            dict['sum_distance_to_centroid'] = _regionprops_to_1d_np(regionprops['sum_distance_to_centroid'])
            dict['mean_distance_to_centroid'] = _regionprops_to_1d_np(regionprops['mean_distance_to_centroid'])
            dict['mean_max_distance_to_centroid_ratio'] = _regionprops_to_1d_np(regionprops['mean_max_distance_to_centroid_ratio'])

        # measurements related to second timepoint
        if delta_statistics and subsequent_cells is not None:
            # measure distance to closest cell centroid in the other image
            other_pointlist = cle.centroids_of_labels(subsequent_cells)
            displacement_matrix = cle.generate_distance_matrix(centroids, other_pointlist)
            dict['displacement_estimation'] = _cle_to_1d_np(cle.average_distance_of_n_closest_points(displacement_matrix))
    # stopwatch("C")

    # ignore measurements with background
    for key in dict.keys():
        dict[key][0] = 0

    # stopwatch("D")

    return dict

def _cle_to_1d_np(image : cle.Image):
    # workaround
    image = cle.undefined_to_zero(image)

    result = cle.pull_zyx(image)
    return result[0]

def _regionprops_to_1d_np(values : list):
    import numpy as np
    import math
    values = [v if not math.isnan(v) or math.isinf(v) else 0 for v in values]
    return np.asarray(values)
