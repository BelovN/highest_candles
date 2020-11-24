import math
import datetime
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import os
import pandas as pd

from services import get_standartized_data
from settings import OUTPUT_FILE_DIR, GAZP_PATH_5MIN, GAZP_PATH_HOUR, GAZP_PATH_MIN


class TheoryStatistic:
    ''' Класс для сбора статистики
    '''
    def __init__(self, *args, **kwargs):
        self.statistic = {
            'ind_in': [],
            'ind_out': [],
            'point_in': [],
            'point_out': [],
            'delta_price': [],
            'potencial': [],
            'delta_potencial': [],
            'time_in': [],
            'time_out': [],
            'delta_time': [],
            'delta_max_min': [],
        }
        self.meta_statistic = {
            'count_lesion': 0,
            'avr_lesion': 0,
            'count_profit': 0,
            'avr_profit': 0,
            'count_all': 0,
            'total': 0,
            'avr_all': 0,
            'avr_potencial': 0,
            'avr_max_min': 0,
        }

    def _get_statistic(self):
        ''' Подсчитывает дельта статистику
        '''
        for i in range(len(self.statistic['ind_out'])):
            ind_in = self.statistic['ind_in'][i]
            ind_out = self.statistic['ind_out'][i]
            date_in = dates.num2date(self.data['DATE'][ind_in])
            date_out = dates.num2date(self.data['DATE'][ind_out])

            self.statistic['delta_price'].append(self.statistic['point_out'][i] - self.statistic['point_in'][i])
            self.statistic['delta_time'].append((date_out - date_in).seconds / 60)

            self.statistic['potencial'].append(max(self.data['<CLOSE>'][ind_in:ind_out]))
            self.statistic['delta_potencial'].append(self.statistic['potencial'][i] - self.statistic['point_in'][i])
            self.statistic['delta_max_min'].append(self.highest[i] - self.lowest[i])


        min_len = len(self.statistic['ind_out'])
        for key, value in self.statistic.items():
            self.statistic[key] = self.statistic[key][:min_len]

    def _get_meta_statistic(self):
        ''' Подсчитывает средние и ожидаемые значения
        '''
        for i in range(len(self.statistic['ind_out'])):
            self.meta_statistic['avr_max_min'] += self.statistic['delta_max_min'][i]
            if self.statistic['delta_price'][i] < 0:
                self.meta_statistic['count_lesion'] += 1
                self.meta_statistic['avr_lesion'] += self.statistic['delta_price'][i]
            elif self.statistic['delta_price'][i] > 0:
                self.meta_statistic['count_profit'] += 1
                self.meta_statistic['avr_profit'] += self.statistic['delta_price'][i]

            self.meta_statistic['avr_potencial'] += self.statistic['delta_potencial'][i]
            self.meta_statistic['total'] += self.statistic['delta_price'][i]

        if self.meta_statistic['avr_max_min'] > 0:
            self.meta_statistic['avr_max_min'] = self.meta_statistic['avr_max_min'] / len(self.statistic['delta_max_min'])

        if self.meta_statistic['count_lesion'] > 0:
            self.meta_statistic['avr_lesion'] = self.meta_statistic['avr_lesion'] / self.meta_statistic['count_lesion']

        if self.meta_statistic['count_profit'] > 0:
            self.meta_statistic['avr_profit'] = self.meta_statistic['avr_profit'] / self.meta_statistic['count_profit']

        if len(self.statistic['ind_out']) > 0:
            self.meta_statistic['avr_all'] = self.meta_statistic['total'] / len(self.statistic['ind_out'])

        if len(self.statistic['ind_out']) > 0:
            self.meta_statistic['avr_potencial'] = self.meta_statistic['avr_potencial'] / len(self.statistic['ind_out'])

        self.meta_statistic['count_all'] = len(self.statistic['ind_out'])

    def check(self, *args, **kwargs):
        ''' Считает всю статистику
        '''
        self._get_statistic()
        self._get_meta_statistic()

    def print_statistic(self, view_all_rows=False):
        ''' Вывод в консоль статистики и мета статистики
            view_all_rows - Выводить все строки
        '''
        if view_all_rows:
            pd.set_option("display.max_rows", None)
        else:
            pd.set_option("display.max_rows", 10)

        statistic = pd.DataFrame.from_dict(self.statistic)
        # statistic = statistic.drop(columns=['ind_in', 'ind_out'])
        print('\n', statistic, '\n')
        for key, value in self.meta_statistic.items():
            print(key, ' = ', value)

    def write_meta_statistic(self, path):
        ''' Пишет статистику в файл
        '''
        with open(path, 'a', encoding='utf-8') as file:

            string = '{:^4} {:^4} {:^12} {:^10} {:^12} {:^10} {:^9} {:^5} {:^7} {:^13}'
            string = string.format(self.Nmin, self.Nmax, str(self.meta_statistic['count_lesion'])[:5], str(self.meta_statistic['avr_lesion'])[:5],
                                   str(self.meta_statistic['count_profit'])[:5], str(self.meta_statistic['avr_profit'])[:5],
                                   str(self.meta_statistic['count_all'])[:5], str(self.meta_statistic['total'])[:5],
                                   str(self.meta_statistic['avr_all'])[:5], str(self.meta_statistic['avr_potencial'])[:5])

            file.write(string  + '\n')

    def check_potential_correlation(self):
        r = 0
        numerator = 0
        denominator = 0
        for i in range(len(self.statistic['ind_out'])):
            numerator += (self.statistic['delta_potencial'][i]-self.meta_statistic['avr_potencial']) * \
                                (self.statistic['delta_max_min'][i]-self.meta_statistic['avr_max_min'])
            denominator += math.sqrt(math.pow(self.statistic['delta_potencial'][i]-self.meta_statistic['avr_potencial'], 2) * \
                                math.pow(self.statistic['delta_max_min'][i]-self.meta_statistic['avr_max_min'] , 2))

        r = numerator / denominator
        print('correlation = ', r)


class TheoryBase(TheoryStatistic):
    ''' Базовый класс Теория для наследования c логикой покупки и продажи
        а также возможностью получения статистики
    '''
    def __init__(self, _data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = _data

    def buy(self, ind):
        ''' Операция покупки
        '''
        self.ready_to_buy = False
        self.statistic['ind_in'].append(ind)
        self.statistic['point_in'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_in'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))

    def sell(self, ind):
        ''' Операция продажи
        '''
        self.ready_to_buy = True
        self.statistic['ind_out'].append(ind)
        self.statistic['point_out'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_out'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))


class TheoryQuickGrowth(TheoryBase):
    ''' Проверка теории покупки при резком скачке и продаже при резком падении
    '''

    def __init__(self, *args, Nmin=10, Nmax=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.Nmin = Nmin
        self.Nmax = Nmax

        self.lowest = []
        self.highest = []

        self.highest_indexes = []
        self.lowest_indexes = []

    def _get_min_values(self, ind):
        ''' Получение минимальных значений в промежутке
        '''
        sind = ind-self.Nmin
        sind = 0 if sind < 0 else sind
        find = ind
        min_value = min(self.data['<LOW>'][sind:find])
        self.lowest.append(min_value)

    def _get_max_values(self, ind):
        ''' Получение максимальных значений в промежутке
        '''
        sind = ind-self.Nmax
        sind = 0 if sind < 0 else sind
        find = ind
        max_value = max(self.data['<HIGH>'][sind:find])
        self.highest.append(max_value)

    def _get_extremum_values(self, ind):
        ''' Получение минимального и максимального значения в промежутке
            относительно индекса
        '''
        self._get_min_values(ind)
        self._get_max_values(ind)

    def _get_highest_lowest_indexes(self, ind):
        ''' Получение индекса покупки и продажи
        '''
        if ind > 0:
            if self.ready_to_buy:
                if self.data['<CLOSE>'][ind] > self.highest[ind-1]:
                    self.highest_indexes.append(ind)
            else:
                if self.data['<CLOSE>'][ind] < self.lowest[ind-1]:
                    self.lowest_indexes.append(ind)

    def check(self, *args, **kwargs):
        ''' Проверка теории
        '''
        self.ready_to_buy = True
        for ind in range(1, len(self.data['<CLOSE>'])):

            self._get_extremum_values(ind)
            self._get_highest_lowest_indexes(ind)

            if self.ready_to_buy and ind in self.highest_indexes:
                self.buy(ind)

            elif not self.ready_to_buy and ind in self.lowest_indexes:
                self.sell(ind)

        super().check(*args, **kwargs)


def main():

    LDATA = [GAZP_PATH_MIN, GAZP_PATH_5MIN, GAZP_PATH_HOUR]
    # for data_path in LDATA:
    data = get_standartized_data(path=GAZP_PATH_HOUR)
    theory = TheoryQuickGrowth(data, Nmin=20, Nmax=10)
    theory.check()
    theory.print_statistic()
    theory.check_potential_correlation()

    # plt.plot(theory.statistic['delta_potencial'])
    # plt.show()
    #
    # plt.plot(theory.statistic['delta_max_min'])
    # plt.show()
    #
    # plt.plot(theory.statistic['delta_max_min'], theory.statistic['delta_potencial'])
    # plt.show()


if __name__ == '__main__':
    main()
