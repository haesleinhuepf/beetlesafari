foldername = 'C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/stacks/C0opticsprefused'
width = 512
height = 1024
depth = 71

import beetlesafari as bs

img_arr = bs.imread_raw_folder(foldername + "/000*00.raw", width, height, depth)

import pyclesperanto_prototype as cle
print(cle.cl_info())

cle.select_device("RTX")
print(cle.get_device())

def background_subtraction(input, output : cle.Image, radius_x : int = 10, radius_y : int = 10, radius_z = 0):
    print("subtract background")
    import time
    start_time = time.time()
    cle.top_hat_sphere(input, output, radius_x, radius_y, radius_z)
    print("sub back took " + str(time.time() - start_time))
    return output


# push a first image to get something on the GPU to work with
gpu_input = cle.push_zyx(img_arr[0])

# allocated memory for subsequent steps
gpu_background_subtracted = cle.create(gpu_input)

# on demand, push a nother time point
delayed_pushed = bs.delayed_push(img_arr, gpu_input)
print(delayed_pushed)

# on demand, process it
delayed_background_subtracted = bs.delayed_operation(background_subtraction, {'input':gpu_input, 'output':gpu_background_subtracted}, shape=gpu_input.shape, length=img_arr.shape[0], dtype=float)
print(delayed_background_subtracted)


# print(img_arr)

# Start up napari
import napari
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.add_image(bs.delayed_pull(delayed_pushed), name='Tribolium')


    #bs.delayed_operation(background_subtraction, {'input':gpu_input, 'output':gpu_background_subtracted})

    viewer.add_image(bs.delayed_pull(delayed_background_subtracted), name = "Background subtracted")
