import datetime

from magicgui import magicgui
from ._clearcontrol_dataset import ClearControlDataset
from napari_tools_menu import register_function
import napari

@register_function(menu="File Import/Export > Load ClearControl dataset (beetlesafari)")
def _clearcontrol_loader(directory : str = "C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR", dataset_name : str = 'C0opticsprefused', hours : int = 0, minutes : int = 0, seconds : int = 0) -> napari.types.ImageData:
    import time
    start_time = time.time()

    if directory is None:
        # we have to do it like this because the assistant hands over None at the first call
        directory = "C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR"

    cc_dataset : ClearControlDataset = ClearControlDataset(directory)

    #hours = timepoint.hour
    #minutes = timepoint.minute
    #seconds = timepoint.second

    index = cc_dataset.get_index_after_time(hours * 60 * 60 + minutes * 60 + seconds)
    filename = cc_dataset.get_image_filename(index)
    print('Load index', index)
    output = cc_dataset.get_resampled_image(index)

    import pyclesperanto_prototype as cle

    min_intensity = 0
    max_intensity = cle.maximum_of_all_pixels(output)

    output = cle.pull(output)
    print("Loading took " + str(time.time() - start_time) + " s")

    # show result in napari
    return output

from napari_pyclesperanto_assistant import Assistant

def attach_clearcontrol_dock_widget(assistant : Assistant):

    assistant.add_button("ClearControl loader", _clearcontrol_loader)
