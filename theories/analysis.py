import os
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import cm

from settings import OUTPUT_DIR, GAZP_PATH_MIN, GAZP_PATH_5MIN, GAZP_PATH_HOUR
from services import get_standartized_data
from theory import TheoryQuickGrowth

# mpl.use('Qt5Agg')


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
                self.theories.append(theory)

    def _count_all_theories(self):
        ''' Подсчет статистики всех теорий
        '''
        count = 1
        for theory in self.theories:
            print('progress: ', str((count/len(self.theories))*100)[:6] + '%', count, '/', len(self.theories))
            theory.check()
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

            self.full_meta_statistic['Nmin'].append(theory.Nmin)
            self.full_meta_statistic['Nmax'].append(theory.Nmax)

    def write_meta_statistic_to_csv(self, path=os.path.join(OUTPUT_DIR, 'outputfull_hour.csv')):
        ''' Пишет имеющуюся статистику в файл
        '''
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

    def view_graph_statistic(self, stat_arg='total'):
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

    def view_all_graphics(self):
        ''' Выводит статистику в виде графиков
        '''
        self.view_graph_statistic()
        self.view_graph_statistic('avr_lesion')
        self.view_graph_statistic('avr_profit')
        self.view_graph_statistic('avr_potencial')

    def get_anilysis(self):
        ''' Подсчитывает всю статистику
        '''
        self._count_all_theories()
        self._get_full_meta_statistic()



def main():
    LDATA = [GAZP_PATH_MIN, GAZP_PATH_5MIN, GAZP_PATH_HOUR]
    data = get_standartized_data(path=GAZP_PATH_HOUR)
    analysis = TheoryQuickGrowthAnalysis(min_ind=10, max_ind=60, step=5, data=data)
    analysis.get_anilysis()
    analysis.write_meta_statistic_to_csv()
    analysis.view_all_graphics()


if __name__ == '__main__':
    main()
