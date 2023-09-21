# IMPORT LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
import datetime

# CONFIGURATION
signal_length = 200
moving_average_window = 3
sample_interval = 3.28125 # Microseconds
keg_height = 445 # Millimeters
speed_of_sound = 1.5 # Millimeters per microsecond
min_index = 50 # Ringdown boundary index

# SAMPLE VALUES
sample_values = [1851,1959,2022,2043,2023,1970,1877,1755,1617,1478,1328,1181,1049,938,829,751,687,625,571,530,531,517,478,442,497,638,745,784,796,756,701,665,613,566,521,479,443,427,403,381,367,351,341,334,345,362,390,443,483,509,465,434,408,400,412,398,394,391,383,384,387,363,376,374,383,383,378,391,382,379,413,469,516,533,520,489,450,428,418,399,389,387,389,395,381,351,335,335,326,323,324,322,309,297,335,352,342,324,311,324,327,360,414,467,499,523,513,497,486,449,411,395,386,369,372,372,360,351,354,346,329,312,307,313,311,307,315,327,364,360,367,384,397,412,407,409,402,385,373,388,416,424,472,505,503,459,429,391,381,370,372,350,361,340,349,367,353,359,359,357,356,355,373,368,365,358,374,406,446,471,460,421,394,377,371,358,341,350,367,352,339,351,348,339,323,323,343,354,353,373,386,428,459,462,460,445,451,445,425,411]
sample_values2 = [2015,2158,2294,2380,2409,2396,2347,2268,2161,2029,1866,1667,1488,1343,1202,1082,979,886,833,755,711,697,654,642,645,799,912,986,999,1044,1120,1157,1184,1206,1209,1156,1135,1075,1050,1034,954,935,945,905,844,838,800,793,805,793,760,726,710,689,712,699,658,639,641,635,659,685,688,737,749,690,727,751,745,747,744,711,670,675,687,694,691,671,645,682,698,684,652,643,604,614,631,598,581,572,551,569,600,592,563,570,611,613,630,585,584,605,640,640,582,556,581,578,544,531,505,478,474,501,495,491,533,544,514,491,520,514,535,568,563,551,557,538,521,555,599,596,627,617,605,598,590,571,567,567,558,536,574,558,572,601,600,598,613,589,582,598,617,595,608,601,600,590,580,566,570,606,619,621,607,585,601,646,659,690,711,699,683,637,623,635,672,682,676,697,707,658,636,624,602,611,576,555,572,575,596,610,620,626,627,610,604,612,609,590]

# MOVING AVERAGE FUNCTION
def moving_avg_calc(input_array, window_size):
    i = 0
    moving_averages = []
    while i < len(input_array) - window_size + 1:
        window = input_array[i : i + window_size]
        window_average = round(sum(window) / window_size, 2)
        moving_averages.append(window_average)
        i += 1

    return moving_averages

# FIND NEXT PEAK
def find_next_peak(input_array, start_index):
    index = start_index
    max_val = input_array[start_index]
    for i in range(start_index+1, len(input_array)):
        if input_array[i] > max_val:
            max_val = input_array[i]
            index = i
        else:
            break
    return index

# FIND NEXT TROUGH
def find_next_trough(input_array, start_index):
    index = start_index
    min_val = input_array[start_index]
    for i in range(start_index+1, len(input_array)):
        if input_array[i] < min_val:
            min_val = input_array[i]
            index = i
        else:
            break
    return index

# PROCESS DATA
def find_peaks_and_troughs(input_array):
    moving_average = moving_avg_calc(input_array, moving_average_window)
    peaks = []
    troughs = []
    index = 0
    while index < signal_length - moving_average_window - 1:
        peaks.append(find_next_peak(moving_average, index))
        index = peaks[-1]+1
        if index < signal_length - moving_average_window - 1:
            troughs.append(find_next_trough(moving_average, index))
            index = troughs[-1]+1

    # FILL LEVEL CALCULATION
    index_difference = peaks[2] - peaks[0]
    tof = index_difference * sample_interval
    fill_level = round(100 * (tof * speed_of_sound) / (keg_height * 2), 1)
    print("Index Difference: ", index_difference)
    print("Time of Flight: ", tof)
    print("Fill level: ", fill_level)

    # MAX PEAK CALCULATION AFTER RINGDOWN
    for peak in peaks:
        if peak > min_index:
            max_peak = peak
            break
    for peak in peaks:
        if peak > min_index and moving_average[peak] > moving_average[max_peak]:
            max_peak = peak
    index_difference_max = max_peak - peaks[0]
    tof_max = index_difference_max * sample_interval
    fill_level_max = round(100 * (tof_max * speed_of_sound) / (keg_height * 2), 1)
    max_peak_gain = moving_average[max_peak]
    print("Index Difference (MAX): ", index_difference_max)
    print("Time of Flight (MAX): ", tof_max)
    print("Fill level (MAX): ", fill_level_max)    
    print("Peak Gain: ", max_peak_gain)

    #plt.figure()
    #plt.plot(input_array)
    #plt.plot(moving_average)
    ma = []
    for i in range(0,3):
        ma.append(moving_avg_calc(input_array, moving_average_window + (i*2)))
        #plt.plot(ma[i])
    '''
    plt.axvline(peaks[2],color='k')
    plt.annotate("Fill Level: " + str(fill_level) + "%", xy = (peaks[2], moving_average[peaks[2]]), xytext=(peaks[2] + 20, moving_average[peaks[2]]+500), arrowprops= dict(facecolor = 'black', shrink = 0.03),)
    for peak in peaks:
        plt.axvline(peak, color='y')
    if peaks[2] != max_peak:
        plt.axvline(max_peak,color='k')
        plt.annotate("Fill Level (MAX): " + str(fill_level_max) + "%", xy = (max_peak, moving_average[max_peak]), xytext=(max_peak + 20, moving_average[max_peak]+500), arrowprops= dict(facecolor = 'black', shrink = 0.03),)
    plt.show()
    '''

    ts = datetime.datetime.now().timestamp()

    return ts, index_difference_max, tof_max, fill_level_max, max_peak, max_peak_gain, input_array, moving_average

# AVERAGE OF PREVIOUS RESULTS
def average_samples(samples, range):
    sample_average = np.array(samples[-range:])
    print("Sample List Length = ", len(sample_average))
    sample_average = np.average(sample_average, axis=0)
    sample_average_analysis = find_peaks_and_troughs(sample_average)

    return sample_average_analysis

# find_peaks_and_troughs(sample_values)