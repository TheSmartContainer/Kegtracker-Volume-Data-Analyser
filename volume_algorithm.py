# IMPORT LIBRARIES
import matplotlib.pyplot as plt

# CONFIGURATION
signal_length = 200
moving_average_window = 5
sample_frequency = 3.28125 # Microseconds
keg_height = 445 # Millimeters

sample_values2 = [1805,1940,2043,2093,2095,2057,1987,1892,1777,1643,1481,1328,1213,1095,985,892,802,759,696,644,612,566,527,511,487,527,655,772,827,897,995,1029,1047,1080,1051,1077,1068,1066,1097,1134,1140,1094,1039,967,977,992,990,1007,994,899,858,855,881,901,922,889,842,838,829,803,749,698,649,642,618,596,573,592,635,658,644,633,648,650,636,603,566,559,549,552,561,576,547,545,542,523,519,517,544,514,507,469,443,439,459,442,439,452,418,427,449,461,478,481,466,429,405,395,401,396,400,387,398,403,403,413,409,388,377,373,362,366,352,351,372,397,383,381,395,368,392,384,359,353,374,364,357,359,365,379,371,356,377,363,356,346,343,349,373,359,360,373,371,397,398,408,399,387,406,397,396,397,409,402,394,400,395,401,375,373,391,379,375,376,378,396,399,365,359,382,367,383,391,369,365,377,371,383,384,379,377,378,365,368,395,393,421,427,411,398]
sample_values = [2015,2158,2294,2380,2409,2396,2347,2268,2161,2029,1866,1667,1488,1343,1202,1082,979,886,833,755,711,697,654,642,645,799,912,986,999,1044,1120,1157,1184,1206,1209,1156,1135,1075,1050,1034,954,935,945,905,844,838,800,793,805,793,760,726,710,689,712,699,658,639,641,635,659,685,688,737,749,690,727,751,745,747,744,711,670,675,687,694,691,671,645,682,698,684,652,643,604,614,631,598,581,572,551,569,600,592,563,570,611,613,630,585,584,605,640,640,582,556,581,578,544,531,505,478,474,501,495,491,533,544,514,491,520,514,535,568,563,551,557,538,521,555,599,596,627,617,605,598,590,571,567,567,558,536,574,558,572,601,600,598,613,589,582,598,617,595,608,601,600,590,580,566,570,606,619,621,607,585,601,646,659,690,711,699,683,637,623,635,672,682,676,697,707,658,636,624,602,611,576,555,572,575,596,610,620,626,627,610,604,612,609,590]
vol_samples = []

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
    for i in range(start_index, len(input_array)):
        if input_array[i] > max_val:
            max_val = input_array[i]
            index = i
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

# ANALYSE SAMPLE DATA
plt.plot(sample_values) # Plot sample
moving_average = moving_avg_calc(sample_values)
plt.plot(moving_average) # Plot moving average
first_peak_index = find_next_peak(moving_average, 0)
plt.axvline(x=first_peak_index, color = 'k') # Plot first peak
first_trough_index = find_next_trough(moving_average, first_peak_index)
plt.axvline(x=first_trough_index, color = 'y') # Plot first trough
second_peak_index = find_next_peak(moving_average, first_trough_index)
plt.axvline(x=second_peak_index, color = 'k') # Plot second peak
second_trough_index = find_next_trough(moving_average, second_peak_index)
plt.axvline(x=second_trough_index, color = 'y') # Plot first trough
third_peak_index = find_next_peak(moving_average, second_trough_index)
plt.axvline(x=third_peak_index, color = 'g') # Plot second peak
plt.legend()
plt.show()

index_difference = third_peak_index - first_peak_index
print("Index Difference :", index_difference)
