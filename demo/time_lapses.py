from beetlesafari import ClearControlDataset
from beetlesafari import seconds_to_hours
from beetlesafari import hours_to_seconds

delta_time_in_seconds = hours_to_seconds(0.25)

start_time_in_seconds = hours_to_seconds(12)
end_time_in_seconds = hours_to_seconds(28)

ds = ClearControlDataset('C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR')

output_dir = "C:/structure/temp/lund/"

import numpy as np
import pyclesperanto_prototype as cle
import beetlesafari as bs

resampled_image = None

for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time_in_seconds):
    index = ds.get_index_after_time(t)
    input_image = cle.push_zyx(ds.get_image(index))
    voxel_size = ds.get_voxel_size_zyx(index)

    resampled_image = cle.resample(input_image, resampled_image, factor_x = voxel_size[2], factor_y = voxel_size[1], factor_z = voxel_size[0])

    print(resampled_image.shape)

    cells = bs.segmentation(resampled_image)

    touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = bs.neighbors(cells)

    distance_matrix = bs.distances(cells)

    # ---------------------------------
    # Measurements
    nearest_neighbor_distance = cle.average_distance_of_n_closest_points(distance_matrix, n=6)
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(touching_neighbor_count, 0, 0)

    regionprops = cle.statistics_of_background_and_labelled_pixels(resampled_image, cells)
    size = cle.push_zyx(np.asarray([[r.area for r in regionprops]]))
    cle.set_column(size, 0, 0)

    intensity = cle.push_zyx(np.asarray([[r.mean_intensity for r in regionprops]]))
    cle.set_column(intensity, 0, 0)

    standard_deviation_intensity = cle.push_zyx(np.asarray([[r.standard_deviation_intensity for r in regionprops]]))
    cle.set_column(intensity, 0, 0)

    major_axis_length = cle.push_zyx(np.asarray([[r.major_axis_length for r in regionprops]]))
    cle.set_column(major_axis_length, 0, 0)

    minor_axis_length = cle.push_zyx(np.asarray([[r.minor_axis_length for r in regionprops]]))
    cle.set_column(minor_axis_length, 0, 0)

    num_classes = 5

    raw_data = [
        size,
        intensity,
        standard_deviation_intensity,
        major_axis_length,
        minor_axis_length,
        touching_neighbor_count,
        #displacement_vector,
        cle.average_distance_of_n_closest_points(distance_matrix, n=1),
        cle.average_distance_of_n_closest_points(distance_matrix, n=2),
        cle.average_distance_of_n_closest_points(distance_matrix, n=3),
        cle.average_distance_of_n_closest_points(distance_matrix, n=4),
        cle.average_distance_of_n_closest_points(distance_matrix, n=5),
        cle.average_distance_of_n_closest_points(distance_matrix, n=6),
        cle.average_distance_of_n_closest_points(distance_matrix, n=10),
        cle.average_distance_of_n_closest_points(distance_matrix, n=15),
        cle.average_distance_of_n_closest_points(distance_matrix, n=20),
    ]

    data = bs.neighborize(raw_data, touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors)

    from sklearn import mixture

    try:
        # fit a Gaussian Mixture Model with two components
        clf = mixture.GaussianMixture(n_components=num_classes, covariance_type='full')
        clf.fit(data)
        # print(clf.means_, clf.covariances_)

        gmm_prediction = clf.predict(data)

        predicition_vector = cle.push_zyx(np.asarray([gmm_prediction]) + 1)
        cle.set_column(predicition_vector, 0, 0)
        prediction_map = cle.replace_intensities(cells, predicition_vector)


        proj_image = cle.create([prediction_map.shape[1], prediction_map.shape[2]])
        proj_image = cle.maximum_z_projection(prediction_map, proj_image)




        from beetlesafari import index_to_clearcontrol_filename
        from skimage.io import imsave
        imsave(output_dir + "/gmm/" + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))




        cle.maximum_z_projection(resampled_image, proj_image)
        imsave(output_dir + "/img/" + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))

    except ValueError:
        pass

