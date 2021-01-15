def feature_vectors(input : dict, key_selection : list = None):
    if key_selection is None:
        key_selection = input.keys()

    output = []
    for key in key_selection:
        output.append(input[key])

    import numpy as np
    data = np.asarray(output).T
    print(data.shape)
    return data

def neighborized_feature_vectors(
        input : dict,
        neighborhoods : list,
        key_selection : list = None,

):
    import pyclesperanto_prototype as cle
    import numpy as np

    if key_selection is None:
        key_selection = input.keys()

    output = []

    neighborized_element = None
    for key in key_selection:
        #print("key", key)
        element = input[key]

        output.append(element)

        element = cle.push_zyx(np.asarray([element]))

        for neighborhood in neighborhoods:
            #print("n")
            #neighborized_element = cle.mode_of_touching_neighbors(element, neighborhood, neighborized_element)
            #output.append(cle.pull_zyx(neighborized_element)[0])

            neighborized_element = cle.median_of_touching_neighbors(element, neighborhood, neighborized_element)
            output.append(cle.pull_zyx(neighborized_element)[0])

            neighborized_element = cle.standard_deviation_of_touching_neighbors(element, neighborhood, neighborized_element)
            output.append(cle.pull_zyx(neighborized_element)[0])

            neighborized_element = cle.mean_of_touching_neighbors(element, neighborhood, neighborized_element)
            output.append(cle.pull_zyx(neighborized_element)[0])

            #neighborized_element = cle.minimum_of_touching_neighbors(element, neighborhood, neighborized_element)
            #output.append(cle.pull_zyx(neighborized_element)[0])

            #neighborized_element = cle.maximum_of_touching_neighbors(element, neighborhood, neighborized_element)
            #output.append(cle.pull_zyx(neighborized_element)[0])

    import numpy as np
    data = np.asarray(output).T

    return data
