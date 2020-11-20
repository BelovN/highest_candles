import matplotlib.pyplot as plt
import pandas as pd
from settings import OUTPUT_FILE_DIR


data = pd.read_csv(OUTPUT_FILE_DIR, sep=' ', encoding='utf-8')
data = data.set_index('N')
data['count_lesion'].plot(title='Количество убыточных сделок')
plt.show()
data['avr_lesion'].plot(title='Средний убыток')
plt.show()
data['count_profit'].plot(title='Количество прибыльных сделок')
plt.show()
data['avr_profit'].plot(title='Средняя прибыль')
plt.show()
data['count_all'].plot(title='Общее количество сделок')
plt.show()
data['total'].plot(title='Итог')
plt.show()
data['avr_all'].plot(title='Среднее от всех сделок')
plt.show()
data['avr_potencial'].plot(title='Средний потенциал')
plt.show()

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()
