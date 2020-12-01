import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

GAZP_PATH_MIN_2019 = os.path.join(DATA_DIR, 'GAZP_190101_191231 (MIN).csv')
GAZP_PATH_MIN_2020 = os.path.join(DATA_DIR, 'GAZP_200101_201112 (MIN).csv')

GAZP_PATH_5MIN_2019 = os.path.join(DATA_DIR, 'GAZP_190101_191231 (5 MIN).csv')

GAZP_PATH_HOUR_2018 = os.path.join(DATA_DIR, 'GAZP_180101_181231 (HOUR).csv')
GAZP_PATH_HOUR_2019 = os.path.join(DATA_DIR, 'GAZP_190101_191231 (HOUR).csv')
GAZP_PATH_HOUR_2020 = os.path.join(DATA_DIR, 'GAZP_200101_201123 (HOUR).csv')


RTS_PATH_HOUR_2018 = os.path.join(DATA_DIR, 'RTS_2018_HOUR.csv')
RTS_PATH_HOUR_2019 = os.path.join(DATA_DIR, 'RTS_2019_HOUR.csv')
RTS_PATH_HOUR_2020 = os.path.join(DATA_DIR, 'RTS_2020_HOUR.csv')

RTS_PATH_15MIN_2018 = os.path.join(DATA_DIR, 'RTS_2018_15MIN.csv')
RTS_PATH_15MIN_2019 = os.path.join(DATA_DIR, 'RTS_2019_15MIN.csv')
RTS_PATH_15MIN_2020 = os.path.join(DATA_DIR, 'RTS_2020_15MIN.csv')

RTS_3YEARS_HOUR = os.path.join(DATA_DIR, 'RTS_3YEARS_HOUR.csv')
RTS_3YEARS_15MIN = os.path.join(DATA_DIR, 'RTS_3YEARS_15MIN.csv')


SI_PATH_HOUR_2018 = os.path.join(DATA_DIR, 'SI_2018_HOUR.csv')
SI_PATH_HOUR_2019 = os.path.join(DATA_DIR, 'SI_2019_HOUR.csv')
SI_PATH_HOUR_2020 = os.path.join(DATA_DIR, 'SI_2020_HOUR.csv')

SI_PATH_15MIN_2018 = os.path.join(DATA_DIR, 'SI_2018_15MIN.csv')
SI_PATH_15MIN_2019 = os.path.join(DATA_DIR, 'SI_2019_15MIN.csv')
SI_PATH_15MIN_2020 = os.path.join(DATA_DIR, 'SI_2020_15MIN.csv')

SI_3YEARS_HOUR = os.path.join(DATA_DIR, 'SI_3YEARS_HOUR.csv')
SI_3YEARS_15MIN = os.path.join(DATA_DIR, 'SI_3YEARS_15MIN.csv')


OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_FILE_DIR = os.path.join(OUTPUT_DIR, 'output.txt')
