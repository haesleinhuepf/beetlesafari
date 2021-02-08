import datetime

from magicgui import magicgui
from ._clearcontrol_dataset import ClearControlDataset

@magicgui(
    auto_call=True,
    layout='vertical',
)
def _clearcontrol_loader(directory : str = "C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR", dataset_name : str = 'C0opticsprefused', hours : int = 0, minutes : int = 0, seconds : int = 0):
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
    start_time = time.time()
    if (_clearcontrol_loader.call_count == 0):
        _clearcontrol_loader.self.viewer.add_image(output)
    else:
        _clearcontrol_loader.self.layer.data = output
        _clearcontrol_loader.self.layer.name = "CCds" + str(index)
        _clearcontrol_loader.self.layer.contrast_limits = (min_intensity, max_intensity)
        _clearcontrol_loader.self.layer.metadata['filename'] = filename
    print("Interop took " + str(time.time() - start_time) + " s")


from napari_pyclesperanto_assistant import Assistant

def attach_clearcontrol_dock_widget(assistant : Assistant):

    assistant.add_button("ClearControl loader", _clearcontrol_loader)
