import pyclesperanto_prototype as cle

def spot_detection(input : cle.Image, output : cle.Image, threshold : float = 50.0, radius=0):
    import time
    start_time = time.time()
    if output is None:
        output = cle.create_like(input)

    # permanently allocate temporary images
    if not hasattr(spot_detection, 'temp_flip'):
        spot_detection.temp_flip = cle.create(input)
    if not hasattr(spot_detection, 'temp_flop'):
        spot_detection.temp_flop = cle.create(input)

    # detect maxima
    cle.detect_maxima_box(input, spot_detection.temp_flop, radius_x=radius, radius_y=radius, radius_z=radius)

    # threshold
    cle.greater_constant(input, output, constant=threshold)

    # mask
    cle.binary_and(output, spot_detection.temp_flop, spot_detection.temp_flip)

    # label spots
    # cle.connected_components_labeling_box(spot_detection.temp_flip, output)

    cle.label_spots(spot_detection.temp_flip, output)

    number_of_spots = cle.maximum_of_all_pixels(output)
    print("Num spots: " + str(number_of_spots))

    print("spot detection took " + str(time.time() - start_time))
    return output
