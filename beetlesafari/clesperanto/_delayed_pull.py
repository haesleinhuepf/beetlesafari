import pyclesperanto_prototype as cle
import numpy as np
from pyclesperanto_prototype._tier0._pycl import OCLArray


def _pull(target : cle.Image):
    print("pull")
    import time
    start_time = time.time()
    result = cle.pull_zyx(target)
    print("push_copy took " + str(time.time() - start_time))

    return result

def delayed_pull(target):
    import dask
    import dask.array as da

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(_pull)  # lazy reader
    lazy_arrays = [lazy_process_image(target[n]) for n in range(0, target.shape[0])]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=target.shape[1:], dtype=target.dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)


