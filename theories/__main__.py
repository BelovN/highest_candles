from view import TheoryQuickGrowthView
from theory import TheoryQuickGrowth
from services import get_standartized_data
from settings import *


def main():
    data = get_standartized_data(path=RTS_3YEARS_HOUR, sep=';')
    tasks = [] # Пулл задач

    deals = [] # Общий пулл сделок
    highest = []
    lowest = []

    candles_view = TheoryQuickGrowthView(data, deals=deals, highest=highest, lowest=lowest)
    theory = TheoryQuickGrowth(data, Nmin=20, Nmax=20, deals=deals, highest=highest, lowest=lowest)

    tasks.append(theory.check())
    tasks.append(candles_view.show())

    while True: # Корутина
        try: # Асинхронное выполнение тасков
            task = tasks.pop(0)
            next(task)
            tasks.append(task)

        except StopIteration:
            break

    input()

if __name__ == '__main__':
    main()
