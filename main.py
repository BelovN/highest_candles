import csv
import os
import time
import pandas as pd
import numpy as np
import matplotlib.style
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as dates

from datetime import datetime
from matplotlib import ticker
from mplfinance.original_flavor import candlestick_ohlc


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
GAZP_PATH = os.path.join(DATA_DIR, 'GAZP_200101_201112.csv')

N = 20


def convert_datetime(data):
    indexes = []
    for i, date in enumerate(data['<DATE>']):
        full_date = str(data['<DATE>'][i]) + str(data['<TIME>'][i])
        converted_date = datetime.strptime(full_date, '%Y%m%d%H%M%S')
        indexes.append(converted_date)

    indexes = mpl.dates.date2num(indexes)

    return indexes


def load_csv(path=GAZP_PATH, count=1000):
    gazp_data = pd.read_csv(GAZP_PATH, sep=';', encoding='utf-8')

    gazp_data = gazp_data.loc[:count]
    date = convert_datetime(gazp_data)
    gazp_data = gazp_data.drop(columns=['<DATE>', '<TIME>', '<PER>', '<VOL>', '<TICKER>'])
    gazp_data = gazp_data.assign(INDEX=date)

    return gazp_data


def get_highest_lowest_indexes(data, lowest, highest):
    highest_indexes = []
    lowest_indexes = []
    for index, value in enumerate(data['<CLOSE>']):
        if index > 0:
            if value < lowest[index-1]:
                lowest_indexes.append(index)
            elif value > highest[index-1]:
                highest_indexes.append(index)

    return lowest_indexes, highest_indexes


def get_values_in_range(data, n, function):
    values = []
    for i in range(len(data)):
        if i <= n:
            values.append(function(data[:i+1]))
        else:
            values.append(function(data[i-n:i+1]))
    return values


def get_min_max_values(data):
    max_values = get_values_in_range(data['<HIGH>'], N, max)
    min_values = get_values_in_range(data['<LOW>'], N, min)

    return min_values, max_values


def vizualize_highest_lowest(min_values, max_values, indexes, ax):
    data_min = pd.DataFrame(min_values, index=indexes, columns=["min_values"])
    data_max = pd.DataFrame(max_values, index=indexes, columns=["max_values"])

    data_min_float = data_min.astype(float)
    data_max_float = data_max.astype(float)

    data_min_float["min_values"].plot(ax=ax, color='black')
    data_max_float["max_values"].plot(ax=ax, color='black')


def vizualize_extremum(indexes, extremum_values, data_values, data_indexes, ax):
    for index in indexes:
        line_y = [extremum_values[index-1], data_values[index]]
        line_x = [data_indexes[index-1], data_indexes[index]]
        line_data = pd.DataFrame(line_y, index=line_x, columns=[str(index)]).astype(float)
        line_data[str(index)].plot(kind='line', color='yellow', ax=ax)


def format_data_to_tuple(data):
    data_tuples = [tuple([data['INDEX'][i],
                     data['<OPEN>'][i],
                     data['<HIGH>'][i],
                     data['<LOW>'][i],
                     data['<CLOSE>'][i]]) for i in range(len(data))]
    return data_tuples


def vizualize_candles(data, ax):
    tuples_data = format_data_to_tuple(data)
    candlestick_ohlc(ax, tuples_data, width=0.0005, colorup='g', colordown='r', alpha=0.8)

    ax.xaxis.set_major_formatter(dates.DateFormatter('%d.%m.%Y %H:%M'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))

    plt.xticks(rotation = 30)
    plt.grid()
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.tight_layout()
    plt.show()


def main():
    data = load_csv()


    min_values, max_values = get_min_max_values(data)
    values_lowest_indexes, values_highest_indexes = get_highest_lowest_indexes(data, min_values, max_values)

    fig, ax = plt.subplots()
    vizualize_highest_lowest(min_values, max_values, data['INDEX'], ax)
    vizualize_extremum(values_highest_indexes, max_values, data['<CLOSE>'], data['INDEX'], ax)
    vizualize_extremum(values_lowest_indexes, min_values, data['<CLOSE>'], data['INDEX'], ax)
    vizualize_candles(data, ax)


if __name__ == '__main__':
    main()
