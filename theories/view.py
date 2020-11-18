import time
import keyboard
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from matplotlib import ticker
from mplfinance.original_flavor import candlestick_ohlc



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

    def __init__(self, data, N=10, **kwargs):
        ''' Данные должны быть в формате списка кортежей из 5 состовляющих
        '''
        self.data = data
        self.N = N
        self.set_up(**kwargs) # Настройки


    def _show_algorithm(self, *args, **kwargs):
        ''' Функция для отображения алгоритмов
        '''
        return


    def show(self, width=0.0007, alpha=0.8, *args, **kwargs):
        ''' Базовая функция для отображения функции на графике
        '''
        plt.ion()
        plt.show(block=False)
        for i in range(len(self.data)):

            if self.ax.has_been_closed:
                break

            candles_data = self.data[i:i+self.N*3]
            candles = candlestick_ohlc(self.ax, candles_data, width=width,
                                       colorup='g', colordown='r', alpha=alpha)

            x_lim = self.ax.get_xlim()
            self.ax.set_xlim([candles_data[0][0], candles_data[self.N-1][0]])

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

            self._show_algorithm(args, kwargs)

            self.ax.lines = []
            self.ax.patches = []
