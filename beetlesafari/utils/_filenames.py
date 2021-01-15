def index_to_clearcontrol_filename(index : int ):
    return ("000000" + str(index))[-6:] + ".raw"
