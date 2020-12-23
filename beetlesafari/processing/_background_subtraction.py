
import pyclesperanto_prototype as cle

def background_subtraction(input : cle.Image, output : cle.Image, sigma1=1, sigma2=5):
    import time
    start_time = time.time()
    if output is None:
        output = cle.create_like(input)

    #cle.top_hat_sphere(input, output, radius_x, radius_y, radius_z)
    output = cle.difference_of_gaussian(input, output, sigma1, sigma1, sigma1, sigma2, sigma2, sigma2)
    print("subtract background took " + str(time.time() - start_time))
    return output