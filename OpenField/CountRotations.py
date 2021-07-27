import pandas as pd
import numpy as np

file = open('C:/Users/HS student/Desktop/20210617/Results.txt')
lines = file.readlines()

interval = (int)(input('Time Interval (minutes) '))
fps = (int)(input('Frames per second '))
fpm = fps * 60

data = []

def adjusted(nums):
    nums.sort()
    
    #s = sorted(nums, key= abs)
    
    del nums[0]
    del nums[0]
    del nums[len(nums)-1]
    del nums[len(nums)-1]

    return nums

def get_name(filename):
    return filename.split('_')[1]

header = ['name']
for x in range(0, 10, interval):
    r = str(x) + ' - ' + str(x+interval)
    header.append(r)

header.append('adjusted mean')
data.append(header)

prev_name = ""

row = [0] * int(10/ interval)

for i in range(1, len(lines)-1): #-1 for header
    l = lines[i]
    
    name = get_name(l.split('\t')[1])

    cw_slice = int(l.split('\t')[3])
    insert_index = int(cw_slice / fpm)

    if (int(l.split('\t')[2]) != 0):
        c = 1
    else: # (l.split('\t')[4] != 0)
        c = -1

    if(insert_index == len(row)):
        insert_index -= 1

    if (name == prev_name or prev_name == ""):
        row[insert_index] = c + row[insert_index]
    else:
        print('diff')

        adj_mean = np.mean(adjusted(row.copy()))

        row.insert(0, prev_name)
        row.insert(len(row), adj_mean)
        data.append(row)

        row = [0] * int(10/ interval)

        row[insert_index] = c


    prev_name = name

#for last one
print('diff')
adj_mean = np.mean(adjusted(row.copy()))

row.insert(0, prev_name)
row.insert(len(row), adj_mean)
data.append(row)

row = [0] * int(10/ interval)
row[insert_index] = c

#dataframe displayed
df = pd.DataFrame(data = data)
pd.set_option('display.max_rows', None, 'display.max_columns', None)

df.to_csv('output_rotations.csv', index=False)

print(df)