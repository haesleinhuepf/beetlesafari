import pyclesperanto_prototype as cle

def cell_segmentation(input : cle.Image, output : cle.Image, number_of_dilations : int = 10, number_of_erosions : int = 6):
    import time
    start_time = time.time()
    if output is None:
        output = cle.create_like(input)

    # permanently allocate temporary images
    if not hasattr(cell_segmentation, 'temp_flip'):
        cell_segmentation.temp_flip = cle.create(input)
    if not hasattr(cell_segmentation, 'temp_flop'):
        cell_segmentation.temp_flop = cle.create(input)
    if not hasattr(cell_segmentation, 'temp_flag'):
        cell_segmentation.temp_flag = cle.create([1, 1, 1])

    # extend labels until they touch
    cle.copy(input, cell_segmentation.temp_flip)
    for i in range(0, number_of_dilations):
        cle.onlyzero_overwrite_maximum_box(cell_segmentation.temp_flip, cell_segmentation.temp_flag, cell_segmentation.temp_flop)
        cle.onlyzero_overwrite_maximum_diamond(cell_segmentation.temp_flop, cell_segmentation.temp_flag, cell_segmentation.temp_flip)

    # shrink labels a bit again
    cle.greater_constant(cell_segmentation.temp_flip, output, constant=0)
    for i in range(0, number_of_erosions):
        cle.erode_box(output, cell_segmentation.temp_flop)
        cle.erode_box(cell_segmentation.temp_flop, output)

    # mask the extended labels with a mask made from the shrinked
    cle.copy(output, cell_segmentation.temp_flop)
    cle.mask(cell_segmentation.temp_flip, cell_segmentation.temp_flop, output)

    print("cell segmentation took " + str(time.time() - start_time))
    return output
