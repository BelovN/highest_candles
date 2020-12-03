import datetime
import math
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import os
import pandas as pd

from services import get_standartized_data
from settings import *


class TheoryStatistic:
    ''' Класс для сбора статистики
    '''
    STATUS = {
        'NOTHING': 0,
        'SHORT': 1,
        'LONG': 2,
    }

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
            'status': [],
        }
        self.meta_statistic = {
            'count_lesion': 0,
            'avr_lesion': 0,
            'count_profit': 0,
            'avr_profit': 0,
            'count_all': 0,
            'sum_lesion': 0,
            'sum_profit': 0,
            'P/L': 0,
            'total': 0,
            'total_short': 0,
            'total_long': 0,
            'avr_all': 0,
            'avr_potencial': 0,
            'avr_max_min': 0,
        }

    def _get_additional_statistic(self):
        ''' Метод подсчета дополнительной статистики для переопределения потомком
        '''
        return

    def _get_additional_metastatistic(self):
        ''' Метод подсчета дополнительной метастатистики для переопределения потомком
        '''
        return

    def _get_statistic(self):
        ''' Подсчитывает дельта статистику
        '''
        min_len = len(self.statistic['ind_out'])

        for key, value in self.statistic.items():
            self.statistic[key] = self.statistic[key][:min_len-1]
        for i in range(len(self.statistic['ind_out'])):
            ind_in = self.statistic['ind_in'][i]
            ind_out = self.statistic['ind_out'][i]
            date_in = dates.num2date(self.data['DATE'][ind_in])
            date_out = dates.num2date(self.data['DATE'][ind_out])

            if self.statistic['status'][i] == self.STATUS['LONG']:
                self.statistic['delta_price'].append(self.statistic['point_out'][i] - self.statistic['point_in'][i])
                self.statistic['delta_time'].append((date_out - date_in).seconds / 60)

                self.statistic['potencial'].append(max(self.data['<CLOSE>'][ind_in:ind_out]))
                self.statistic['delta_potencial'].append(self.statistic['potencial'][i] - self.statistic['point_in'][i])

            if self.statistic['status'][i] == self.STATUS['SHORT']:
                self.statistic['delta_price'].append(self.statistic['point_in'][i] - self.statistic['point_out'][i])
                self.statistic['delta_time'].append((date_out - date_in).seconds / 60)

                self.statistic['potencial'].append(min(self.data['<CLOSE>'][ind_in:ind_out]))
                self.statistic['delta_potencial'].append(self.statistic['point_in'][i] - self.statistic['potencial'][i])

            self.statistic['delta_max_min'].append(self.highest[i] - self.lowest[i])

        self._get_additional_statistic()

    def _get_meta_statistic(self):
        ''' Подсчитывает средние и ожидаемые значения
        '''
        self.meta_statistic['Nmin'] = self.Nmin
        self.meta_statistic['Nmax'] = self.Nmax
        for i in range(len(self.statistic['ind_out'])):
            self.meta_statistic['avr_max_min'] += self.statistic['delta_max_min'][i]
            if self.statistic['delta_price'][i] < 0:
                self.meta_statistic['count_lesion'] += 1
                self.meta_statistic['sum_lesion'] += self.statistic['delta_price'][i]
            elif self.statistic['delta_price'][i] > 0:
                self.meta_statistic['count_profit'] += 1
                self.meta_statistic['sum_profit'] += self.statistic['delta_price'][i]

            if self.statistic['status'][i] == self.STATUS['LONG']:
                self.meta_statistic['total_long'] += self.statistic['delta_price'][i]
            elif self.statistic['status'][i] == self.STATUS['SHORT']:
                self.meta_statistic['total_short'] += self.statistic['delta_price'][i]

            self.meta_statistic['avr_potencial'] += self.statistic['delta_potencial'][i]
            self.meta_statistic['total'] += self.statistic['delta_price'][i]

        if self.meta_statistic['avr_max_min'] > 0: # Средняя разница между max и min
            self.meta_statistic['avr_max_min'] = self.meta_statistic['avr_max_min'] / len(self.statistic['delta_max_min'])

        if self.meta_statistic['count_lesion'] > 0: # Средний убыток за сделку
            self.meta_statistic['avr_lesion'] = self.meta_statistic['sum_lesion'] / self.meta_statistic['count_lesion']

        if self.meta_statistic['count_profit'] > 0: # Средняя прибыль за сделку
            self.meta_statistic['avr_profit'] = self.meta_statistic['sum_profit'] / self.meta_statistic['count_profit']

        if len(self.statistic['ind_out']) > 0: # Матожидание одной сделки
            self.meta_statistic['avr_all'] = self.meta_statistic['total'] / len(self.statistic['ind_out'])

        if len(self.statistic['ind_out']) > 0: # Средний потенциал
            self.meta_statistic['avr_potencial'] = self.meta_statistic['avr_potencial'] / len(self.statistic['ind_out'])

        self.meta_statistic['count_all'] = len(self.statistic['ind_out']) # Количество сделок
        self.meta_statistic['P/L'] = abs(self.meta_statistic['sum_profit'] / self.meta_statistic['sum_lesion']) # Прибыль на убыток

        self._get_additional_metastatistic()

    def check(self, *args, **kwargs):
        ''' Считает всю статистику
        '''
        self._get_statistic()
        self._get_meta_statistic()

    def write_statistic(self, path=OUTPUT_DIR):
        df = pd.DataFrame.from_dict(self.statistic)
        with open(os.path.join(OUTPUT_DIR, 'statistic.csv'), 'w', encoding='utf-8') as file:
            df.to_csv(file, index=False, header=True, sep=';', float_format='%.3f', decimal=',')


    def print_metastatistic(self):
        for key, value in self.meta_statistic.items(): # Вывод метастатистики
            print(key, ' = ', value)

    def print_statistic(self, view_all_rows=None):
        ''' Вывод в консоль статистики и мета статистики
            view_all_rows - Выводить все строки
        '''
        pd.set_option("display.max_rows", view_all_rows)
        statistic = pd.DataFrame.from_dict(self.statistic)
        print('\n', statistic, '\n') # Вывод статистики

    def print_full_statistic(self, view_all_rows=None):
        self.print_statistic(view_all_rows=view_all_rows)
        self.print_metastatistic()

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


class TheoryBase(TheoryStatistic):
    ''' Базовый класс Теория для наследования c логикой покупки и продажи
        а также возможностью получения статистики
    '''

    def __init__(self, _data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = _data
        self.status = self.STATUS['NOTHING']

    def open_long(self, ind):
        ''' Открытие long
        '''
        self.status = self.STATUS['LONG']
        self.statistic['ind_in'].append(ind+1)
        self.statistic['point_in'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_in'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))

    def close_long(self, ind):
        ''' Закрытие long
        '''
        self.status = self.STATUS['NOTHING']
        self.statistic['ind_out'].append(ind+1)
        self.statistic['point_out'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_out'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))
        self.statistic['status'].append(self.STATUS['LONG'])

    def open_short(self, ind):
        ''' Открытие short
        '''
        self.status = self.STATUS['SHORT']
        self.statistic['ind_in'].append(ind+1)
        self.statistic['point_in'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_in'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))

    def close_short(self, ind):
        ''' Закрытие short
        '''
        self.status = self.STATUS['NOTHING']
        self.statistic['ind_out'].append(ind+1)
        self.statistic['point_out'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_out'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))
        self.statistic['status'].append(self.STATUS['SHORT'])


class TheoryQuickGrowth(TheoryBase):
    ''' Проверка теории покупки при резком скачке и продаже при резком падении
    '''

    def __init__(self, *args, Nmin=10, Nmax=10, deals=None, lowest=None, highest=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.Nmin = Nmin
        self.Nmax = Nmax

        if deals is not None:
            self.deals = deals
        else:
            self.deals = []

        if lowest is not None:
            self.lowest = lowest
        else:
            self.lowest = []

        if highest is not None:
            self.highest = highest
        else:
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
            if self.status == self.STATUS['SHORT'] or self.status == self.STATUS['NOTHING']:
                if self.data['<CLOSE>'][ind] >= self.highest[ind-1]:
                    self.highest_indexes.append(ind)
            elif self.status == self.STATUS['LONG'] or self.status == self.STATUS['NOTHING']:
                if self.data['<CLOSE>'][ind] <= self.lowest[ind-1]:
                    self.lowest_indexes.append(ind)

    def check(self, deals=None, highest=None, lowest=None, *args, **kwargs):
        ''' Проверка теории
        '''

        for ind in range(1, len(self.data['<CLOSE>'])):

            self._get_extremum_values(ind)
            self._get_highest_lowest_indexes(ind)

            if self.status == self.STATUS['NOTHING']:
                if ind in self.highest_indexes:
                    self.open_long(ind)
                    self.deals.append(ind)
                if ind in self.lowest_indexes:
                    self.open_short(ind)
                    self.deals.append(ind)

            elif self.status == self.STATUS['SHORT']:
                if ind in self.highest_indexes:
                    self.close_short(ind)
                    self.open_long(ind)
                    self.deals.append(ind)

            elif self.status == self.STATUS['LONG']:
                if ind in self.lowest_indexes:
                    self.close_long(ind)
                    self.open_short(ind)
                    self.deals.append(ind)

            yield

    def full_check(self, *args, **kwargs):
        func = self.check(*args, **kwargs)
        while True:
            try:
                next(func)
            except:
                super().check(*args, **kwargs)
                break


def main():
    Nmin = 5
    Nmax = 5
    data = get_standartized_data(path=RTS_5YEARS_HOUR)
    theory = TheoryQuickGrowth(data, Nmin=Nmin, Nmax=Nmax)
    theory.full_check()

    theory.write_statistic()
    # theory.print_full_statistic(view_all_rows=10)


if __name__ == '__main__':
    main()
