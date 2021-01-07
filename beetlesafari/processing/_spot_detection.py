import pyclesperanto_prototype as cle

def spot_detection(input : cle.Image, output : cle.Image, threshold : float = 50.0, radius=0):
    if output is None:
        output = cle.create_like(input)

    # allocate temporary images
    temp_flip = cle.create(input)
    temp_flop = cle.create(input)

    # detect maxima
    cle.detect_maxima_box(input, temp_flop, radius_x=radius, radius_y=radius, radius_z=radius)

    # threshold
    cle.greater_constant(input, output, constant=threshold)

    # mask
    cle.binary_and(output, temp_flop, temp_flip)

    # label spots
    cle.label_spots(temp_flip, output)

    return output
