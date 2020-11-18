import pandas as pd
import datetime
import matplotlib.dates as dates
from services import get_standartized_data


class TheoryBase:
    ''' Базовый класс Теория для наследования
    '''

    def __init__(self, _data, N=10):
        self.data = _data
        self.N = N

    def __str__(self):
        return ''


class TheoryQuickGrowth(TheoryBase):
    statistic = {
        'ind_in': [],
        'ind_out': [],
        'point_in': [],
        'point_out': [],
        'delta_price': [],
        'time_in': [],
        'time_out': [],
        'delta_time': [],
        'potencial': []
    }
    highest_indexes = []
    lowest_indexes = []

    def get_values_in_range(self, data, function):
        values = []
        for i in range(len(data)):
            if i <= self.N:
                values.append(function(data[:i+1]))
            else:
                values.append(function(data[i-n:i+1]))
        return values


    def get_min_max_values(self, sind, find):
        max_values = self.get_values_in_range(self.data['<HIGH>'][sind:find], max)
        min_values = self.get_values_in_range(self.data['<LOW>'][sind:find], min)

        return min_values, max_values


    def get_highest_lowest_indexes(self, lowest, highest, sind, find):

        for index, value in enumerate(self.data['<CLOSE>'][sind:find]):
            if value < lowest[index-1]:
                if index+sind not in self.lowest_indexes:
                    self.lowest_indexes.append(index+sind)
            elif value > highest[index-1]:
                if index+sind not in self.highest_indexes:
                    self.highest_indexes.append(index+sind)



    def check(self):
        self.ready_to_buy = True
        for ind in range(len(self.data)):
            min_values, max_values = self.get_min_max_values(ind, ind+self.N)
            self.get_highest_lowest_indexes(min_values, max_values, ind, ind+self.N)

            if self.ready_to_buy and ind in self.highest_indexes:
                self.buy(ind)

            elif not self.ready_to_buy and ind in self.lowest_indexes:
                self.sell(ind)


    def buy(self, ind):
        self.ready_to_buy = False
        self.statistic['ind_in'].append(ind)
        self.statistic['point_in'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_in'].append(dates.num2date(self.data['DATE'][ind]))


    def sell(self, ind):
        self.ready_to_buy = True
        self.statistic['ind_out'].append(ind)
        self.statistic['point_out'].append(self.data['<CLOSE>'][ind])
        self.statistic['time_out'].append(dates.num2date(self.data['DATE'][ind]))


    def count_potencial(self, ind_in, ind_out):
        return 0


    def get_statistic(self):
        for i in range(len(self.statistic['ind_out'])):
            self.statistic['delta_price'].append(self.statistic['point_out'][i] - self.statistic['point_in'][i])
            self.statistic['delta_time'].append((self.statistic['time_out'][i] - self.statistic['time_in'][i]).seconds / 60)
            self.statistic['potencial'].append(self.count_potencial(self.statistic['ind_in'], self.statistic['ind_out']))


    def print_statistic(self):
        min_len = len(self.statistic['ind_out'])
        self.get_statistic()
        pd.set_option("display.max_rows", None)

        for key, value in self.statistic.items():
            self.statistic[key] = self.statistic[key][:min_len]

        statistic = pd.DataFrame.from_dict(self.statistic)
        print(statistic)


data = get_standartized_data()
theory = TheoryQuickGrowth(data)
theory.check()
theory.print_statistic()
