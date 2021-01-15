import pyclesperanto_prototype as cle

def cell_segmentation(input : cle.Image, output : cle.Image, number_of_dilations : int = 10, number_of_erosions : int = 6):
    if output is None:
        output = cle.create_like(input)

    # allocate temporary images
    temp_flip = cle.create(input)
    temp_flop = cle.create(input)
    temp_flag = cle.create([1, 1, 1])

    # extend labels until they touch
    cle.copy(input, temp_flip)
    for i in range(0, number_of_dilations):
        cle.onlyzero_overwrite_maximum_box(temp_flip, temp_flag, temp_flop)
        cle.onlyzero_overwrite_maximum_diamond(temp_flop, temp_flag, temp_flip)

    # shrink labels a bit again
    cle.greater_constant(temp_flip, output, constant=0)
    for i in range(0, number_of_erosions):
        cle.erode_box(output, temp_flop)
        cle.erode_box(temp_flop, output)

    # mask the extended labels with a mask made from the shrinked
    cle.copy(output, temp_flop)
    cle.mask(temp_flip, temp_flop, output)
    return output
