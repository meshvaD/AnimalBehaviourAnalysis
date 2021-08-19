import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import filedialog

#sort numbers and delete two lowest/highest numbers
def adjusted(nums):
    nums.sort()
        
    del nums[0]
    del nums[0]
    del nums[len(nums)-1]
    del nums[len(nums)-1]

    return nums

def get_name(filename):
    return filename.split('_')[1].split('.')[0]

interval = (int)(input('Time Interval (minutes) '))
fps = (int)(input('Frames per second '))
fpm = fps * 60

#creater header
header = ['name']
for x in range(0, 10, interval):
    r = str(x) + ' - ' + str(x+interval)
    header.append(r)

header.append('adjusted mean')

#user inputed location
root = tk.Tk()
root.withdraw()

print('Select the .txt file is location')
open_file = filedialog.askopenfilename()

df = pd.read_csv(open_file, delimiter = "\t")
print(df)

data = []

#number of cols depends on interval size
row = [0] * int(10/ interval)

prev_name = ""
for index, r in df.iterrows(): 
    
    name = get_name(r['Filename'])

    #ObjectJ updates slice for both cw/ccw for each click --> cw_slice = ccw_slice always
    cw_slice = int(r['Slice_cw'])
    insert_index = int(cw_slice / fpm)

    # + for cw (always on left in txt file) and - for ccw
    if (int(r['Count_cw']) != 0):
        c = 1
    else:
        c = -1

    if(insert_index == len(row)):
        insert_index -= 1

    #if name same as previous txt file row, add data to same animal row
    if (name == prev_name or prev_name == ""):
        row[insert_index] = c + row[insert_index]
    else:
        adj_mean = np.mean(adjusted(row.copy()))

        row.insert(0, prev_name)
        row.insert(len(row), adj_mean)
        data.append(row) #append animal row to complete data array

        row = [0] * int(10/ interval) #reset row

        row[insert_index] = c


    prev_name = name

#for last one
adj_mean = np.mean(adjusted(row.copy()))

row.insert(0, prev_name)
row.insert(len(row), adj_mean)
data.append(row)

row = [0] * int(10/ interval)
row[insert_index] = c

#dataframe displayed
df_output = pd.DataFrame(columns = header, data = data)
pd.set_option('display.max_rows', None, 'display.max_columns', None)

print('Select the folder to save new .csv file')
open_file = filedialog.askdirectory()

df_output.to_csv(open_file + '/Rotation Test_adjusted.csv', index=False)

print(df_output)