import napari

# create Qt GUI context
with napari.gui_qt():
    # start napari
    viewer = napari.Viewer()

    # attach the assistant
    import napari_pyclesperanto_assistant
    assistant_gui = napari_pyclesperanto_assistant.napari_plugin(viewer)

    import beetlesafari as bs
    bs.attach_clearcontrol_dock_widget(assistant_gui)
    bs.attach_crop_dock_widget(assistant_gui)
    bs.attach_segmentation_dock_widget(assistant_gui)
    bs.attach_clustering_dock_widget(assistant_gui)






