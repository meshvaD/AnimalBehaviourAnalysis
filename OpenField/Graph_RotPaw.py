import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_group(name):
    if group_1.count(name) > 0:
        return None
    elif group_2.count(name) > 0:
        return None
    elif group_3.count(name) > 0:
        return 1
    elif group_4.count(name) > 0:
        return 2

def sort_means(names, means):
    sorted_means = [None, None, None, None]
    for i in range(0, len(names)):
        if i == 22:
            print('breakpoint')
        n = names[i]
        group = get_group(n)

        if group != None:
            m = sorted_means[group-1]
            if m != None:
                m.append(means[i])
                sorted_means[group-1] = m
            else:
                sorted_means[group-1] = [means[i]]
        print(n)
    return sorted_means

def plot_bar(sorted_means, num_groups, ax, color, bar_pos):
    for i in range(0, num_groups):
        avg = 0
        for mean in sorted_means[i]:
            #plot each point
            jitter = np.random.uniform(low=bar_pos[i]-0.1, high=bar_pos[i]+0.1)
            ax.plot(jitter, mean, color+'o')

            avg += mean

        avg /= len(sorted_means[i])
        print(avg)

        #plot avg line
        ax.hlines(avg, xmin = bar_pos[i]-0.2, xmax = bar_pos[i]+0.2, color='k')


df = pd.read_csv('OpenField/output_rotations_20210617.csv')
df_2 = pd.read_csv('OpenField/output_rotations_20210730.csv')

group_1 = ['PD5-01', 'PD5-02', 'PD5-03', 'PD5-13', 'PD5-14']
group_2 = ['PD5-24', 'PD5-19', 'PD5-20', 'PD5-12']
group_3 = ['PD5-09', 'PD5-18', 'PD5-17', 'PD5-10', 'PD06-02', 'PD06-06', 'PD06-05']
group_4 = ['PD5-04', 'PD5-08', 'PD5-15', 'PD5-06', 'PD06-03', 'PD06-04', 'PD06-08']

names = df['name']
means = df['adjusted mean']

names_2 = df_2['name']
means_2 = df_2['adjusted mean']

sorted_means = sort_means(names, means)
sorted_means_2 = sort_means(names_2, means_2)

print(sorted_means, '\n \n')
print(sorted_means_2)

fig, ax = plt.subplots(1,1)

plot_bar(sorted_means, 2, ax, 'b', [1,3])
plot_bar(sorted_means_2, 2, ax, 'r', [2,4])

ax.axhline(0, linestyle='--', color='gray') #x-axis at y=0


ax.set_xticks([1,2,3,4])

#change depending on slides
ax.set_xticklabels(['a', 'b', 'c', 'd'])

plt.show()

