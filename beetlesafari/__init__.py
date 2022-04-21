from .io import *
from .utils import *

__version__ = "0.3.2"

from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_experimental_provide_dock_widget():

    return [attach_clearcontrol_dock_widget]