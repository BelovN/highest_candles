import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import cm

from services import get_standartized_data
from theory import TheoryQuickGrowth

mpl.use('Qt5Agg')


class TheoryQuickGrowthAnalysis:
    ''' Класс для проверки теории c несколькими различными параметрами
    '''
    def __init__(self, min_ind, max_ind, step, data):
        self.min_ind = min_ind
        self.max_ind = max_ind
        self.step = step
        self.data = data
        self.full_meta_statistic = {}
        self.theories = []

        # Создание теорий в диапазоне (min_ind, max_ind)
        for i in range(min_ind, max_ind + step, step):
            for j in range(min_ind, max_ind + step, step):
                theory = TheoryQuickGrowth(self.data, Nmin=i, Nmax=j)
                theories.append(theory)


    def _count_all_theories(self):
        ''' Подсчет статистики всех теорий
        '''
        for theory in theories:
            theory.check()


    def _get_full_meta_statistic(self):
        ''' Объединение все статистик в одну
        '''
        self.full_meta_statistic['Nmin'] = []
        self.full_meta_statistic['Nmax'] = []

        for key in self.theories[0].meta_statistic:
            self.full_meta_statistic[key] = []

        for theory in self.theories:
            for key, value in theory.meta_statistic.items():
                self.full_meta_statistic[key].append(value)

            self.full_meta_statistic['Nmin'].append(theory.Nmin)
            self.full_meta_statistic['Nmax'].append(theory.Nmax)


    def _get_coordinates(self, data_list=[]):
        ''' Разбиение данных для отображения в 3d графике
        '''
        split_value = int(math.sqrt(len(self.theories)))
        coordinates = []
        for i in range(split_value):
            data_slice = data_list[i*split_value:(i+1)*split_value]
            coordinates.append(np.asarray(data_slice))

        coordinates = np.asarray(coordinates)
        return coordinates


    def view_graph_statistic(self, stat_arg='total'):
        ''' Выводит графики статистики
            stat_arg - Z координата графики
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


    def get_anilysis(self):
        ''' Подсчитывает всю статистику и выводит в графике
        '''
        self._count_all_theories()
        self._get_full_meta_statistic()
        self.view_graph_statistic()
        self.view_graph_statistic('avr_lesion')
        self.view_graph_statistic('avr_profit')
        self.view_graph_statistic('avr_potencial')


def main():
    data = get_standartized_data()
    analysis = TheoryQuickGrowthAnalysis()
    analysis.get_anilysis()


if __name__ == '__main__':
    main()
