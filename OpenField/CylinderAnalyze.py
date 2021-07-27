import os
import pandas as pd

def new_row(file):
    name = file.split('/')[1].split('.')[0]

    temp_df = pd.read_csv(file, index_col=False)

    new = [0] * (int(10 * 3 / interval) + 1) # x3 for L, R, and T
    new[0] = name

    for row in temp_df.iterrows():

        insert_time = int(row[1]['frame'] / fpm / interval)

        if (row[1]['left_count'] == 1 and row[1]['right_count'] == 1):
            in_loc = insert_time * 3 + 3
        elif (row[1]['left_count'] == 1):
            in_loc = insert_time * 3 + 1
        elif (row[1]['right_count'] == 1):
            in_loc = insert_time * 3 + 2

        new[in_loc] = new[in_loc] + 1


    #df.append(new)
    df.loc[len(df)] = new


interval = (int)(input('Time Interval (minutes) '))
fpm = 3600

header = ['name']
for x in range(0, 10, interval):
    header.append(str(x) + ' - ' + str(x + interval) + " L")
    header.append(str(x) + ' - ' + str(x + interval) + " R")
    header.append(str(x) + ' - ' + str(x + interval) + " T")

df = pd.DataFrame(columns = header)

for filename in os.listdir('cylinder_test'):
    if filename.endswith('.csv'):
        new_row('cylinder_test/' + filename)

pd.set_option('display.max_rows', None, 'display.max_columns', None)
df.to_csv('cylinder_test_interval_10.csv')
print(df)
