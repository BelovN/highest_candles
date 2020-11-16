import pandas as pd
import matplotlib.style
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib import ticker
from mplfinance.original_flavor import candlestick_ohlc

from statistic import get_min_max_values, get_highest_lowest_indexes


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


def view():
    data = load_csv()

    min_values, max_values = get_min_max_values(data)
    values_lowest_indexes, values_highest_indexes = get_highest_lowest_indexes(data, min_values, max_values)

    fig, ax = plt.subplots()
    vizualize_highest_lowest(min_values, max_values, data['INDEX'], ax)
    vizualize_extremum(values_highest_indexes, max_values, data['<CLOSE>'], data['INDEX'], ax)
    vizualize_extremum(values_lowest_indexes, min_values, data['<CLOSE>'], data['INDEX'], ax)
    vizualize_candles(data, ax)
