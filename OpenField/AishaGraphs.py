import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

df = pd.read_csv('C:/Users/HS student/Downloads/Aisha Graph.csv')

x = df['Group'].values.tolist()
y = df['Left Paw Usage Increase ()'].values.tolist()

fig, ax = plt.subplots(1,1)

prev_group = 1
count = 0
geo_mean = 1
mean = 0

colors = ['go', 'ro', 'bo', 'yo']

sorted_vals = [[None]]
mean_list = []

for i in range(0, len(x)):
    jitter = np.random.uniform(low=-0.05, high=+0.05)
    x_plot = x[i] + jitter
    ax.plot(x_plot + jitter, y[i], colors[x[i] - 1])

    if x[i] != prev_group:
        geo_mean = geo_mean ** (1/count)

        mean /= count

        mean_list.append(mean)
        ax.hlines(mean, xmin = x[i]-0.2-1, xmax = x[i]+0.2-1, color='k')

        if i != len(x) - 1:
            count = 1
            geo_mean = y[i]
            mean = y[i]

        sorted_vals.append([y[i]])
    else:
        geo_mean *= y[i]
        mean += y[i]
        count += 1 

        if sorted_vals[-1][-1] == None:
            sorted_vals[-1][-1] = y[i]
        else:
            sorted_vals[-1].append(y[i])

    prev_group = x[i]

#last group
geo_mean = geo_mean ** (1/count)
mean /= count

mean_list.append(mean)
ax.hlines(mean, xmin = prev_group-0.2, xmax = prev_group+0.2, color='k')

print(sorted_vals)

#calculate standard deviation
#std_list = []
#for group in sorted_vals:
#    std_list.append(np.std(group))

#print(std_list)

se_list = [8.6115459961870100,	3.9382458023846100,	2.3741314201197900,	6.8728017102353700]
#for i in range(0, len(std_list)):
#    print(std_list[i], ', ', len(sorted_vals[i]) ** (1/2))
#    se_list.append(std_list[i]/(len(sorted_vals[i]) ** (1/2)))
#print(se_list)

#draw error bars
for i in range(0, len(se_list)):
    plt.errorbar(i+1, mean_list[i], yerr=se_list[i], ecolor='k')

plt.show()