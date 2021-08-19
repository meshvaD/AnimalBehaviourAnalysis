import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_group(name):
    if group_1.count(name) > 0:
        return 1
    elif group_2.count(name) > 0:
        return 2
    elif group_3.count(name) > 0:
        return 3
    elif group_4.count(name) > 0:
        return 4

def sort_means(names, means):
    sorted_means = [None, None, None, None]
    for i in range(0, len(names)):
        n = names[i]
        group = get_group(n)

        if group != None:
            m = sorted_means[group-1]
            if m != None:
                m.append(means[i])
                sorted_means[group-1] = m
            else:
                sorted_means[group-1] = [means[i]]
    return sorted_means

def sorted_ratios(df, df_2):
    names = df['name']
    means = df['adjusted mean']

    names_2 = df_2['name']
    means_2 = df_2['adjusted mean']

    sorted_ratios = [None, None, None, None]
    for i in range(0, len(names)):
        n = names[i]
        group = get_group(n)

        #get index of name from second list
        try:
            j = names_2.values.tolist().index(n)

            if group != None:
                m = sorted_ratios[group-1]
                if means_2[j] == 0 or means[i] == 0:
                    ratio = 0
                else:
                    ratio = means_2[j] / means[i]


                if m != None:
                    m.append(ratio)
                    sorted_ratios[group-1] = m
                else:
                    sorted_ratios[group-1] = [ratio]
        except:
            print(n)
    return sorted_ratios

def plot_bar(df, num_groups, ax, color, bar_pos, sorted_ratios=None):
    if sorted_ratios == None:
        names = df['name']
        means = df['adjusted mean']
        sorted_means = sort_means(names, means)
    else:
        sorted_means = sorted_ratios

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

    ax.axhline(1, linestyle='--', color='gray') #x-axis at y=0

def plot_bar_connected(df, df_2, ax):
    names = df['name']
    means = df['adjusted mean']

    names_2 = df_2['name']
    means_2 = df_2['adjusted mean']

    for i in range (0, len(names_2)):
        n = names_2[i]
        group = get_group(n)

        if group != None:
            j = names.values.tolist().index(n)

            #jitter = np.random.uniform(low=-0.05, high=+0.05)

            x = group - 0.1
            x_2 = group + 0.1

            y = np.abs(means[j])
            y_2 = np.abs(means_2[i])

            ax.plot(x, y, 'ro')
            ax.plot(x_2, y_2, 'bo')

            #find slope of line
            m = (y_2 - y) / (x_2 - x)

            #plot line between two
            ax.plot([x, x_2], [y, y_2], color='k')



group_1 = ['PD5-01', 'PD5-02', 'PD5-03', 'PD5-13', 'PD5-14']
group_2 = ['PD5-24', 'PD5-19', 'PD5-20', 'PD5-12']
group_3 = ['PD5-09', 'PD5-18', 'PD5-17', 'PD5-10', 'PD06-02', 'PD06-06', 'PD06-05']
group_4 = ['PD5-04', 'PD5-08', 'PD5-15', 'PD5-06', 'PD06-03', 'PD06-04', 'PD06-08']

basepath = 'C:/Users/HS student/Desktop/Behavioural Analysis/'

df = pd.read_csv(basepath + 'Test_1/Cylinder Test.csv')
df_2 = pd.read_csv(basepath + 'Test_2/Cylinder Test.csv')

fig, ax = plt.subplots(1,1)

#plot_bar(df, 4, ax, 'r', [1,3,5,7]) #before
#plot_bar(df_2, 4, ax, 'b', [2,4,6,8]) #after

#ratios = sorted_ratios(df, df_2)
#plot_bar(None, 2, ax, 'r', [1,2], ratios)

plot_bar_connected(df, df_2, ax)

ax.set_xticks([1,2,3,4])

#change depending on slides
ax.set_xticklabels(['1', '2', '3', '4'])

plt.savefig(basepath + 'cylinder_lineplot' + '.png')
print('saved')

plt.show()
