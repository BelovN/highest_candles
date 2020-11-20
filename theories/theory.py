import os
import pandas as pd
import datetime
import matplotlib.dates as dates
from services import get_standartized_data
from settings import OUTPUT_FILE_DIR


class TheoryBase:
    ''' Базовый класс Теория для наследования
    '''

    def __init__(self, _data, Nmin=10, Nmax=10):
        self.data = _data
        self.Nmin = Nmin
        self.Nmax = Nmax

    def __str__(self):
        return ''


class TheoryQuickGrowth(TheoryBase):
    statistic = {
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
    }

    meta_statistic = {
        'count_lesion': 0,
        'avr_lesion': 0,
        'count_profit': 0,
        'avr_profit': 0,
        'count_all': 0,
        'total': 0,
        'avr_all': 0,
        'avr_potencial': 0,
    }

    highest_indexes = []
    lowest_indexes = []
    lowest = []
    highest = []


    def get_min_values(self, sind, find):
        min_value = min(self.data['<LOW>'][sind:find])
        self.lowest.append(min_value)

    def get_max_values(self, sind, find):
        max_value = max(self.data['<HIGH>'][sind:find])
        self.highest.append(max_value)

    def get_min_max_values(self, ind):
        if sind < 0:
            sind = 0
        if find > 0:
            get_min_values(ind-self.Nmin, find)
            get_max_values(ind-self.Nmax, find)


    def get_highest_lowest_indexes(self, ind):
        if ind > 0:
            if self.data['<CLOSE>'][ind] > self.highest[ind-1]:
                self.highest_indexes.append(ind)

            if self.data['<CLOSE>'][ind] < self.lowest[ind-1]:
                self.lowest_indexes.append(ind)


    def check(self):
        # import pdb; pdb.set_trace()
        self.ready_to_buy = True
        for ind in range(1, len(self.data['<CLOSE>'])):

            self.get_min_max_values(ind)
            self.get_highest_lowest_indexes(ind)

            if self.ready_to_buy and ind in self.highest_indexes:
                self.buy(ind)

            elif not self.ready_to_buy and ind in self.lowest_indexes:
                self.sell(ind)


    def buy(self, ind):
        self.ready_to_buy = False
        self.statistic['ind_in'].append(ind)
        self.statistic['point_in'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_in'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))


    def sell(self, ind):
        self.ready_to_buy = True
        self.statistic['ind_out'].append(ind)
        self.statistic['point_out'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_out'].append(dates.num2date(self.data['DATE'][ind]).strftime('%d.%m %H:%M'))


    def count_potencial(self, ind_in, ind_out):
        return max(self.data['<CLOSE>'][ind_in+1:ind_out+1])


    def get_statistic(self):
        for i in range(len(self.statistic['ind_out'])):
            ind_in = self.statistic['ind_in'][i]
            ind_out = self.statistic['ind_out'][i]
            date_in = dates.num2date(self.data['DATE'][ind_in])
            date_out = dates.num2date(self.data['DATE'][ind_out])

            self.statistic['delta_price'].append(self.statistic['point_out'][i] - self.statistic['point_in'][i])
            self.statistic['delta_time'].append((date_out - date_in).seconds / 60)
            self.statistic['potencial'].append(self.count_potencial(self.statistic['ind_in'][i], self.statistic['ind_out'][i]))
            self.statistic['delta_potencial'].append(self.statistic['potencial'][i] - self.statistic['point_in'][i])


        min_len = len(self.statistic['ind_out'])
        for key, value in self.statistic.items():
            self.statistic[key] = self.statistic[key][:min_len]


    def get_meta_statistic(self):

        for i in range(len(self.statistic['ind_out'])):
            if self.statistic['delta_price'][i] < 0:
                self.meta_statistic['count_lesion'] += 1
                self.meta_statistic['avr_lesion'] += self.statistic['delta_price'][i]
            elif self.statistic['delta_price'][i] > 0:
                self.meta_statistic['count_profit'] += 1
                self.meta_statistic['avr_profit'] += self.statistic['delta_price'][i]

            self.meta_statistic['avr_potencial'] += self.statistic['delta_potencial'][i]
            self.meta_statistic['total'] += self.statistic['delta_price'][i]

        self.meta_statistic['avr_lesion'] = self.meta_statistic['avr_lesion'] / self.meta_statistic['count_lesion']
        self.meta_statistic['avr_profit'] = self.meta_statistic['avr_profit'] / self.meta_statistic['count_profit']
        self.meta_statistic['avr_all'] = self.meta_statistic['total'] / len(self.statistic['ind_out'])
        self.meta_statistic['avr_potencial'] = self.meta_statistic['avr_potencial'] / len(self.statistic['ind_out'])
        self.meta_statistic['count_all'] = len(self.statistic['ind_out'])


    def print_statistic(self):
        self.get_statistic()
        self.get_meta_statistic()

        # pd.set_option("display.max_rows", None)

        statistic = pd.DataFrame.from_dict(self.statistic)
        # statistic = statistic.drop(columns=['ind_in', 'ind_out'])
        print(statistic)
        print()

        for key, value in self.meta_statistic.items():
            print(key, ' = ', value)


    def write_meta_statistic(self, path):
        self.get_statistic()
        self.get_meta_statistic()
        with open(path, 'a', encoding='utf-8') as file:

            string = '{:^2} {:^2} {:^12} {:^10} {:^12} {:^10} {:^9} {:^5} {:^7} {:^13}'
            string = string.format(self.Nmin, self.Nmax, str(self.meta_statistic['count_lesion'])[:5], str(self.meta_statistic['avr_lesion'])[:5],
                                   str(self.meta_statistic['count_profit'])[:5], str(self.meta_statistic['avr_profit'])[:5],
                                   str(self.meta_statistic['count_all'])[:5], str(self.meta_statistic['total'])[:5],
                                   str(self.meta_statistic['avr_all'])[:5], str(self.meta_statistic['avr_potencial'])[:5])

            file.write(string  + '\n')



count = 20000
data = get_standartized_data(count=count)

theory = TheoryQuickGrowth(data, Nmin=30, Nmax=60)
theory.check()
theory.write_meta_statistic(OUTPUT_FILE_DIR)


# for i in range(5, 65, 5):
#     count = 10000
#     data = get_standartized_data(count=count)
#
#     theory = TheoryQuickGrowth(data, N=i)
#     theory.check()
#     theory.write_meta_statistic(OUTPUT_FILE_DIR)

# for i in range(5, 65, 5):
#     theory = TheoryQuickGrowth(data, N=i)
#     theory.check()
#     theory.write_meta_statistic(OUTPUT_FILE_DIR)
#     theories.append(theory)
# theory.print_statistic()
#
#
# print(count)
#
# f = open(OUTPUT_FILE_DIR, 'w')
# f.close()
#
#
# theories = []
# for i in range(10, 65, 5):
#     theory = TheoryQuickGrowth(data, N=i)
#     theory.check()
#     theory.write_meta_statistic(OUTPUT_FILE_DIR)
#     theories.append(theory)
#
# print('Ready!')
