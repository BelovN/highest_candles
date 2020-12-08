import time
import matplotlib as mpl
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.patches as patches
from mplfinance.original_flavor import candlestick_ohlc

from settings import *
from services import format_data_to_tuple, get_standartized_data

mpl.use('Qt5Agg')


class BaseSettingsMixin:
    ''' Дефолтный класс для наследования классов настроек
    '''
    def _set_default_settings(self):
        ''' Дефолтные настройки
        '''
        return

    def _parse_settings(self, **kwargs):
        ''' Применяем внешние настройки
        '''
        if kwargs is not None:
            for value, key in kwargs.items():
                setattr(self, key, value)

    def set_up(self, **kwargs):
        ''' Настройка
        '''
        self._set_default_settings()
        if kwargs:
            self._parse_settings(kwargs)


class SettingsMixinView(BaseSettingsMixin):
    ''' Миксин класс для вынесения логики настроек
    '''

    def _setup_axis(self):
        ''' Настройка отображения осей
        '''
        self.ax.xaxis.set_major_formatter(dates.DateFormatter('%d.%m.%Y %H:%M'))
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(10))

        self.fig.canvas.mpl_connect('close_event', self.__on_close)
        self.ax.has_been_closed = False

        plt.xticks(rotation=30)
        plt.grid()
        plt.xlabel('Дата')
        plt.ylabel('Цена')
        plt.tight_layout()


    def _set_default_settings(self):
        ''' Стандартные настройки
        '''
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self._setup_axis()


    def __on_close(self, event):
        ''' Для завершения цикла при закрытии окна
        '''
        event.canvas.figure.axes[0].has_been_closed = True


class BaseViewCandles(SettingsMixinView):
    ''' Базовый класс для динамического отображения графика свечей
    '''

    def __init__(self, data, N=15, deals=[], highest=[], lowest=[], **kwargs):
        ''' Данные должны быть в формате списка кортежей из 5 состовляющих
        '''
        self.deals = deals
        self.highest = highest
        self.lowest = lowest
        self.data = data
        self.tuppled_data = format_data_to_tuple(self.data)
        self.N = N
        self.set_up(**kwargs) # Настройки

    def _date_ticker(self, x, pos):
        return self.data['CONVDATE'][int(x)] # Для корректоного вывода даты

    def _show_algorithm(self, *args, **kwargs):
        ''' Функция для отображения алгоритмов
        '''
        return

    def _color_deals(self, ind, i, lines, rectangles):
        '''Окрашиваем сделки в черный цвет
        '''
        for deal in self.deals:
            if deal >= ind and deal < i:
                lines[deal-ind].set_color("black")
                rectangles[deal-ind].set_color("black")
            else:
                self.deals.remove(deal)

        indexes = range(ind, i)

        plt.plot(indexes, self.lowest[ind:i], color='black')
        plt.plot(indexes, self.highest[ind:i], color='black')


    def _set_limits(self, candles_data, i, ind):
        ''' Устанавливаем лимиты для осей
        '''
        min_lim = min(self.data['<LOW>'].iloc[ind:i])
        max_lim = max(self.data['<HIGH>'].iloc[ind:i])

        self.ax.set_xlim([candles_data[0][0], candles_data[i-ind-1][0]])
        self.ax.set_ylim([min_lim-2, max_lim+2])

    def count_SMA(self):
        ''' Построение скользящей средней
        '''
        self.SMA = self.data['<CLOSE>'].rolling(self.N).mean()


    def count_EMA(self):
        ''' Построение экспоненциальной скользящей средней
        '''
        self.EMA = self.data['<CLOSE>'].ewm(span=self.N, adjust=False).mean()

    def show(self, width=0.3, alpha=0.8, *args, **kwargs):
        ''' Базовая функция для отображения функции на графике
        '''
        self.ax.xaxis.set_major_formatter(ticker.FuncFormatter(self._date_ticker))

        plt.ion()
        plt.show(block=False) # Block = False для динамической отрисовки
        for i in range(1, len(self.data['<CLOSE>'])):
            self.find = i

            if self.ax.has_been_closed: # Если окно было закрыто - выхордим из цикла
                break

            ind = i - self.N # Избавляемся от отрицательных случаев (i < 0)
            if ind < 0:
                ind = 0

            self.sind = ind

            candles_data = self.tuppled_data[ind:i] # Берем последние N свеч
            lines, rectangles = candlestick_ohlc(self.ax, candles_data, width=width,
                                                 colorup='g', colordown='r', alpha=alpha)

            self._color_deals(ind, i, lines, rectangles) # Окрашиваем сделки в черный цвет

            self._set_limits(candles_data, i, ind) # Вычисляем лимиты для осей

            # self._show_algorithm(*args, highest=self.highest, lowest=self.lowest, **kwargs) # Обратная зависимость

            # plt.plot(range(len(self.data))[self.sind:self.find-1], self.SMA.iloc[self.sind:self.find-1], color='blue')
            # plt.plot(range(len(self.data))[self.sind:self.find-1], self.EMA.iloc[self.sind:self.find-1], color='purple')

            self.fig.canvas.draw()

            yield # Возвращаем управление

            self.fig.canvas.flush_events()

            self.ax.lines = [] # Очищаем оси
            self.ax.patches = []


class TheoryQuickGrowthView(BaseViewCandles):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _show_algorithm(self, *args, highest=[], lowest=[], **kwargs):
        if len(lowest) > 0 and len(highest) > 0:
            sind = self.sind
            find = self.find

            if highest is not None:
                highest = highest[self.sind:self.find]

            if lowest is not None:
                lowest = lowest[self.sind:self.find]

            indexes = range(self.sind, self.find-1)
            plt.plot(indexes, highest, color='black')
            plt.plot(indexes, lowest, color='black')
