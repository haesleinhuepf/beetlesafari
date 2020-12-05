foldername = 'C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/stacks/C0opticsprefused'
width = 512
height = 1024
depth = 71
voxel_size = [1, 3, 0.6934, 0.6934]

import beetlesafari as bs
from functools import lru_cache

#
img_arr = bs.imread_raw_folder(foldername  + "/000*0.raw", width, height, depth)

import pyclesperanto_prototype as cle
print(cle.cl_info())

cle.select_device("RTX")
print(cle.get_device())

def background_subtraction(input : cle.Image, output : cle.Image):
    import time
    start_time = time.time()
    #cle.top_hat_sphere(input, output, radius_x, radius_y, radius_z)
    cle.difference_of_gaussian(input, output, 1,1,0,5,5,0)
    print("subtract background took " + str(time.time() - start_time))
    return output

def spot_detection(input : cle.Image, output : cle.Image, threshold : float = 50.0):
    import time
    start_time = time.time()

    # permanently allocate temporary images
    if not hasattr(spot_detection, 'temp_flip'):
        spot_detection.temp_flip = cle.create(input)
    if not hasattr(spot_detection, 'temp_flop'):
        spot_detection.temp_flop = cle.create(input)

    # detect maxima
    cle.detect_maxima_box(input, spot_detection.temp_flop)

    # threshold
    cle.greater_constant(input, output, constant=threshold)

    # mask
    cle.binary_and(output, spot_detection.temp_flop, spot_detection.temp_flip)

    # label spots
    cle.connected_components_labeling_box(spot_detection.temp_flip, output)

    print("spot detection took " + str(time.time() - start_time))
    return output

def cell_segmentation(input : cle.Image, output : cle.Image, number_of_dilations : int = 10, number_of_erosions : int = 4):
    import time
    start_time = time.time()

    # permanently allocate temporary images
    if not hasattr(cell_segmentation, 'temp_flip'):
        cell_segmentation.temp_flip = cle.create(input)
    if not hasattr(cell_segmentation, 'temp_flop'):
        cell_segmentation.temp_flop = cle.create(input)
    if not hasattr(cell_segmentation, 'temp_flag'):
        cell_segmentation.temp_flag = cle.create([1, 1, 1])

    cle.copy(input, cell_segmentation.temp_flip)

    for i in range(0, number_of_dilations):
        cle.onlyzero_overwrite_maximum_box(cell_segmentation.temp_flip, cell_segmentation.temp_flag, cell_segmentation.temp_flop)
        cle.onlyzero_overwrite_maximum_diamond(cell_segmentation.temp_flop, cell_segmentation.temp_flag, cell_segmentation.temp_flip)

    cle.greater_constant(cell_segmentation.temp_flip, output, constant=1)
    for i in range(0, number_of_erosions):
        cle.erode_box(output, cell_segmentation.temp_flop)
        cle.erode_box(cell_segmentation.temp_flop, output)

    cle.copy(output, cell_segmentation.temp_flop)
    cle.mask(cell_segmentation.temp_flip, cell_segmentation.temp_flop, output)

    print("cell segmentation took " + str(time.time() - start_time))
    return output



# push a first image to get something on the GPU to work with
gpu_input = cle.push_zyx(img_arr[0])

# allocated memory for subsequent steps
gpu_background_subtracted = cle.create(gpu_input)
gpu_spot_detection = cle.create(gpu_input)
gpu_cell_segmentation = cle.create(gpu_input)

# on demand, push a nother time point
delayed_pushed = bs.delayed_push(img_arr, gpu_input)
print(delayed_pushed)

# on demand, process it
delayed_background_subtracted = bs.delayed_operation(background_subtraction, source=delayed_pushed, target=gpu_background_subtracted)

delayed_spot_detected = bs.delayed_operation(spot_detection, source=delayed_background_subtracted, target=gpu_spot_detection)

delayed_cells_segmented = bs.delayed_operation(cell_segmentation, source=delayed_spot_detected, target=gpu_cell_segmentation)

# print(img_arr)

# Start up napari
import napari
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.add_image(img_arr, name='Tribolium', contrast_limits=[0, 1000], scale=voxel_size)


    #bs.delayed_operation(background_subtraction, {'input':gpu_input, 'output':gpu_background_subtracted})

    viewer.add_image(bs.delayed_pull(delayed_background_subtracted), name = "Background subtracted", contrast_limits=[0, 200], scale=voxel_size)

    viewer.add_image(bs.delayed_pull(delayed_spot_detected), name = "Detected spots", contrast_limits=[0, 1], scale=voxel_size)

    viewer.add_labels(bs.delayed_pull(delayed_cells_segmented), name = "Segmented cells", scale=voxel_size, multiscale=False)
