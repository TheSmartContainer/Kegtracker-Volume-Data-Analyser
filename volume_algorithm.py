# IMPORT LIBRARIES
import matplotlib.pyplot as plt

# CONFIGURATION
signal_length = 200
moving_average_window = 5
sample_interval = 3.28125 # Microseconds
keg_height = 445 # Millimeters
speed_of_sound = 1.5 # Millimeters per microsecond

# SAMPLE VALUES
sample_values = [2015,2158,2294,2380,2409,2396,2347,2268,2161,2029,1866,1667,1488,1343,1202,1082,979,886,833,755,711,697,654,642,645,799,912,986,999,1044,1120,1157,1184,1206,1209,1156,1135,1075,1050,1034,954,935,945,905,844,838,800,793,805,793,760,726,710,689,712,699,658,639,641,635,659,685,688,737,749,690,727,751,745,747,744,711,670,675,687,694,691,671,645,682,698,684,652,643,604,614,631,598,581,572,551,569,600,592,563,570,611,613,630,585,584,605,640,640,582,556,581,578,544,531,505,478,474,501,495,491,533,544,514,491,520,514,535,568,563,551,557,538,521,555,599,596,627,617,605,598,590,571,567,567,558,536,574,558,572,601,600,598,613,589,582,598,617,595,608,601,600,590,580,566,570,606,619,621,607,585,601,646,659,690,711,699,683,637,623,635,672,682,676,697,707,658,636,624,602,611,576,555,572,575,596,610,620,626,627,610,604,612,609,590]

# MOVING AVERAGE FUNCTION
def moving_avg_calc(input_array):
    i = 0
    window_size = moving_average_window
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
    moving_average = moving_avg_calc(input_array)
    peaks = []
    troughs = []
    index = 0
    while index < signal_length - moving_average_window:
        peaks.append(find_next_peak(moving_average, index))
        print(peaks[-1])
        index = peaks[-1]
        troughs.append(find_next_trough(moving_average, index))
        print(troughs[-1])
        if peaks[-1] == troughs[-1]:
            break
        index = troughs[-1]

    index_difference = peaks[2] - peaks[0]
    tof = index_difference * sample_interval
    fill_level = round(100 * (tof * speed_of_sound) / (keg_height * 2), 1)
    print("Index Difference: ", index_difference)
    print("Time of Flight: ", tof)
    print("Fill level: ", fill_level)

    plt.figure()
    plt.plot(input_array)
    plt.plot(moving_average)
    plt.axvline(peaks[2],color='k')
    plt.annotate("Fill Level: " + str(fill_level) + "%", xy = (peaks[2], moving_average[peaks[2]]), xytext=(peaks[2] + 20, moving_average[peaks[2]]+500), arrowprops= dict(facecolor = 'black', shrink = 0.03),)
    plt.show()