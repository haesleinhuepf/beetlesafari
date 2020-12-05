
# Helper function for reading ImageJs ZIP file examples
# Thanks to Talley Lambert
# https://forum.image.sc/t/open-imagej-example-zip-images-with-scikit-image-and-friends/45001
import requests
import zipfile
from io import BytesIO
from tifffile import imread

def imread_zip(url : str):
    """Reads an image as numpy arrays representing a tif in a remote zip file.

    Parameters
    ----------
    url

    Returns
    -------
    """

    response = requests.get(url)
    response.raise_for_status()
    with zipfile.ZipFile(BytesIO(response.content)) as zf:
        for path in zf.filelist:
            with zf.open(path, "r") as f:
                # f is a file-like object of type zipfile.ZipExtFile
                # replace imread with any file-reader of your choice
                # that accepts a file-like object as input
                return imread(f)