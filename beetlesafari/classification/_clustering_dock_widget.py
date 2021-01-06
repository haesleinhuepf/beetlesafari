from magicgui import magicgui
from napari.layers import Image

from beetlesafari import stopwatch


@magicgui(
    auto_call=True,
    layout='vertical',
    algorithm={'choices':['k_means_clustering', 'gaussian_mixture_model']}
)
def __clustering_dock_widget(input1 : Image = None,
                                input2 : Image = None,
                                algorithm : str = 'k_means_clustering',
                                num_classes : int = 2,
                                train : bool = False,
                                neighbor_statistics: bool = True,
                                intensity_statistics: bool = True,
                                shape_statistics: bool = True,
                                delta_statistics: bool = True,
                                ):

    if input1 is None or input2 is None:
        print("no data")
        return

    if not train and __clustering_dock_widget.model is None:
        print("no model leaving")
        return

    import numpy as np
    import beetlesafari as bs
    import pyclesperanto_prototype as cle
    import pyopencl

    try:
        intensity = cle.push_zyx(input1.data)
        labels = cle.push_zyx(input2.data)

        stopwatch()
        touch_matrix, neighbors_of_neighbors, neighbors_of_neighbors_of_neighbors = bs.neighbors(labels)
        stopwatch("determine neighbors")

        centroids = cle.centroids_of_labels(labels)
        stopwatch("determine centroids")

        # ---------------------------------
        # Measurements
        meausrements = bs.collect_statistics(
            intensity, labels,
            neighbor_statistics=neighbor_statistics,
            intensity_statistics=intensity_statistics,
            shape_statistics=shape_statistics,
            delta_statistics=delta_statistics,
            touch_matrix=touch_matrix,
            neighbors_of_neighbors=neighbors_of_neighbors,
            neighbors_of_neighbors_of_neighbors=neighbors_of_neighbors_of_neighbors,
            centroids=centroids
        )
        stopwatch("collect statistics")

        data = bs.neighborized_feature_vectors(meausrements, [touch_matrix, neighbors_of_neighbors,
                                                              neighbors_of_neighbors_of_neighbors])

        if train:
            if algorithm == 'k_means_clustering':
                __clustering_dock_widget.model = bs.k_means_clustering(data, num_classes)
            if algorithm == 'gaussian_mixture_model':
                __clustering_dock_widget.model = bs.gaussian_mixture_model(data, num_classes)

            bs.stopwatch("train")

        mesh = cle.create_like(intensity)
        cle.set(mesh, 0)
        mesh = cle.touch_matrix_to_mesh(centroids, touch_matrix, mesh)
        stopwatch("mesh")

        prediction = __clustering_dock_widget.model.predict(data)

        prediction_vector = cle.push_zyx(np.asarray([prediction]) + 1)
        cle.set_column(prediction_vector, 0, 0)

        prediction_vector = cle.mode_of_touching_neighbors(prediction_vector, touch_matrix)
        cle.set_column(prediction_vector, 0, 0)

        prediction_map = cle.replace_intensities(labels, prediction_vector)

        # pred_stats = cle.statistics_of_labelled_pixels(None, prediction_map, measure_shape=False)
        # pred_size = cle.push_regionprops_column(pred_stats, 'area')
        # cle.set_column(pred_size, 0, 0)

        # prediction_map = cle.replace_intensities(prediction_map, pred_size)
        prediction_map = cle.multiply_images(prediction_map, mesh)

        # show result in napari
        if (__clustering_dock_widget.initial_call):
            __clustering_dock_widget.self.viewer.add_labels(cle.pull_zyx(prediction_map))
            __clustering_dock_widget.initial_call = False
        else:
            __clustering_dock_widget.self.layer.data = cle.pull_zyx(prediction_map)
            __clustering_dock_widget.self.layer.name = algorithm + "(" +str(num_classes)+ " classes)"
            #__clustering_dock_widget.self.layer.contrast_limits = (0, num_classes)

        #proj_image = cle.create([prediction_map.shape[1], prediction_map.shape[2]])
        #proj_image = cle.maximum_z_projection(prediction_map, proj_image)
    except pyopencl._cl.MemoryError:
        print ("OCL Memory error")
    except pyopencl._cl.RuntimeError:
        print("OCL Runtime error")

__clustering_dock_widget.model = None


from napari_pyclesperanto_assistant import AssistantGUI

def attach_clustering_dock_widget(assistant : AssistantGUI):

    assistant.add_button("Beetlesafari clustering", __clustering_dock_widget)
