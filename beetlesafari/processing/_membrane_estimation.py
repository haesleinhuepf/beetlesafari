import pyclesperanto_prototype as cle

def membrane_estimation(cell_segmentation : cle.Image, membranes : cle.Image):

    if membranes is None:
        membranes = cle.create_like(cell_segmentation)

    membranes = cle.detect_label_edges(cell_segmentation, membranes)

    return membranes