from typing import Callable

def delayed_operation(operation : Callable, parameters : dict, shape, length, dtype):
    import dask
    import dask.array as da

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(operation)  # lazy reader
    lazy_arrays = [lazy_process_image(**parameters) for n in range(0, length)]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=shape, dtype=dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)

    # operation(**parameters)