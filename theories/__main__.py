import keyboard
import time
from view import TheoryQuickGrowthView
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
    data = get_standartized_data(path=GAZP_PATH_HOUR_2020)
    deals = [] # Общий пулл сделок
    tasks = [] # Пулл задач
    highest = []
    lowest = []

    candles_view = TheoryQuickGrowthView(data)
    tasks.append(candles_view.show(deals=deals, highest=highest, lowest=lowest))
    theory = TheoryQuickGrowth(data, Nmin=10, Nmax=10)
    tasks.append(theory.check(deals=deals, highest=highest, lowest=lowest))

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
