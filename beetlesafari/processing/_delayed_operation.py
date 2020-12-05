from typing import Callable

def _repetition_preventer1(operation, n, source, target):
    if operation in _repetition_preventer1.cache:
        cache = _repetition_preventer1.cache[operation]
        if (cache[0] == n):
            return cache[1]

    result = operation(source, target)
    _repetition_preventer1.cache[operation] = [n, result]
    return result

_repetition_preventer1.cache = {}



def _repetition_preventer2(operation, n, source1, source2, target):
    if operation in _repetition_preventer2.cache:
        cache = _repetition_preventer2.cache[operation]
        if (cache[0] == n):
            return cache[1]

    result = operation(source1, source2, target)
    _repetition_preventer2.cache[operation] = [n, result]
    return result

_repetition_preventer2.cache = {}


def delayed_unary_operation(operation : Callable, source, target):
    import dask
    import dask.array as da

    shape = source.shape[1:]
    length = source.shape[0]
    dtype = source.dtype

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(_repetition_preventer1)  # lazy reader
    lazy_arrays = [lazy_process_image(operation, n, source[n], target) for n in range(0, length)]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=shape, dtype=dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)

    # operation(**parameters)


def delayed_binary_operation(operation : Callable, source1, source2, target):
    import dask
    import dask.array as da

    shape = source1.shape[1:]
    length = source1.shape[0]
    dtype = source1.dtype

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(_repetition_preventer2)  # lazy reader
    lazy_arrays = [lazy_process_image(operation, n, source1[n], source2[n], target) for n in range(0, length)]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=shape, dtype=dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)

    # operation(**parameters)