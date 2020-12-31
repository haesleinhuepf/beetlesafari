from beetlesafari import ClearControlDataset
from beetlesafari import seconds_to_hours
from beetlesafari import hours_to_seconds

delta_time_in_seconds = hours_to_seconds(0.5)

start_time_in_seconds = hours_to_seconds(14)
end_time_in_seconds = hours_to_seconds(26)

ds = ClearControlDataset('C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR')

output_dir = "C:/structure/temp/lund/"

import numpy as np
import pyclesperanto_prototype as cle
import beetlesafari as bs

cle.select_device("RTX")


resampled_image = None
mesh = None

import time
timestamp = time.time()

# make a delta_time that allows us to select 10 time points
n_timepoints = 5
delta_time = (end_time_in_seconds - start_time_in_seconds) / (n_timepoints + 1)

for num_classes in [4, 6]:

    data = None

    for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time):
        print("delta time                          ", time.time() - timestamp)
        timestamp = time.time()

        index = ds.get_index_after_time(t)
        input_image = cle.push_zyx(ds.get_image(index))
        voxel_size = ds.get_voxel_size_zyx(index)

        resampled_image = cle.resample(input_image, resampled_image, factor_x = voxel_size[2], factor_y = voxel_size[1], factor_z = voxel_size[0])

        print(resampled_image.shape)

        cells = bs.segmentation(resampled_image)

        touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = bs.neighbors(cells)

        # ---------------------------------
        # Measurements
        meausrements = bs.collect_statistics(resampled_image, cells)

        single_timepoint_data = bs.neighborized_feature_vectors(meausrements, [touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors])

        if data is None:
            data = single_timepoint_data
        else:
            data = np.concatenate((data, single_timepoint_data), 0)

        print("data shape", data.shape)

    # model training
    from sklearn import mixture

    # fit a Gaussian Mixture Model with two components
    clf = mixture.GaussianMixture(n_components=num_classes, covariance_type='full')
    clf.fit(data)

    for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time_in_seconds):

        index = ds.get_index_after_time(t)
        input_image = cle.push_zyx(ds.get_image(index))
        voxel_size = ds.get_voxel_size_zyx(index)

        resampled_image = cle.resample(input_image, resampled_image, factor_x = voxel_size[2], factor_y = voxel_size[1], factor_z = voxel_size[0])

        print(resampled_image.shape)

        cells = bs.segmentation(resampled_image)

        touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = bs.neighbors(cells)

        mesh = cle.draw_mesh_between_touching_labels(cells, mesh)

        # ---------------------------------
        # Measurements
        meausrements = bs.collect_statistics(resampled_image, cells)

        single_timepoint_data = bs.neighborized_feature_vectors(meausrements, [touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors])


        try:
            # print(clf.means_, clf.covariances_)

            gmm_prediction = clf.predict(single_timepoint_data)

            prediction_vector = cle.push_zyx(np.asarray([gmm_prediction]) + 1)
            cle.set_column(prediction_vector, 0, 0)

            prediction_vector = cle.mode_of_touching_neighbors(prediction_vector, touch_matrix)
            cle.set_column(prediction_vector, 0, 0)

            prediction_map = cle.replace_intensities(cells, prediction_vector)

            #pred_stats = cle.statistics_of_labelled_pixels(None, prediction_map, measure_shape=False)
            #pred_size = cle.push_regionprops_column(pred_stats, 'area')
            #cle.set_column(pred_size, 0, 0)

            #prediction_map = cle.replace_intensities(prediction_map, pred_size)

            prediction_map = cle.multiply_images(prediction_map, mesh)

            proj_image = cle.create([prediction_map.shape[1], prediction_map.shape[2]])
            proj_image = cle.maximum_z_projection(prediction_map, proj_image)

            import os

            path = output_dir + "/gmm" + str(num_classes) + "/"
            if not os.path.exists(path):
                os.mkdir(path)


            from beetlesafari import index_to_clearcontrol_filename
            from skimage.io import imsave
            imsave(path + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))
            print(path + index_to_clearcontrol_filename(index) + ".tif")




            cle.maximum_z_projection(resampled_image, proj_image)
            imsave(output_dir + "/img/" + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))

            # break

        except ValueError:
            pass

