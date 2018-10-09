# -*- coding: utf-8 -*-
from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# set font
rcParams['font.family'] = 'sans-serif'
rcParams['font.size'] = 10
rcParams['font.sans-serif'] = ['Latin Modern Mono']

csv_names = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']


def import_csv(csv_names):
    data = {}
    for i in csv_names:
        data[str(i)] = pd.read_csv('csv/' + i + '.csv')
        del data[str(i)]['generation']

        data[str(i)]['avg'] = \
            data[str(i)].iloc[1:, 1:].sum(axis=1) / (len(data[str(i)].columns) - 1)

    return data


def draw_plots(data):
    ax = plt.subplot(1, 2, 1)
    colors = ['b-', 'g-', 'r-', 'k-', 'm-']
    markers = ['8', 'v', 'D', 's', 'd']

    i = 0
    for key, value in data.items():
        plt.plot(
            'effort', 'avg', colors[i], label=key, marker=markers[i],
            markevery=25, markersize=4, linewidth=0.5, data=value)
        i += 1

    plt.margins(0)
    plt.grid(color='k', drawstyle="steps", linestyle='--', alpha=0.4, linewidth=0.8)
    plt.xlabel('Rozegranych gier (x1000)')
    plt.ylabel('Odsetek wygranych gier [%]')
    plt.title('Pokolenie')
    plt.legend(loc=4)

    plt.xticks(np.arange(0, 500001, 100000), np.arange(0, 501, 100))
    plt.yticks(np.arange(0.6, 1.01, 0.05), np.arange(60, 101, 5))

    # additional x-axis
    ax2 = ax.twiny()
    ax2.xaxis.tick_top()
    plt.xticks(np.arange(0, 500001, 100000), np.arange(0, 201, 40))

    # boxplot
    bx = plt.subplot(1, 2, 2)
    boxes_array = []
    for key, value in data.items():
        # normalized_df =  (y - y.mean()) / y.std()
        boxes_array.append(value['avg'][1:])

    meanprops = dict(marker='o', markeredgecolor='black', markerfacecolor='blue')
    whiskerprops = dict(color='b', linestyle='--')
    flierprops = dict( color='b', marker='+', markersize=3.0)
    medianprops = dict( color='red', linewidth=1.5)

    bp = plt.boxplot(
        boxes_array, patch_artist=True, notch=True, bootstrap=500,
        labels=csv_names, showmeans=True, whiskerprops=whiskerprops, meanprops=meanprops,
        medianprops=medianprops, flierprops=flierprops)

    plt.setp(bp['boxes'], color='blue', linewidth=1.5)
    plt.setp(bp['boxes'], facecolor='#ffffff', alpha=0.5)

    plt.margins(0)
    plt.grid(color='k', drawstyle="steps", linestyle='--', alpha=0.4, linewidth=0.8)
    bx.yaxis.tick_right()
    plt.yticks(np.arange(0.6, 1.01, 0.05), np.arange(60, 101, 5))
    plt.xticks(rotation=20)


def main():
    data = import_csv(csv_names)
    draw_plots(data)
    plt.show()


if __name__ == '__main__':
    main()
