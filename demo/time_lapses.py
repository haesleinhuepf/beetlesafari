import numpy as np
import pyclesperanto_prototype as cle
import beetlesafari as bs

delta_time_in_seconds = bs.minutes_to_seconds(5)

start_time_in_seconds = bs.hours_to_seconds(0)
end_time_in_seconds = bs.hours_to_seconds(48)

cc_dataset = bs.ClearControlDataset('C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/')

sigma_noise_removal = 2
sigma_background_removal = 17
spot_detection_threshold = 25


n_timepoints = 2

num_class_selection = [2, 4, 5, 6, 7, 10]

output_dir = "C:/structure/temp/lund/"


print(cle.select_device("RTX"))



import time
timestamp = time.time()


bundle = bs.from_dataset_to_raw_statistics(cc_dataset, start_time_in_seconds, end_time_in_seconds, num_timepoints=n_timepoints, spot_detection_threshold=spot_detection_threshold)
data = bundle['data']
print(data.shape)
resampled_image = None
mesh = None

for num_classes in num_class_selection:

    #model = bs.k_means_clustering(data, num_classes)
    model = bs.gaussian_mixture_model(data, num_classes)
    #model = bs.spectral_clustering(data, num_classes)

    for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time_in_seconds):

        bundle = bs.from_dataset_to_raw_statistics(cc_dataset, t, spot_detection_threshold=spot_detection_threshold)
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

            path = output_dir + "/img/"
            if not os.path.exists(path):
                os.mkdir(path)

            cle.maximum_z_projection(resampled_image, proj_image)
            imsave(output_dir + "/img/" + index_to_clearcontrol_filename(index) + ".tif", cle.pull_zyx(proj_image))

            # quit()

        except ValueError:
            pass

