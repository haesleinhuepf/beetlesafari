import pyclesperanto_prototype as cle

def membrane_estimation(cell_segmentation : cle.Image, membranes : cle.Image):
    import time
    start_time = time.time()

    if membranes is None:
        membranes = cle.create_like(cell_segmentation)

    membranes = cle.detect_label_edges(cell_segmentation, membranes)

    print("membranes took " + str(time.time() - start_time))

    return membranes