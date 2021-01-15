
import pyclesperanto_prototype as cle

def background_subtraction(input : cle.Image, output : cle.Image, sigma1=1, sigma2=5):
    if output is None:
        output = cle.create_like(input)

    output = cle.difference_of_gaussian(input, output, sigma1, sigma1, sigma1, sigma2, sigma2, sigma2)
    return output