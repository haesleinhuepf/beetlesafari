
from ..io import ClearControlDataset

def from_dataset_to_raw_statistics(
        cc_dataset : ClearControlDataset,
        start_time_in_seconds : float,
        end_time_in_seconds : float = None,
        num_timepoints : int = 1,
        sigma_noise_removal : float = 2,
        sigma_background_removal : float = 7,
        spot_detection_threshold : float = 10
):
    import numpy as np
    from ..processing import segmentation
    import pyclesperanto_prototype as cle
    from ..analysis import collect_statistics
    from ..processing import neighbors
    from ..utils import neighborized_feature_vectors

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
    index = None
    spots = None
    pointlist = None
    touch_matrix = None
    neighbors_of_neighbors = None
    neighbors_of_neighbors_of_neighbors = None

    for t in np.arange(start_time_in_seconds, end_time_in_seconds, delta_time):
        print("Analysing time point just after " + str(t) + " s")

        from beetlesafari import stopwatch

        stopwatch()
        index = cc_dataset.get_index_after_time(t)
        resampled_image = cc_dataset.get_resampled_image(index, resampled_image)

        stopwatch("load")

        print(resampled_image.shape)

        cells, spots = segmentation(resampled_image, cells, sigma_noise_removal=sigma_noise_removal, sigma_background_removal=sigma_background_removal, spot_detection_threshold=spot_detection_threshold)

        stopwatch()

        touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = neighbors(cells)

        stopwatch("determine neighbors")

        #spots_to_keep = cle.binary_and(cells, spots, spots_to_keep)
        #cle.multiply_images(spots_to_keep, cells, spots)

        pointlist = cle.labelled_spots_to_pointlist(spots)

        stopwatch("centroids")

        # ---------------------------------
        # Measurements
        meausrements = collect_statistics(
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

        single_timepoint_data = neighborized_feature_vectors(meausrements, [touch_matrix, neighbors_of_neighbors,
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
