import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_group(name):
    if group_1.count(name) > 0:
        return 1
    elif group_2.count(name) > 0:
        return 2
    elif group_3.count(name) > 0:
        return 2
    elif group_4.count(name) > 0:
        return 2


df = pd.read_csv('paw_20210616_10signed.csv')

group_1 = ['PD5-01', 'PD5-02', 'PD5-03', 'PD5-13', 'PD5-14']
group_2 = ['PD5-24', 'PD5-19', 'PD5-20', 'PD5-12']
group_3 = ['PD5-09', 'PD5-18', 'PD5-17', 'PD5-10', 'PD06-02', 'PD06-06', 'PD06-05']
group_4 = ['PD5-04', 'PD5-08', 'PD5-15', 'PD5-06', 'PD06-03', 'PD06-04', 'PD06-08']

names = df['name']
means = df['adjusted mean']

sorted_means = [None, None, None, None]

for i in range(1, len(names)):
    n = names[i]
    group = get_group(n)
    
    if group != None:
        m = sorted_means[group-1]
        if m != None:
            m.append(means[i])
            sorted_means[group-1] = m
        else:
            sorted_means[group-1] = [means[i]]

print(sorted_means)

fig, ax = plt.subplots(1,1)

ax.axhline(0, linestyle='--', color='gray') #x-axis at y=0

for i in range(0, 2):
    avg = 0
    for mean in sorted_means[i]:
        #plot each point
        jitter = np.random.uniform(low=i+0.9, high=i+1.1)
        ax.plot(jitter, mean, 'ro')

        avg += mean

    avg /= len(sorted_means[i])

    ##calculate standard deviation
    #s = 0
    #for val in sorted_means[i]:
    #    s += (val - avg) ** 2
    #s= (s/len(sorted_means[i])) ** 0.5
    #print(s)

    ##plot error bars
    #x = [i+1]*len(sorted_means[i])
    #ax.errorbar(x, sorted_means[i], yerr=s, fmt = 'none', color='gray')

    #plot avg line
    ax.hlines(avg, xmin = i+0.8, xmax = i+1.2)

ax.set_xticks([1,2])

#change depending on slides
ax.set_xticklabels(['a', 'b'])

plt.show()

