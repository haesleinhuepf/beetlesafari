import numpy as np
import pyclesperanto_prototype as cle
import beetlesafari as bs


cc_dataset = bs.ClearControlDataset('C:/structure/data/2019-12-17-16-54-37-81-Lund_Tribolium_nGFP_TMR/')
output_dir = "C:/structure/temp/lund/"
#sigma_noise_removal = 2
#sigma_background_removal = 17
#spot_detection_threshold = 25
delta_time_in_seconds = bs.minutes_to_seconds(5)
start_time_in_seconds = bs.hours_to_seconds(0)
end_time_in_seconds = bs.hours_to_seconds(36)

table = {'time_in_s':[],
         'original_index':[],
         'index':[]}

for i, t in enumerate(np.arange(start_time_in_seconds, end_time_in_seconds, delta_time_in_seconds)):
    print("Analysing time point just after " + str(t) + " s")

    from beetlesafari import stopwatch

    stopwatch()
    index = cc_dataset.get_index_after_time(t)
    print("Time (h), index", bs.seconds_to_hours(t), index)
    image = cc_dataset.get_image(index)
    acquisition_time = cc_dataset.times_in_seconds[index]

    from skimage.io import imsave
    imsave(output_dir + "lund_i" + (str(i).zfill(6)) + "_oi_" + (str(index).zfill(6)) + ".tif", image)

    table['time_in_s'].append(acquisition_time)
    table['index'].append(i)
    table['original_index'].append(index)

import pandas as pd
pd.DataFrame(table).to_csv(output_dir + "metadata.csv")

