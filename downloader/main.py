import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
# r = requests.get('https://www.finam.ru/profile/moex-akcii/gazprom/export/')


# url = 'http://export.finam.ru/btsx.ltc/usd_190313_190313.txt?market=520&em=499047&code=btsx.ltc%2fusd&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=btsx.ltc%2fusd_190313_190313&e=.txt&cn=btsx.ltc%2fusd&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
with open('page.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file)
    dropdown_list = soup.find_all('a')
    data = {
        'text': [],
        'value': []
    }
    for link in dropdown_list:
        data['text'].append(link.text)
        data['value'].append(int(link['value']))

    frame= pd.DataFrame.from_dict(data)
    print(frame)
    # print(dropdown_list['value'])
    # print(dropdown_list.get_text())
#
# with open('codes.html', 'r', encoding='utf-8') as file:
#     data = json.load(file)
