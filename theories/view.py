import time
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
        fig, ax = plt.subplots()

        self.fig = fig
        self.ax = ax

        self._setup_axis()


    def __on_close(self, event):
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


    def show(self, width=0.0005, alpha=0.8):
        plt.ion()
        plt.show(block=False)
        for i in range(1000):

            if self.ax.has_been_closed:
                break

            candles = candlestick_ohlc(self.ax, self.data[i+self.N:i+self.N*2], width=width,
                                       colorup='g', colordown='r', alpha=alpha)
            # self.ax.xaxis.set_major_formatter(dates.DateFormatter('%d.%m.%Y %H:%M'))
            # self.ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
            #
            # plt.grid()
            # plt.xticks(rotation=30)
            # plt.xlabel('Дата')
            # plt.ylabel('Цена')
            # plt.autoscale(enable=False, axis='both')

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

            self.ax.clear()



from services import get_tuppled_data

data = get_tuppled_data()
view = BaseViewCandles(data, N=50)
view.show()



#
# x = np.linspace(0, 6*np.pi, 100)
# y = np.sin(x)
#
# x = [1,2,3,4,5,6]
# y = x
#
#
# # You probably won't need this if you're embedding things in a tkinter plot...
# plt.ion()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma
#
# for phase in range(1000):
#     y = [i+1 for i in y]
#     line1.set_ydata(y)
#     time.sleep(0.4)
#     fig.canvas.draw()
#     fig.canvas.flush_events()
