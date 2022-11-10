import pandas as pd
import datetime
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from DATA_LOADER.data_loader import DataReader

### Load data for one patient
# change path 
# one dataset for each patient
# ohio = DataReader(name='ohio', filepath='streamlit_introduction/DATA_LOADER/ohio_data/').read_data()
#linux directory : '~/streamlit_introduction/DATA_LOADER/ohio_data/'
ohio = DataReader(name='ohio', filepath='DATA_LOADER/ohio_data/').read_data() #new directory 
### it is a good idea to routinely check all analisys with other patients
patient_number = 2 # it can be from 1 to 11
df = ohio[patient_number].copy(True)

#NOTE: see paper in this folder for columns' meaning

"""
- measurement error
- lag with respect to real values (5' to 30')
- [40,400]
- less accurate data around big gaps(hours) of nan values
- data less accurate on the higher range
"""

# resampling
### aligning or summary
# see resampling pandas
df = df.resample('5min').mean()

# for this analysis i keep only the glucose values
df = pd.DataFrame(df[['glucose']])

# defining target threshold 
lb = 70
ub = 180

### data management
# one way to manage this data
def get_day(df, hypo_night_night_end = '08:00:00'):
    """
    df: a dataframe containing one column for glucose values
        and with a datetime index
    hypo_night_night_end: timestamp of the END of the 24 hour
                        period that i want for each day
    
    Returns a Generator of pd:Series (288,), every series is a 
                    different day
    """
    # list all unique dates
    udt:list[datetime.date] = list(set(df.index.to_series().dt.date.values))
    udt.sort()

    for i in range(1, len(udt)-1 -1):
        # the 1 and the second -1 are thre because the sereis
        # of the first and last dates could contains nan

        day_start = pd.Timestamp(udt[i]) + pd.Timedelta(hypo_night_night_end)
        day_end = pd.Timestamp(udt[i + 1]) + pd.Timedelta(hypo_night_night_end)

        dday = df.loc[day_start:day_end,:] # df containing 289 ROWS of almost a single day*
        dday = dday.iloc[:-1] # df containing 288 ROWS of a single day*

        yield pd.Series(dday.glucose.values,
                        index=pd.date_range(day_start, day_end, freq='5min')[:-1])

# alternatively i can create a date object containing all days for easier inspection
day_obj = list(get_day(df))
# get a single day
day_number = 4
day_obj[day_number]

# or i can work with the whole series 
df

### finding peaks, lows and visualizations

# one basic option to visualize the data 
for i, day in enumerate(get_day(df)):
    plt.cla()
    plt.plot(day)
    plt.savefig('new_plots/' + f'day_{i}.jpg')

# # some more plots with peaks identification 
# for i, day in enumerate(get_day(df)):
#     day = day.reset_index(drop=True)
#     peaks, _ = find_peaks(day, height=ub, prominence=1, width=6,distance=15)#Ali(added the distance argument)
#     plt.plot(day)
#     plt.plot(peaks, day[peaks], "x")
#     plt.plot([180]*len(day), "--", color="gray")
#     plt.savefig('new_plots/' + f'day_{i}.jpg')
#     plt.cla()

# # same thing for finding lows
# for i, day in enumerate(get_day(df)):
#     day = day.reset_index(drop=True)
#     # FIXED: add .dropna() to day in max(day) bc max(array w nan) = nan
#     all_lows_idx, _ = find_peaks(-day+max(day.dropna()), prominence=1, width=6,distance=15)
#     # since hight arg doesn't work with negative "day" values
#     # i remove manually all values above lb
#     below_lb_idx = []
#     for low_value, low_idx in zip(day[all_lows_idx], all_lows_idx):
#         if low_value <= lb:
#             below_lb_idx.append(low_idx)
#         #print(i)
#     plt.plot(day)
#     plt.plot(below_lb_idx, day[below_lb_idx], "x")
#     plt.plot([lb]*len(day), "--", color="gray")
#     plt.savefig('new_plots/' + f'day_{i}.jpg')
#     plt.cla()


#==============================================================================================================

#function to print the lows in the required format
# month day range
#lb = 70

def show_low_dates_ranges(lb,flag):
    #flag = 0 -> shows the data in the required format 
    #flag = 1 -> returns a list of lists containing the data that might be used later (like for a function or something)
    lows_list=[]
    for i, day in enumerate(get_day(df)):
        all_lows_idx, _ = find_peaks(-day+max(day.dropna()), prominence=1, width=6) 
        below_lb_idx = []
        for low_value, low_idx in zip(day[all_lows_idx], all_lows_idx):
            if low_value <= lb:
                below_lb_idx.append(low_idx) 
                temp_low=[day[below_lb_idx],low_idx]
                lows_list.append(temp_low)
    
    date_range=[]
    
    for i in range(len(lows_list)):#not the smartest way but it works
        temp2=[]
        temp=str(lows_list[i][0])
        temp=temp.split(' ')
        temp=temp[0].split('-')
        #temp = ['2021', '09', '17'] # an example data  
        temp2.append(temp[1])
        temp2.append(temp[2])
        #['09', '17'] # an example data  
        temp=str(lows_list[i][1])
        temp2.append(temp)
        #temp2=['09', '17', '54'] # an example data  
        date_range.append(temp2)
        #date_range = [['09', '17', '54']] # an example data
    if flag == 0:
        for i in range(len(date_range)):
            print(date_range[i][0]+ " "+date_range[i][1]+" "+date_range[i][2])
    elif flag == 1:
        return date_range
    #all the required data is stored in date_range list for further use 


#using the date as a string might not be a good option
#it's better not to change them into strings

# show_low_dates_ranges(70,1)
#========================================================================================================================

#========================================================================================================================
#in order to deal with multiple lows/peaks, we can chose a value for the "distance" argument
#of the find_peaks arguemnt
#I chose 15
#So I just used one of the arguemnts of the find_peaks function
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
#=============================================================================================


# plot high and lows, save the plot
for i, day in enumerate(get_day(df)):
    date = day.index[0].date()
    day = day.reset_index(drop=True)
    peaks, _ = find_peaks(day, height=180, prominence=1, width=6,distance=10)
    all_lows_idx, _ = find_peaks(-day+max(day.dropna()), prominence=1, width=6,distance=15) #(added the distance argument)
    below_lb_idx = []
    for low_value, low_idx in zip(day[all_lows_idx], all_lows_idx):
        if low_value <= lb:
            below_lb_idx.append(low_idx)
    plt.plot(day)
    plt.plot(below_lb_idx, day[below_lb_idx], "x")
    plt.plot(peaks, day[peaks], "x")
    plt.plot([ub]*len(day), "--", color="gray")
    plt.plot([lb]*len(day), "--", color="gray")
    plt.savefig('new_plots/' + f'day_{date}.jpg')
    plt.cla()

### some problems with this method
# see other file now 

### smoothing 

# we can smooth the line
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

for i, day in enumerate(get_day(df)):
    plt.plot(day,'o')
    plt.plot(day.index, 
        smooth(day,3), 'r-', lw=2) #red
    plt.plot(day.index, 
        smooth(day,19), 'g-', lw=2)#green
    plt.savefig('new_plots/' + f'day_{i}.jpg')
    plt.cla()




# another example of finding all lows that start from a previous high point

# df_smooth = df.copy(True)
# df_smooth['glucose'] = smooth(df['glucose'], 3)

# for day_id, day in enumerate(get_day(df_smooth)):
#     # here i work with integer index of the series
#     day.reset_index(drop=True, inplace=True)

#     # get high and low idx
#     high_idxs, _ = find_peaks(day, height=ub, prominence=1, width=6)
#     low_idxs, _ = find_peaks(-day+max(day.dropna()), prominence=1, width=6)

#     # merge all idx ( high and low) and sort them
#     all_idxs = [] # list of indexes
#     all_idxs.extend(high_idxs)
#     all_idxs.extend(low_idxs)
#     all_idxs.sort()

#     # track if the index corresponds to a low or a high
#     occurrence = [] # 'L' or 'H'
#     for idx in all_idxs:
#         if idx in high_idxs:
#             occurrence.append('H')
#         else:
#             occurrence.append('L')

#     # find every pair of indicies that follow this rule:
#     # a high followed by a low & 
#     # high value - low value > threshold ( here threshold = ub - lb)
#     high_low_pairs_idx:'list[tuple]' = [] # [(high_idx, low_idx),(high_idx, low_idx), ... ]
#     i = 0
#     # -1 bc i work with base 0 idx
#     while i < len(occurrence)-1:
#         if occurrence[i] == 'H' and occurrence[i+1] == 'L':
#             high_idx = all_idxs[i]
#             low_idx = all_idxs[i+1]
#             high_val = day.iloc[high_idx]
#             low_val = day.iloc[low_idx]

#             if high_val - low_val > ub - lb:
#                 high_low_pairs_idx.append((high_idx, low_idx))
#                 i += 1
#             else:
#                 i += 1
#         else:
#             i += 1

    # plotting
    plt.plot(day)
    if high_low_pairs_idx:
        for event in high_low_pairs_idx:
            drop_event = day.iloc[event[0]:event[1]]
            start = drop_event.head(1).index
            end = drop_event.tail(1).index
            plt.plot(drop_event.index, drop_event, 'r-', lw=2)
    plt.savefig('new_plots/' + f'day_{day_id}.jpg')
    plt.cla()
    # print(day_id)

 
