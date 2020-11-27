import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

GAZP_PATH_MIN_2019 = os.path.join(DATA_DIR, 'GAZP_190101_191231 (MIN).csv')
GAZP_PATH_MIN_2020 = os.path.join(DATA_DIR, 'GAZP_200101_201112 (MIN).csv')

GAZP_PATH_5MIN_2019 = os.path.join(DATA_DIR, 'GAZP_190101_191231 (5 MIN).csv')

GAZP_PATH_HOUR_2018 = os.path.join(DATA_DIR, 'GAZP_180101_181231 (HOUR).csv')
GAZP_PATH_HOUR_2019 = os.path.join(DATA_DIR, 'GAZP_190101_191231 (HOUR).csv')
GAZP_PATH_HOUR_2020 = os.path.join(DATA_DIR, 'GAZP_200101_201123 (HOUR).csv')

OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_FILE_DIR = os.path.join(OUTPUT_DIR, 'output.txt')
