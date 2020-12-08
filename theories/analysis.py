import os
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import cm

from settings import *
from services import get_standartized_data
from theory import TheoryQuickGrowth

mpl.use('Qt5Agg')


class TheoryQuickGrowthAnalysis:
    ''' Класс для проверки теории c несколькими различными параметрами
    '''
    def __init__(self, data):
        self.data = data
        self.full_meta_statistic = {}
        self.theories = []

    def set_theories_Nmax_Nmin(self, min_ind, max_ind, step_ind, min_percent, max_percent, step_percent):
        ''' Создание теорий в диапазоне (min_ind, max_ind)
        '''
        for i in range(min_ind, max_ind + step_ind, step_ind):
            for j in range(min_ind, max_ind + step_ind, step_ind):
                for percent in np.arange(min_percent, max_percent + step_percent, step_percent):
                    theory = TheoryQuickGrowth(self.data, Nmin=i, Nmax=j, percent_from_delta=percent)
                    self.theories.append(theory)

    def set_theories_percent(self, Nmin, Nmax, min_percent, max_percent, step):
        ''' Создание теорий в диапазоне процента (min_percent, max_percent)
        '''
        for percent in np.arange(min_percent, max_percent + step, step):
            theory = TheoryQuickGrowth(self.data, Nmin=Nmin, Nmax=Nmax, percent_from_delta=percent)
            self.theories.append(theory)

    def _count_all_theories(self):
        ''' Подсчет статистики всех теорий
        '''
        count = 1
        for theory in self.theories:
            print('progress: ', str((count/len(self.theories))*100)[:6] + '%', count, '/', len(self.theories))
            theory.full_check()
            count += 1

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

    def write_meta_statistic_to_csv(self, path=os.path.join(OUTPUT_DIR, 'full_meta.csv')):
        ''' Пишет имеющуюся статистику в файл
        '''
        df = pd.DataFrame.from_dict(self.full_meta_statistic)
        with open(path, 'w', encoding='utf-8') as file:
            df.to_csv(file, index=False, header=True, sep=';', float_format='%.3f', decimal=',')

    def print_full_meta_statistic(self):
        df = pd.DataFrame.from_dict(self.full_meta_statistic)
        with open(path, 'w', encoding='utf-8') as file:
            df.to_csv(file, index=False, header=True, sep=';', float_format='%.3f', decimal=',')

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

    def view_graph_statistic3D(self, stat_arg='total'):
        ''' Выводит графики статистики
            stat_arg - Z координата графики
        '''

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        X = self._get_coordinates(self.full_meta_statistic['Nmin'])
        Y = self._get_coordinates(self.full_meta_statistic['Nmax'])
        Z = self._get_coordinates(self.full_meta_statistic[stat_arg])

        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        ax.set_xlabel('N MIN')
        ax.set_ylabel('N MAX')
        ax.set_zlabel(stat_arg.upper())

        plt.show()

    def view_all_graphics3D(self):
        ''' Выводит статистику в виде графиков
        '''
        self.view_graph_statistic3D()
        self.view_graph_statistic3D('avr_lesion')
        self.view_graph_statistic3D('avr_profit')
        self.view_graph_statistic3D('avr_potencial')
        self.view_graph_statistic3D('total_short')
        self.view_graph_statistic3D('total_long')

    def get_anilysis_params(self):
        ''' Подсчитывает всю статистику
        '''
        self._count_all_theories()
        self._get_full_meta_statistic()



def main():
    data = get_standartized_data(path=SPB_PATH_HOUR_2020)
    analysis = TheoryQuickGrowthAnalysis(data=data)
    analysis.set_theories_Nmax_Nmin(min_ind=25, max_ind=30, step_ind=5,
                                    min_percent=0.3, max_percent=0.3, step_percent=0.1)
    analysis.get_anilysis_params()
    analysis.write_meta_statistic_to_csv()
    print('DONE!')


if __name__ == '__main__':
    main()
