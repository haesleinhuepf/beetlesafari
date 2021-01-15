
from magicgui import magicgui
from napari.layers import Image
from napari_pyclesperanto_assistant import AssistantGUI
import pyclesperanto_prototype as cle

@magicgui(
    auto_call=True,
    layout='vertical',
    start_x={'minimum': 0, 'maximum': 4096},
    start_y={'minimum': 0, 'maximum': 4096},
    start_z={'minimum': 0, 'maximum': 4096},
    width={'minimum': 1, 'maximum': 4096},
    height={'minimum': 1, 'maximum': 4096},
    depth={'minimum': 1, 'maximum': 4096},
)
def _crop(input1: Image, start_x : int = 0, start_y:int = 0, start_z: int = 0, width:int = 100, height:int = 100, depth:int = 100):
    if input1:
        print("crop")
        # execute operation
        cle_input = cle.push_zyx(input1.data)

        output = cle.create([depth, height, width])
        cle.crop(cle_input, output,
                 start_x=start_x,
                 start_y=start_y,
                 start_z=start_z,
                 width=width,
                 height=height,
                 depth=depth
        )
        max_intensity = cle.maximum_of_all_pixels(output)
        if max_intensity == 0:
            max_intensity = 1 # prevent division by zero in vispy
        output = cle.pull_zyx(output)

        # show result in napari
        if (_crop.initial_call):
            _crop.self.viewer.add_image(output, colormap=input1.colormap)
            _crop.initial_call = False
        else:
            _crop.self.layer.data = output
            _crop.self.layer.name = "Result of crop"
            _crop.self.layer.contrast_limits=(0, max_intensity)
            _crop.self.layer.translate = (start_z, start_y, start_x)



def attach_crop_dock_widget(assistant: AssistantGUI):
    assistant.add_button("Crop", _crop)
