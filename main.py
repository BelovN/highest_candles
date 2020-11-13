import csv
import os
import time
import pandas as pd
import numpy as np
import matplotlib.style
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib import ticker

from datetime import datetime
from mplfinance.original_flavor import candlestick_ohlc


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
GAZP_PATH = os.path.join(DATA_DIR, 'GAZP_200101_201112.csv')
# <TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>

N = 10


def load_csv(path=GAZP_PATH, count=500):
    gazp_data = pd.read_csv(GAZP_PATH, sep=';', encoding='utf-8')
    gazp_data = gazp_data.drop(['<VOL>', '<TICKER>'], axis=1)
    gazp_data = gazp_data[:count]
    return gazp_data


def format_data_to_tuple(data):
    indexes = []
    for i, date in enumerate(data['<DATE>']):
        full_date = str(data['<DATE>'][i]) + str(data['<TIME>'][i])
        converted_date = datetime.strptime(full_date, '%Y%m%d%H%M%S')
        indexes.append(converted_date)


    indexes = mpl.dates.date2num(indexes)

    quotes = [tuple([indexes[i],
                     data['<OPEN>'][i],
                     data['<HIGH>'][i],
                     data['<LOW>'][i],
                     data['<CLOSE>'][i]]) for i in range(len(data))]
    return quotes


def get_values_in_range(data, n, function):
    values = []
    for i in range(len(data)):
        if i <= n:
            values.append(function(data[:i+1]))
        else:
            values.append(function(data[i-n:i+1]))

    return values


def build_candles(data, data_candles):
    fig, ax = plt.subplots()
    candlestick_ohlc(ax, data_candles, width=0.0005, colorup='g', colordown='r', alpha=0.8)

    ax.xaxis.set_major_formatter(dates.DateFormatter('%d.%m.%Y %H:%M'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))

    highs = data['<HIGH>']
    lows = data['<LOW>']
    indexes = [data_candles[i][0] for i in range(len(data_candles))]

    

    max_values = get_values_in_range(highs, N, max)
    min_values = get_values_in_range(lows, N, min)

    data_min = pd.DataFrame(min_values, index=indexes, columns=["min_values"]) #_2
    data_max = pd.DataFrame(max_values, index=indexes, columns=["max_values"]) #_2
    data_min = data_min.astype(float)
    data_max = data_max.astype(float)

    data_min["min_values"].plot(ax=ax)
    data_max["max_values"].plot(ax=ax)


    plt.xticks(rotation = 30)
    plt.grid()
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.tight_layout()
    plt.show()


data = load_csv()
formated_data = format_data_to_tuple(data)
build_candles(data, formated_data)


# if __name__ == '__main__':
#     main()
