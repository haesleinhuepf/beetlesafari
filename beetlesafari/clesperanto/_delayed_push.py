import pyclesperanto_prototype as cle
import numpy as np
from pyclesperanto_prototype._tier0._pycl import OCLArray


def _push_copy(image : np.ndarray, target : cle.Image):
    print("push")
    import time
    start_time = time.time()
    pushed = cle.push_zyx(image)
    cle.copy(pushed, target)

    print("push_copy took " + str(time.time() - start_time))

    #target.write_array(image)
    return target

def delayed_push(image : np.ndarray, target : cle.Image):
    import dask
    import dask.array as da

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(_push_copy)  # lazy reader
    lazy_arrays = [lazy_process_image(image[n], target) for n in range(0, image.shape[0])]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=target.shape, dtype=target.dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)


