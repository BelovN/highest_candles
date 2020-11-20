import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
GAZP_PATH = os.path.join(DATA_DIR, 'GAZP_200101_201112.csv')

OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_FILE_DIR = os.path.join(OUTPUT_DIR, 'output.txt')
