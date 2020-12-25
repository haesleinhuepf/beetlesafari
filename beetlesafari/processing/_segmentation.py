def segmentation(image):
    import pyclesperanto_prototype as cle
    from ._background_subtraction import background_subtraction
    from ._spot_detection import spot_detection
    from ._cell_segmentation import cell_segmentation

    background_subtracted = None
    background_subtracted = background_subtraction(image, background_subtracted, 2, 7)
    # show(background_subtracted, title="background subtracted", use_napari=True)

    spots = cle.create_like(background_subtracted)
    spots = spot_detection(background_subtracted, spots, threshold=10)
    # show(spots, title="spots", use_napari=True)

    # temporary workaround; see https://github.com/clEsperanto/pyclesperanto_prototype/issues/63
    new_spots = cle.create_like(spots)
    cle.close_index_gaps_in_label_map(spots, new_spots)
    spots = new_spots
    print("corrected number of spots", cle.maximum_of_all_pixels(spots))

    cells = cle.create_like(spots)
    cells = cell_segmentation(spots, cells, number_of_dilations=14, number_of_erosions=8)

    #show(cells, title="cells", use_napari=True, labels=True)

    print("number of cells", cle.maximum_of_all_pixels(cells))

    # temporary workaround; see https://github.com/clEsperanto/pyclesperanto_prototype/issues/63
    new_cells = cle.create_like(cells)
    cle.close_index_gaps_in_label_map(cells, new_cells)
    cells = new_cells
    print("corrected number of cells", cle.maximum_of_all_pixels(cells))

    return cells

