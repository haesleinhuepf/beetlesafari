import napari

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    # attach the assistant
    import napari_pyclesperanto_assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    from beetlesafari import attach_clearcontrol_dock_widget
    attach_clearcontrol_dock_widget(assistant_gui)







