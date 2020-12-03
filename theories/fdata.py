import copy
from settings import DATA_DIR


FINAM_DATA_DIR = DATA_DIR


class FURLBuilder:
    def build_url(self):
        pass


class FPathBuilder:
    def build_path(self):
        pass


class FDownloader:
    def save_file(self, file):
        pass

    def get_file(self):
        pass

    def download_file(self):
        pass


class FData:

    PERIODS = ['month','week','day','hour','30min','15min','10min','5min','1min']
    TICKERS = ['GAZP', 'ACM', 'MAGN'] # Сделать подгрузку из файла
    MARKETS = []  # Сделать автоматическое определение биржи

    def __init__(self, *args, **kwargs):
        self.period = kwargs.get('period', None)
        self.date_end = kwargs.get('date_end', None)
        self.date_begin = kwargs.get('date_begin', None)
        self.ticker = kwargs.get('ticker', None)
        self.temp_date = kwargs.get('temp_date', None)

    def __getitem__(self, key):
        copy_fdata = self.copy()
        if key in self.PERIODS:
            copy_fdata.period = key
        elif key in self.TICKERS:
            copy_fdata.ticker = key
        else:
            copy_fdata.temp_date = key
        return copy_fdata

    def __str__(self):
        return str(self.period) + ' ' + str(self.ticker) + ' ' + str(self.temp_date)

    def copy(self):
        return copy.copy(self)



''' ЗАДАЧИ '''
'''
1) Написать расшифрование даты их строки
2) Реализовать сравнений дат для определения в дату начала и дату конца
3) Сделать автоматическую подгузку тикеров из файла
4) Сделать автоматическое определение биржи
5) Реализовать поиск по папкам на основе параметров
6) Реализовать загрузку в нужную папку на основе параметров
7) Реализовать слайсинг по датам в существующих файлах
8) ...

'''
