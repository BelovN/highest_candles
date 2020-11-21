import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from settings import OUTPUT_FILE_DIR
import numpy as np

mpl.use('Qt5Agg')

INPUT_FILE_DIR = OUTPUT_FILE_DIR.replace('output.txt', 'output_h.txt')
#
# with open(OUTPUT_FILE_DIR, 'r', encoding='utf-8') as output:
#     with open(INPUT_FILE_DIR, 'w', encoding='utf-8') as input:
#         for line in output:
#             while line.find('  ') != -1:
#                 line = line.replace('  ', ' ')
#             input.write(line)


fig = plt.figure()
ax = fig.gca(projection='3d')

data = pd.read_csv(INPUT_FILE_DIR, sep=' ', encoding='utf-8')
X = np.asarray([np.asarray(list(range(60, 5, -5))) for i in range(10)])
Y = np.asarray([np.asarray([i]*11) for i in range(10, 60, 5)])
# Y = np.asarray([np.asarray(list(range(10, 65, 5))) for i in range(10)])

Z = []
t = []
count = 0
for i, value in enumerate(data['total']):
    if count % 11 == 0 and i != 0:
        Z.append(np.asarray(t))
        t = []
        count = 0

    t.append(value)
    count = count + 1

Z = np.asarray(Z)


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax.set_xlabel('MIN')
ax.set_ylabel('MAX')
ax.set_zlabel('TOTAL')


# fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


# data = pd.read_csv(OUTPUT_FILE_DIR, sep=' ', encoding='utf-8')
# data = data.set_index('N')
# data['count_lesion'].plot(title='Количество убыточных сделок')
# plt.show()
# data['avr_lesion'].plot(title='Средний убыток')
# plt.show()
# data['count_profit'].plot(title='Количество прибыльных сделок')
# plt.show()
# data['avr_profit'].plot(title='Средняя прибыль')
# plt.show()
# data['count_all'].plot(title='Общее количество сделок')
# plt.show()
# data['total'].plot(title='Итог')
# plt.show()
# data['avr_all'].plot(title='Среднее от всех сделок')
# plt.show()
# data['avr_potencial'].plot(title='Средний потенциал')
# plt.show()
