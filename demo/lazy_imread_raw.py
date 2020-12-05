foldername = 'C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/stacks/C0opticsprefused'
width = 512
height = 1024
depth = 71

import beetlesafari as bs

img_arr = bs.imread_raw_folder(foldername, width, height, depth)

# print(img_arr)

# Start up napari
import napari
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.add_image(img_arr, name='Tribolium')
