from datetime import time

from magicgui import magicgui
from ._clearcontrol_dataset import ClearControlDataset

@magicgui(
    auto_call=True,
    layout='vertical',
    hours={'minimum':0, 'maximum':1000},
    minutes={'minimum': 0, 'maximum': 1000000},
    seconds={'minimum': 0, 'maximum': 1000000},
)
def _clearcontrol_loader(directory : str = "C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR", dataset_name : str = 'C0opticsprefused', hours : int = 0, minutes : int = 0, seconds : int = 0, ):
    if directory is None:
        # we have to do it like this becasue the assistant hands over None at the first call
        directory = "C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR"

    cc_dataset : ClearControlDataset = ClearControlDataset(directory)

    index = cc_dataset.get_index_after_time(hours * 60 * 60 + minutes * 60 + seconds)
    print('Load index', index)
    output = cc_dataset.get_resampled_image(index)

    import pyclesperanto_prototype as cle

    min_intensity = 0
    max_intensity = cle.maximum_of_all_pixels(output)

    output = cle.pull_zyx(output)


    # show result in napari
    if (_clearcontrol_loader.initial_call):
        _clearcontrol_loader.self.viewer.add_image(output)
        _clearcontrol_loader.initial_call = False
    else:
        _clearcontrol_loader.self.layer.data = output
        _clearcontrol_loader.self.layer.name = "CCds" + str(index)
        _clearcontrol_loader.self.layer.contrast_limits = (min_intensity, max_intensity)


from napari_pyclesperanto_assistant import AssistantGUI

def attach_clearcontrol_dock_widget(assistant : AssistantGUI):

    assistant.add_button("ClearControl loader", _clearcontrol_loader)