# Thanks to Ignacio Vazquez-Abrams https://stackoverflow.com/questions/2225564/get-a-filtered-list-of-files-in-a-directory
# Thanks to Talley Lambert https://github.com/tlambert03/napari-dask-example/blob/master/dask_napari.ipynb
import numpy as np

def imread_raw_folder(foldername : str, width : int = 1, height : int = 1, depth : int = 1, dtype = np.uint16):
    """Opens a folder of raw files lazyly (using dask.delayed)

    Parameters
    ----------
    foldername : str
        directory location or pattern for searching for files. E.g. '/path/to/files*.raw'
    width
    height
    depth
    dtype

    Returns
    -------
        dask stack of delayed numpy arrays representing the specified image file
    """
    import glob
    import dask
    import dask.array as da
    from ._imread_raw import imread_raw

    from os.path import isdir
    if isdir(foldername):
        foldername = foldername + "/*"

    image_filenames = glob.glob(foldername)

    number_of_files = len(image_filenames)

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(imread_raw)  # lazy reader
    lazy_arrays = [lazy_process_image(image_filenames[n], width, height, depth, dtype) for n in range(0, number_of_files)]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=(depth, height, width), dtype=dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)
