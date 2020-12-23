foldername = 'C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/stacks/C0opticsprefused'
width = 512
height = 1024
depth = 71
voxel_size = [3, 0.6934, 0.6934]

# init GPU
import pyclesperanto_prototype as cle

# print out CL Info to see available devices
#print(cle.cl_info())

# select a good default device
cle.select_device("TX")

# print out chosen device
print(cle.get_device())


class Navigator:
    def __init__(self, viewer, image_data, voxel_size):
        self.timepoint = 0
        self._drawn_timepoint = -1
        self.viewer = viewer
        self.image_data = image_data
        self.voxel_size = voxel_size

        self.gpu_resampled = None
        self.gpu_background_subtracted = None
        self.gpu_spots = None
        self.gpu_cells = None
        self.gpu_membranes = None
        self.gpu_mesh = None

        self.viewer.add_image(self._fake_image(self.image_data.shape[0]), contrast_limits=[0, 1], visible=True, scale=[50, 50, 50], blending='additive')
        #self.viewer.add_image(self.image_data, contrast_limits=[0, 1], visible=True, scale=voxel_size, blending='additive')

    def recompute(self):
        input_image = self.image_data[self.timepoint]

        import pyclesperanto_prototype as cle

        if self._drawn_timepoint != self.timepoint:
            self._drawn_timepoint = self.timepoint

            pushed = cle.push_zyx(input_image)

            self.gpu_resampled = cle.resample(pushed, self.gpu_resampled, factor_x=self.voxel_size[2], factor_y=self.voxel_size[1], factor_z=self.voxel_size[0])

            import beetlesafari as bs
            self.gpu_background_subtracted = bs.background_subtraction(self.gpu_resampled, self.gpu_background_subtracted)
            self.gpu_spots = bs.spot_detection(self.gpu_background_subtracted, self.gpu_spots)
            self.gpu_cells = bs.cell_segmentation(self.gpu_spots, self.gpu_cells)
            self.gpu_membranes = bs.membrane_estimation(self.gpu_cells, self.gpu_membranes)
            self.gpu_mesh = bs.draw_mesh(self.gpu_spots, self.gpu_cells, self.gpu_mesh)

            import time
            start_time = time.time()

            result =  [self.timepoint,
                       {
                        'resampled':            {'data':self.gpu_resampled, 'blending':'additive', 'contrast_limits':[0, 1000], 'visible':False},
                        'background subtracted':{'data':self.gpu_background_subtracted, 'blending':'additive', 'contrast_limits':[0, 400], 'colormap':'magenta'},
                        'spots':                {'data':self.gpu_spots, 'blending':'additive', 'contrast_limits':[0, 1], 'colormap':'yellow'},
                        # 'cells':              {'data':self.gpu_cells, 'blending':'additive', 'contrast_limits':[0, 1], 'rendering':'average'},
                        'membranes':            {'data':self.gpu_membranes, 'blending':'additive', 'contrast_limits':[0, 0.01], 'rendering':'average', 'colormap':'cyan'},

                        'mesh':                 {'data':self.gpu_mesh, 'blending':'additive', 'contrast_limits':[0, 50], 'colormap':'green'},
                      }
                   ]

            print("pulling took " + str(time.time() - start_time))
        else:
            result = None

        return result

    def _fake_image(self, number_of_timepoints):
        shape = [10, 10, 10]
        dtype = float
        length = number_of_timepoints

        import dask
        import dask.array as da

        # create dask stack of lazy image readers
        lazy_process_image = dask.delayed(self.change_timepoint, pure=False, traverse=False)  # lazy reader
        lazy_arrays = [lazy_process_image(n) for n in range(0, length)]
        dask_arrays = [
            da.from_delayed(lazy_array, shape=shape, dtype=dtype)
            for lazy_array in lazy_arrays
        ]

        # Stack into one large dask.array
        result = da.stack(dask_arrays, axis=0)
        print(result)

        return result

    def change_timepoint(self, n):
        self.timepoint = n
        import numpy as np

        return np.zeros([10, 10, 10])

    # Multi-threaded interaction
    # inspired by https://napari.org/docs/dev/events/threading.html
    def update_layer(self, data):
        if data is None:
            return

        timepoint, images = data

        #if (self._drawn_timepoint == timepoint):
        #    return

        #self._drawn_timepoint = timepoint

        print("updt " + str(timepoint))

        for name in images.keys():
            kwargs = images[name]

            try:
                self.viewer.layers[name].data = kwargs['data']
            except KeyError:
                self.viewer.add_image(
                    name=name, **kwargs
                )





# lazy loading
import beetlesafari as bs
img_arr = bs.imread_raw_folder(foldername, width, height, depth)

# star viewer
import time
import napari
from napari.qt.threading import thread_worker
with napari.gui_qt():

    viewer = napari.Viewer(ndisplay=3, order=[0, 2, 1], title='napari on beetle safari')

    navigator = Navigator(viewer, img_arr, voxel_size)



    @thread_worker
    def yield_random_images_forever():
        while True:  # infinite loop!

            data = navigator.recompute()

            yield data

            time.sleep(0.1)

    # Start the game loop
    worker = yield_random_images_forever()
    worker.yielded.connect(navigator.update_layer)
    worker.start()