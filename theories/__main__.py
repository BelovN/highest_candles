import keyboard
import time
from view import BaseViewCandles
from theory import TheoryQuickGrowth
from services import get_standartized_data
from settings import *


def pause_listener():
    while True:
        if keyboard.is_pressed('='):
            input()
            # keyboard.read_key()
        yield

def main():
    data = get_standartized_data(path=GAZP_PATH_MIN_2020)
    deals = [] # Общий пулл сделок
    tasks = [] # Пулл задач

    candles_view = BaseViewCandles(data)
    tasks.append(candles_view.show(deals=deals))
    theory = TheoryQuickGrowth(data, Nmin=30, Nmax=40)
    tasks.append(theory.check(deals=deals))

    tasks.append(pause_listener())

    while True: # Корутина
        try: # Асинхронное выполнение тасков
            task = tasks.pop(0)
            next(task)
            tasks.append(task)
        except StopIteration:
            break

if __name__ == '__main__':
    main()
