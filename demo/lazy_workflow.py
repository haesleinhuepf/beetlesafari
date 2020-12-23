foldername = 'C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/stacks/C0opticsprefused'
width = 512
height = 1024
depth = 71
voxel_size = [3, 0.6934, 0.6934]
zoom = 0.8
scaling_factor = [voxel_size[0] * zoom, voxel_size[1] * zoom, voxel_size[2] * zoom]

import beetlesafari as bs
from functools import lru_cache

# lazy loading
img_arr = bs.imread_raw_folder(foldername  + "/001*0.raw", width, height, depth)

# init GPU
import pyclesperanto_prototype as cle

# print out CL Info to see available devices
print(cle.cl_info())

# select a good default device
cle.select_device("TX")

# print out chosen device
print(cle.get_device())









# push a first image to get something on the GPU to work with
gpu_input = cle.push_zyx(img_arr[0])
resampled = cle.resample(gpu_input, factor_x = scaling_factor[2], factor_y = scaling_factor[1], factor_z = scaling_factor[0])


# allocate memory for subsequent steps
gpu_background_subtracted = cle.create(resampled)
gpu_spot_detection = cle.create(resampled)
gpu_cell_segmentation = cle.create(resampled)
gpu_membranes = cle.create(resampled)
gpu_mesh = cle.create(resampled)

# on demand, push a nother time point
delayed_pushed = bs.delayed_push(img_arr, resampled, zoom = scaling_factor)
print(delayed_pushed)

from beetlesafari import background_subtraction, spot_detection, cell_segmentation, membrane_estimation, draw_mesh

# on demand, process it
delayed_background_subtracted = bs.delayed_unary_operation(background_subtraction, source=delayed_pushed, target=gpu_background_subtracted)

delayed_spot_detected = bs.delayed_unary_operation(spot_detection, source=delayed_background_subtracted, target=gpu_spot_detection)

delayed_cells_segmented = bs.delayed_unary_operation(cell_segmentation, source=delayed_spot_detected, target=gpu_cell_segmentation)

delayed_membranes = bs.delayed_unary_operation(membrane_estimation, source=delayed_cells_segmented, target=gpu_membranes)

delayed_mesh = bs.delayed_binary_operation(draw_mesh, delayed_spot_detected, delayed_cells_segmented, gpu_mesh)

# print(img_arr)



# Start up napari
import napari
with napari.gui_qt():
    viewer = napari.Viewer(ndisplay=3, order=[0,2,1], title='napari on beetle safari')


    viewer.add_image(bs.delayed_pull(delayed_pushed), name='Tribolium', contrast_limits=[0, 1000], blending='additive', visible=False)

    #bs.delayed_operation(background_subtraction, {'input':gpu_input, 'output':gpu_background_subtracted})

    viewer.add_image(bs.delayed_pull(delayed_background_subtracted), name = "Background subtracted", contrast_limits=[0, 400], blending='additive', colormap='magenta')

    viewer.add_image(bs.delayed_pull(delayed_spot_detected), name = "Detected spots", contrast_limits=[0, 1], blending='additive', colormap='yellow')

    viewer.add_labels(bs.delayed_pull(delayed_cells_segmented), name = "Segmented cells", visible=False)

    viewer.add_image(bs.delayed_pull(delayed_membranes), name = "Estimated membranes", visible=True, rendering='average', contrast_limits=[0, 0.001], blending='additive', colormap='cyan')

    viewer.add_image(bs.delayed_pull(delayed_mesh), name = "Mesh", contrast_limits=[0, 50], blending='additive', colormap='green')

    viewer.window.qt_viewer.camera.zoom = 1
