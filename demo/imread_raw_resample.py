import numpy as np

filename = 'C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/stacks/C0opticsprefused/000000.raw'
width = 512
height = 1024
depth = 71
voxel_size = [3, 0.6934, 0.6934]

#image = np.empty((71, 1024, 512), np.uint16)

import beetlesafari as bs

img_arr = bs.imread_raw(filename, width, height, depth)

import pyclesperanto_prototype as cle

print("Shape before resampling: " + str(img_arr.shape))

buffer = cle.push_zyx(img_arr)
resampled = cle.resample(buffer, factor_x = voxel_size[2], factor_y = voxel_size[1], factor_z = voxel_size[0])
img_arr = cle.pull_zyx(resampled)

print("Shape after resampling: " + str(img_arr.shape))

# print(img_arr)

# Start up napari
import napari
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.add_image(img_arr, name='Tribolium')

