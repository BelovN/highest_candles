import matplotlib.dates as dates
import pandas as pd

from datetime import datetime

from settings import *


def convert_datetime(data):
    ''' Конвертирует колонки <DATE> и <TIME> в числовой формат для обображения
    '''
    indexes = []
    converted_dates = []
    for i, date in enumerate(data['<DATE>']):
        if str(data['<TIME>'][i]) == '0':
            full_date = str(data['<DATE>'][i]) + '000000'
        else:
            full_date = str(data['<DATE>'][i]) + str(data['<TIME>'][i])
        converted_date = datetime.strptime(full_date, '%Y%m%d%H%M%S')
        indexes.append(converted_date)
        converted_dates.append(converted_date)
    indexes = dates.date2num(indexes)
    return indexes, converted_dates


def standartize_data(data):
    ''' Удаление лилних колонок и добавление единой колонки DATE (дата и время)
    '''
    DATE, CONVERTED_DATE = convert_datetime(data)
    data = data.assign(CONVDATE=CONVERTED_DATE)
    # data = data.drop(columns=['<DATE>', '<TIME>', '<PER>', '<VOL>', '<TICKER>'])
    data = data.drop(columns=[ '<PER>', '<VOL>', '<TICKER>'])
    data = data.assign(DATE=DATE)
    return data


def load_csv(path=GAZP_PATH_MIN_2020, sep=';',  encoding='utf-8', count=None):
    ''' Загрузка данных из csv файла
    '''
    data = pd.read_csv(path, sep=sep, encoding=encoding)
    if count is not None:
        data = data.loc[:count]

    return data


def get_standartized_data(path=GAZP_PATH_MIN_2020, count=None):
    ''' Считывание и обработка данных
    '''
    data = load_csv(path=path, count=count)
    standartized_data = standartize_data(data)
    return standartized_data


def format_data_to_tuple(data):
    ''' Форматирует данные в список кортежей
    '''
    data_tuples = [tuple([i,
                     data['<OPEN>'][i],
                     data['<HIGH>'][i],
                     data['<LOW>'][i],
                     data['<CLOSE>'][i]]) for i in range(len(data))]

    return data_tuples


def get_tuppled_data(path=GAZP_PATH_HOUR_2018, count=None):
    ''' Внешняя интерфейсная функция для быстрого получения данных для отображения
    '''
    data = get_standartized_data(path=path, count=count)
    data_tuples = format_data_to_tuple(data)

    return data_tuples


def remove_evening_session(data):
    ''' Удаляет вечерние сессии
    '''
    indexes = []
    for index, row in data.iterrows():

        if row['<TIME>'] >= 190000 or row['<TIME>'] == 0:
            indexes.append(index)

    data = data.drop(data.index[indexes])
    data.index = range(len(data))
    return data
