from typing import Callable

def _repetition_preventer(operation, n, source, target):
    if operation in _repetition_preventer.cache:
        cache = _repetition_preventer.cache[operation]
        if (cache[0] == n):
            return cache[1]

    result = operation(source, target)
    _repetition_preventer.cache[operation] = [n, result]
    return result

_repetition_preventer.cache = {}

def delayed_operation(operation : Callable, source, target):
    import dask
    import dask.array as da

    shape = source.shape[1:]
    length = source.shape[0]
    dtype = source.dtype

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(_repetition_preventer)  # lazy reader
    lazy_arrays = [lazy_process_image(operation, n, source[n], target) for n in range(0, length)]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=shape, dtype=dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)

    # operation(**parameters)