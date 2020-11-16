import os
import pandas as pd
import matplotlib.dates as dates

from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
GAZP_PATH = os.path.join(DATA_DIR, 'GAZP_200101_201112.csv')


def convert_datetime(data):
    indexes = []
    for i, date in enumerate(data['<DATE>']):
        full_date = str(data['<DATE>'][i]) + str(data['<TIME>'][i])
        converted_date = datetime.strptime(full_date, '%Y%m%d%H%M%S')
        indexes.append(converted_date)

    indexes = dates.date2num(indexes)

    return indexes


def load_csv(path=GAZP_PATH, count=500):
    gazp_data = pd.read_csv(GAZP_PATH, sep=';', encoding='utf-8')
    gazp_data = gazp_data[:count]

    date = convert_datetime(gazp_data)
    gazp_data = gazp_data.drop(columns=['<DATE>', '<TIME>', '<PER>', '<VOL>', '<TICKER>'])
    gazp_data = gazp_data.assign(INDEX=date)

    return gazp_data


def format_data_to_tuple(data):
    data_tuples = [tuple([data['INDEX'][i],
                     data['<OPEN>'][i],
                     data['<HIGH>'][i],
                     data['<LOW>'][i],
                     data['<CLOSE>'][i]]) for i in range(len(data))]
    return data_tuples
