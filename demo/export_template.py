import numpy as np
import pyclesperanto_prototype as cle
import beetlesafari as bs

# specify the location of the raw input data
cc_dataset = bs.ClearControlDataset('D:/IMAGING/archive_data_good/2020-02-06-16-10-18-21-Montafon_Tribolium_nGFP_TMR/')

# specify the location where the resulting TIF images should be stored
output_dir = "C:/structure/temp/montafon/"

# specify from which timepoint to which timepoint and in what interval data should be exported; in seconds
start_time_in_seconds = bs.hours_to_seconds(7)
end_time_in_seconds = bs.hours_to_seconds(16)
delta_time_in_seconds = bs.minutes_to_seconds(10)

# ---------------------------------- Do not change anything below ------------------------------------------------------
table = {'time_in_s':[],
         'original_index':[],
         'index':[]}

for i, t in enumerate(np.arange(start_time_in_seconds, end_time_in_seconds, delta_time_in_seconds)):
    print("Analysing time point just after " + str(t) + " s")

    from beetlesafari import stopwatch

    stopwatch()

    # find the index of the dataset after a given time
    index = cc_dataset.get_index_after_time(t)
    print("Time (h), index", bs.seconds_to_hours(t), index)

    # retrieve image from that time
    image = cc_dataset.get_image(index)
    acquisition_time = cc_dataset.times_in_seconds[index]

    # save image
    from skimage.io import imsave
    imsave(output_dir + "lund_i" + (str(i).zfill(6)) + "_oi_" + (str(index).zfill(6)) + ".tif", image)

    # save time of the dataset to the metadata table
    table['time_in_s'].append(acquisition_time)
    table['index'].append(i)
    table['original_index'].append(index)

# save metadata into same folder
import pandas as pd
pd.DataFrame(table).to_csv(output_dir + "metadata.csv")

