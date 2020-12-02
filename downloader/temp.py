import pandas as pd
import time
import requests

df = pd.read_csv("finamru.csv")
# print(df)

# url = 'http://export.finam.ru/{code}/{filename}.{extension}?market={market}&em={em}&code={code}&apply=0&df={df}&mf={mf}&yf={yf}&from={from_}&dt={dt}&mt={mt}&yt={yt}&to={to}&p=2&f={filename}.{extension}&cn={code}&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
url = 'http://export.finam.ru/{code}/{filename}.{extension}?market={market}&em={em}&code={code}&apply=0&df=15&mf=11&yf=2019&from=15.12.2019&dt=31&mt=11&yt=2020&to=31.12.2020&p=7&f={filename}.{extension}&cn={code}&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
URL2 = 'http://export.finam.ru/&df=15&mf=11&yf=2019&from=15.12.2019&dt={dt}&mt={mt}&yt={yt}&to={from_}&p=7&f={filename}&e=.{extension}&cn={code}&dtf=2&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'

def prepare_url():
    code = 'MAGN'
    filename = 'MAGN-'
    extension = 'csv'
    market = 1
    em = 16782
    df = 15
    mf = 11
    yf = 2019
    from_ = '15.12.2019'

    dt = 31
    mt = 12
    yt = 2020

    to = '31.12.2020'
    prepared_url = url.format(code=code, filename=filename, extension=extension, market=market, em=em,
                              df=df, mf=mf, yf=yf, from_=from_, dt=dt, mt=mt, yt=yt, to=to)

    f = requests.get(prepared_url, headers={'User-Agent': 'Mozilla/59.0'})

    with open(filename+'.'+extension, "wb") as file:
        file.write(f.content)
    time.sleep(1)
    print(prepared_url)


prepare_url()
