import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import cm

from services import get_standartized_data
from settings import OUTPUT_FILE_DIR
from theory import TheoryQuickGrowth

mpl.use('Qt5Agg')


INPUT_FILE_DIR = OUTPUT_FILE_DIR.replace('output.txt', 'output_h.txt')


class TheoryQuickGrowthAnalysis:
    def __init__(self):
        self.full_meta_statistic = {}

    def count_all_theories(self, min_ind, max_ind, step, data):
        theories = []
        for i in range(min_ind, max_ind + step, step):
            for j in range(min_ind, max_ind + step, step):
                theory = TheoryQuickGrowth(data, Nmin=i, Nmax=j)
                theory.check()
                theories.append(theory)

        self.theories = theories


    def _get_full_meta_statistic(self):
        self.full_meta_statistic['Nmin'] = []
        self.full_meta_statistic['Nmax'] = []

        for key in self.theories[0].meta_statistic:
            self.full_meta_statistic[key] = []

        for theory in self.theories:
            for key, value in theory.meta_statistic.items():
                self.full_meta_statistic[key].append(value)

            self.full_meta_statistic['Nmin'].append(theory.Nmin)
            self.full_meta_statistic['Nmax'].append(theory.Nmax)

        # print(self.full_meta_statistic)


    def find_correlation(self, Nmin, Nmax, step):
        self._get_full_meta_statistic()


    def _get_coordinates(self, data_list=[]):
        split_value = int(math.sqrt(len(self.theories)))
        # split_value = 4
        # data_list = self.full_meta_statistic['Nmin']
        coordinates = []
        for i in range(split_value):
            data_slice = data_list[i*split_value:(i+1)*split_value]
            coordinates.append(np.asarray(data_slice))

        coordinates = np.asarray(coordinates)
        return coordinates


    def view_graph_statistic(self, stat_arg='total'):
        ''' Выводит графики статистики
        '''

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        data = pd.read_csv(INPUT_FILE_DIR, sep=' ', encoding='utf-8')
        X = self._get_coordinates(self.full_meta_statistic['Nmin'])
        Y = self._get_coordinates(self.full_meta_statistic['Nmax'])
        Z = self._get_coordinates(self.full_meta_statistic[stat_arg])

        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)


        ax.set_xlabel('N MIN')
        ax.set_ylabel('N MAX')
        ax.set_zlabel(stat_arg.upper())

        plt.show()


data = get_standartized_data()
analysis = TheoryQuickGrowthAnalysis()
analysis.count_all_theories(5, 100, 5, data)
analysis._get_full_meta_statistic()

analysis.view_graph_statistic()
analysis.view_graph_statistic('avr_lesion')
analysis.view_graph_statistic('avr_profit')
analysis.view_graph_statistic('avr_potencial')

# print(a)
