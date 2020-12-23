import pyclesperanto_prototype as cle

def draw_mesh(spots : cle.Image, cells : cle.Image, mesh : cle.Image):
    import time
    start_time = time.time()
    if mesh is None:
        mesh = cle.create_like(spots)

    gpu_pointlist = cle.labelled_spots_to_pointlist(spots)

    gpu_distance_matrix = cle.generate_distance_matrix(gpu_pointlist, gpu_pointlist)

    gpu_touch_matrix = cle.generate_touch_matrix(cells)

    # touch matrix:
    # set the first column to zero to ignore all spots touching the background (background label 0, first column)
    cle.set_column(gpu_touch_matrix, 0, 0)

    gpu_touch_matrix_with_distances = cle.multiply_images(gpu_touch_matrix, gpu_distance_matrix)

    cle.set(mesh, 0)
    cle.touch_matrix_to_mesh(gpu_pointlist, gpu_touch_matrix_with_distances, mesh)

    print("mesh took " + str(time.time() - start_time))

    return mesh