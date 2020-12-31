from beetlesafari import ClearControlDataset
from beetlesafari import seconds_to_hours
from beetlesafari import hours_to_seconds

delta_time_in_seconds = hours_to_seconds(1)

start_time_in_seconds = hours_to_seconds(12)
end_time_in_seconds = hours_to_seconds(24)

cc_dataset = ClearControlDataset('C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR')

sigma_noise_removal = 2
sigma_background_removal = 7
spot_detection_threshold = 20


output_dir = "C:/structure/temp/lund/"

import numpy as np
import pyclesperanto_prototype as cle
import beetlesafari as bs

cle.select_device("RTX")



import time
timestamp = time.time()

def from_dataset_to_raw_statistics(
        cc_dataset : ClearControlDataset,
        start_time_in_seconds : float,
        end_time_in_seconds : float = None,
        num_timepoints : int = 1,
        sigma_noise_removal : float = 2,
        sigma_background_removal : float = 7,
        spot_detection_threshold : float = 10
):
    data = None
    spots_to_keep = None

    if end_time_in_seconds is None or num_timepoints == 1:
        # make sure we execute the loop below once
        end_time_in_seconds = start_time_in_seconds + 0.1
        delta_time = 0.1
    else:
        # make a delta_time that allows us to select 10 time points
        delta_time = (end_time_in_seconds - start_time_in_seconds) / (num_timepoints + 1)

    resampled_image = None
    cells = None

    for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time):
        print("DATA", t)

        from beetlesafari import stopwatch

        stopwatch()
        index = cc_dataset.get_index_after_time(t)
        resampled_image = cc_dataset.get_resampled_image(index, resampled_image)

        stopwatch("load")

        print(resampled_image.shape)

        cells, spots = bs.segmentation(resampled_image, cells, sigma_noise_removal=sigma_noise_removal, sigma_background_removal=sigma_background_removal, spot_detection_threshold=spot_detection_threshold)

        stopwatch()

        touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = bs.neighbors(cells)

        stopwatch("determine neighbors")

        spots_to_keep = cle.binary_and(cells, spots, spots_to_keep)
        cle.multiply_images(spots_to_keep, cells, spots)

        pointlist = cle.labelled_spots_to_pointlist(spots)

        stopwatch("centroids")

        # ---------------------------------
        # Measurements
        meausrements = bs.collect_statistics(
            resampled_image, cells,
            #neighbor_statistics=True,
            #intensity_statistics=False,
            #shape_statistics=False,
            #delta_statistics=False,
            touch_matrix=touch_matrix,
            neighbors_of_neighbors=neighbors_of_neighbors,
            neighbors_of_neighbors_of_neighbors=neighbors_of_neighbors_of_neighbors,
            centroids=pointlist
        )

        stopwatch("collect statistics")

        single_timepoint_data = bs.neighborized_feature_vectors(meausrements, [touch_matrix, neighbors_of_neighbors,
                                                                               neighbors_of_neighbors_of_neighbors])

        stopwatch("make feature vectors")

        if data is None:
            data = single_timepoint_data
        else:
            data = np.concatenate((data, single_timepoint_data), 0)

        print("data shape", data.shape)

    return {
        'data':data,
        'index':index,
        'resampled_image':resampled_image,
        'cells':cells,
        'spots':spots,
        'touch_matrix':touch_matrix,
        'neighbors_of_neighbors':neighbors_of_neighbors,
        'neighbors_of_neighbors_of_neighbors':neighbors_of_neighbors_of_neighbors,
        'centroids':pointlist
    }

n_timepoints = 10
bundle = from_dataset_to_raw_statistics(cc_dataset, start_time_in_seconds, end_time_in_seconds, num_timepoints=n_timepoints, spot_detection_threshold=spot_detection_threshold)
data = bundle['data']
print(data.shape)
resampled_image = None
mesh = None

for num_classes in [5]:

    #model = bs.k_means_clustering(data, num_classes)
    model = bs.gaussian_mixture_model(data, num_classes)

    for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time_in_seconds):

        bundle = from_dataset_to_raw_statistics(cc_dataset, t, spot_detection_threshold=spot_detection_threshold)
        cells = bundle['cells']
        single_timepoint_data = bundle['data']
        touch_matrix = bundle['touch_matrix']
        index = bundle['index']
        resampled_image = bundle['resampled_image']
        centroids = bundle['centroids']

        from beetlesafari import stopwatch

        stopwatch()

        # = #cle.draw_mesh_between_touching_labels(cells, mesh)

        if mesh is None:
            mesh = cle.create_like(resampled_image)
        cle.set(mesh, 0)
        mesh = cle.touch_matrix_to_mesh(centroids, touch_matrix, mesh)

        stopwatch("mesh")

        try:
            # print(clf.means_, clf.covariances_)

            gmm_prediction = model.predict(single_timepoint_data)
            #bs.gaussian_mixture_model_predict(model, single_timepoint_data)

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

            path = output_dir + "/kmc" + str(num_classes) + "/"
            if not os.path.exists(path):
                os.mkdir(path)


            from beetlesafari import index_to_clearcontrol_filename
            from skimage.io import imsave
            imsave(path + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))
            print(path + index_to_clearcontrol_filename(index) + ".tif")




            cle.maximum_z_projection(resampled_image, proj_image)
            imsave(output_dir + "/img/" + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))

            #break

        except ValueError:
            pass

