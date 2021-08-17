import os
import pandas as pd
import numpy as np

def adjusted(nums):
    nums.sort()
        
    del nums[0]
    del nums[0]
    del nums[len(nums)-1]
    del nums[len(nums)-1]

    return nums

def new_row(file):
    name = file.split('/')[1].split('.')[0]

    temp_df = pd.read_csv(file, index_col=False)

    new = [0] * (int(10/ interval) + 2) # x3 for L/R/T +1 for name
    new[0] = name

    for row in temp_df.iterrows():

        insert_time = int(row[1]['frame'] / fpm / interval)
                
        # OPTION 1: for each time interval, 3 diff counts for left/right/together touches
        #if (row[1]['left_count'] == 1 and row[1]['right_count'] == 1):
        #    in_loc = insert_time * 3 + 3
        #elif (row[1]['left_count'] == 1):
        #    in_loc = insert_time * 3 + 1
        #elif (row[1]['right_count'] == 1):
        #    in_loc = insert_time * 3 + 2

        # OPTION 2: 2 diff counts for left/right
        #if (row[1]['left_count'] == 1):
        #    in_loc = insert_time * 2 + 1
        #    new[in_loc] = new[in_loc] + 1
        #if (row[1]['right_count'] == 1):
        #    in_loc = insert_time * 2 + 2
        #    new[in_loc] = new[in_loc] + 1

        # OPTION 3: left as +, right as -
        in_loc = insert_time + 1
        count = 0
        if (row[1]['left_count'] == 1):
            count += 1
        if (row[1]['right_count'] == 1):
            count -= 1
        new[in_loc] = new[in_loc] + count

    new_copy = new.copy()
    del new_copy[0] #find adjusted mean after removing name from row

    adj_mean = np.mean(adjusted(new_copy)) 
    new[len(new)-1] = adj_mean
    df.loc[len(df)] = new


interval = (int)(input('Time Interval (minutes) '))
fpm = 3600

header = ['name']
for x in range(0, 10, interval):
    header.append(str(x) + ' - ' + str(x + interval))
    #header.append(str(x) + ' - ' + str(x + interval) + " R")
    #header.append(str(x) + ' - ' + str(x + interval) + " T")
header.append('adjusted mean')

df = pd.DataFrame(columns = header)

dir = 'paw_20210729'
for filename in os.listdir(dir):
    if filename.endswith('.csv'):
        new_row(dir + '/' + filename)

pd.set_option('display.max_rows', None, 'display.max_columns', None)
df.to_csv(dir + '_10signed.csv', index=False)
print(df)
