from datetime import datetime
import matplotlib.dates as dates
import pandas as pd

from settings import GAZP_PATH


def convert_datetime(data):
    ''' Конвертирует колонки <DATE> и <TIME> в числовой формат для обображения
    '''
    indexes = []
    for i, date in enumerate(data['<DATE>']):
        full_date = str(data['<DATE>'][i]) + str(data['<TIME>'][i])
        converted_date = datetime.strptime(full_date, '%Y%m%d%H%M%S')
        indexes.append(converted_date)

    indexes = dates.date2num(indexes)
    return indexes


def standartize_data(data):
    ''' Удаление лилних колонок и добавление единой колонки DATE (дата и время)
    '''
    DATE = convert_datetime(data)
    data = data.drop(columns=['<DATE>', '<TIME>', '<PER>', '<VOL>', '<TICKER>'])
    data = data.assign(DATE=DATE)
    return data


def load_csv(path=GAZP_PATH, sep=';',  encoding='utf-8', count=10000):
    ''' Загрузка данных из csv файла
    '''

    data = pd.read_csv(path, sep=sep, encoding=encoding)
    data = data.loc[:count]

    return data


def get_standartized_data(count=10000):
    ''' Считывание и обработка данных
    '''
    data = load_csv(count=count)
    standartized_data = standartize_data(data)
    return standartized_data


def format_data_to_tuple(data):
    ''' Форматирует данные в список кортежей
    '''
    data_tuples = [tuple([data['DATE'][i],
                     data['<OPEN>'][i],
                     data['<HIGH>'][i],
                     data['<LOW>'][i],
                     data['<CLOSE>'][i]]) for i in range(len(data))]
    return data_tuples


def get_tuppled_data():
    ''' Внешняя интерфейсная функция для быстрого получения данных для отображения
    '''
    data = get_standartized_data()
    data_tuples = format_data_to_tuple(data)

    return data_tuples
