# import requests
# import os
# import time
# import shutil
# from datetime import *
# from numpy import *
#
#
# ############## Дата начала котировок #######################
# startDate = date(2019, 1, 1)
# # качает до сегодняшнего дня
# ############################################################
#
# urls = []
# urls.append('http://export.finam.ru/DSX_190601_190904.txt?market=7&em=12997&code=DSX&apply=0&df=1&mf=5&yf=2019&from=01.06.2019&dt=4&mt=8&yt=2019&to=04.09.2019&p=2&f=DSX_190601_190904&e=.txt&cn=DSX&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
#
# now = datetime.now()
# folder_name = str(now.day).zfill(2)+'_'+str(now.month).zfill(2)+'_'+str(now.year).zfill(2)
#
# if os.path.exists(folder_name):
#     shutil.rmtree(folder_name)
#
# os.mkdir(folder_name)
# os.chdir(folder_name)
#
# print('start date ' + str(startDate))
# now = datetime.now() - timedelta(days=1)
# endDate = date(now.year, now.month, now.day)
# print('end date ' + str(endDate))
#
# cmps = 30 # сжатие на кол-во дней
#
# currentDate = startDate
# dates = endDate - startDate
# countDates = dates.days//cmps
# nameFiles = [None] * (countDates+1)
# print('total ' + str(countDates+1) + ' days')
#
# for url in urls:
#     currentDate = startDate
#     # nextDate = currentDate + timedelta(days=cmps)
#     for i in range(countDates+1):
#         nextDate = currentDate + timedelta(days=cmps-1)
#         if nextDate > endDate :
#             nextDate = endDate
#         # forming download link
#         strings = str.split(url, '&')
#         strings[4] = 'df=' + str(currentDate.day)
#         strings[5] = 'mf=' + str(currentDate.month - 1)
#         strings[6] = 'yf=' + str(currentDate.year)
#         strings[7] = 'from=' + str(currentDate.day).zfill(2) + str('.') + str(currentDate.month).zfill(2) + str('.') + str(currentDate.year)
#         strings[8] = 'dt=' + str(nextDate.day)
#         strings[9] = 'mt=' + str(nextDate.month - 1)
#         strings[10] = 'yt=' + str(nextDate.year)
#         strings[11] = 'to=' + str(nextDate.day).zfill(2) + str('.') + str(nextDate.month).zfill(2) + str('.') + str(nextDate.year)
#
#         newurl = "&".join(strings)
#         # downloading files
#         print("downloading file " + str(i+1) + " of " + str(countDates+1) + " files")
#         f = requests.get(newurl, headers={'User-Agent': 'Mozilla/59.0'})
#         nameFiles[i] = str(i + 1) + '_' + str(currentDate.day).zfill(2) + str('.') + str(currentDate.month).zfill(2) + str('.') + str(currentDate.year) + ".txt"
#         with open(nameFiles[i], "wb") as code:
#             code.write(f.content)
#
#         currentDate += timedelta(days=cmps)
#
#     print("All files was downloaded")
#
#     time.sleep(5)
#     # merging files
#     print("Start merge files...")
#     i = 0
#     firstStr = '<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>\n'
#     # nmefile = url.split('_')[0].split('ru/')[1] + '_' + str(endDate.day).zfill(2) + str(endDate.month).zfill(2) + str(endDate.year).zfill(2)
#     nmefile = url.split('_')[0].split('ru/')[1].replace('/', '')
#     with open(nmefile + '.txt', 'w') as outfile:
#         outfile.write(firstStr)
#         for fname in nameFiles:
#             i += 1
#             print("Merging file " + str(i) + " of " + str(countDates+1) + " files")
#             with open(fname) as infile:
#                 for line in infile:
#                     if line != firstStr:
#                         outfile.write(line)
#             # os.remove(fname)
#             print("Removing file " + str(i) + " of " + str(countDates+1) + " files")
#
#     print("All files was merged")
#
#     time.sleep(5)
#     for fname in nameFiles:
#         os.remove(fname)
#     time.sleep(5)
#
# print("All operation was finished")

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from settings import *

mpl.use('QT5Agg')

data = pd.read_csv(os.path.join(OUTPUT_DIR, 'statistic.csv'), sep=';', decimal=',')
# fig, (ax1, ax2) = plt.subplots(2)
# ax1.plot(data['avr_potencial'], range(len(data['avr_potencial'])))
# ax2.plot(data['avr_max_min'], range(len(data['avr_max_min'])))
#
# plt.show()

#
import numpy
from scipy.stats.stats import pearsonr
# list1 = []
# list2 = []
#
# for item in data['avr_potencial']:
#     list1.append(float(item.replace(',', '.')))
#
# for item in data['avr_max_min']:
#     list2.append(float(item.replace(',', '.')))
#
# c = pearsonr(data['delta_potencial'], data['delta_max_min'])

print(numpy.mean(data['delta_potencial']))
