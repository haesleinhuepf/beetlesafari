# thanks to max9111, https://stackoverflow.com/questions/41651998/python-read-and-convert-raw-3d-image-file
import numpy as np

def imread_raw(filename : str, width : int = 1, height : int = 1, depth : int = 1, dtype = np.uint16):
    """Loads a raw image file (3D) with given dimensions from disk

    Parameters
    ----------
    filename
    width
    height
    depth
    dtype

    Returns
    -------
        numpy array with given dimensions containing pixels from specified file
    """

    f = open(filename, 'rb')  # only opens the file for reading
    img_arr = np.fromfile(f, dtype=dtype)
    img_arr = img_arr.reshape(depth, height, width)
    f.close()
    return img_arr