import os
import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import filedialog

def adjusted(nums):
    nums.sort()
        
    del nums[0]
    del nums[0]
    del nums[len(nums)-1]
    del nums[len(nums)-1]

    return nums

def new_row(file, option):
    name = file.split('/')[-1].split('.')[0]

    temp_df = pd.read_csv(file, index_col=False)

    new = [0] * (int(10 * option/ interval) + 2)
    new[0] = name

    for row in temp_df.iterrows():

        insert_time = int(row[1]['frame'] / fpm / interval)

        #left as +, right as -
        if option == 1:
            in_loc = insert_time + 1
            count = 0
            if (row[1]['left_count'] == 1):
                count += 1
            if (row[1]['right_count'] == 1):
                count -= 1
            new[in_loc] = new[in_loc] + count
        elif option == 2: #2 diff counts for left/right
            if (row[1]['left_count'] == 1):
                in_loc = insert_time * 2 + 1
                new[in_loc] = new[in_loc] + 1
            if (row[1]['right_count'] == 1):
                in_loc = insert_time * 2 + 2
                new[in_loc] = new[in_loc] + 1
        elif option == 3: #for each time interval, 3 diff counts for left/right/together touches
            if (row[1]['left_count'] == 1 and row[1]['right_count'] == 1):
                in_loc = insert_time * 3 + 3
            elif (row[1]['left_count'] == 1):
                in_loc = insert_time * 3 + 1
            elif (row[1]['right_count'] == 1):
                in_loc = insert_time * 3 + 2

    new_copy = new.copy()
    del new_copy[0] #find adjusted mean after removing name from row

    adj_mean = np.mean(adjusted(new_copy)) 
    new[len(new)-1] = adj_mean
    df.loc[len(df)] = new


interval = (int)(input('Time Interval (minutes) '))
fpm = (int)(input('Fps ')) * 60
option = (int)(input('Option Number '))

header = ['name']
for x in range(0, 10, interval):
    if option == 1:
        header.append(str(x) + ' - ' + str(x + interval))
    elif option == 2:
        header.append(str(x) + ' - ' + str(x + interval) + " L")
        header.append(str(x) + ' - ' + str(x + interval) + " R")
    elif option == 3:
        header.append(str(x) + ' - ' + str(x + interval) + " L")
        header.append(str(x) + ' - ' + str(x + interval) + " R")
        header.append(str(x) + ' - ' + str(x + interval) + " T")

header.append('adjusted mean')

df = pd.DataFrame(columns = header)

root = tk.Tk()
root.withdraw()

print('Select the directory with all the individual animal .csv files')
dir = filedialog.askdirectory()

for filename in os.listdir(dir):
    if filename.endswith('.csv'):
        new_row(dir + '/' + filename, option)

pd.set_option('display.max_rows', None, 'display.max_columns', None)

print('Select the directory to save the .csv file')
save_dir = filedialog.askdirectory()

df.to_csv(save_dir + '/Cylinder Test.csv', index=False)
print(df)
