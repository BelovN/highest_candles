from datetime import *
from numpy import *
import requests
import os
import time
import shutil

############## Дата начала котировок #######################
startDate = date(2015, 1, 1)
# качает до сегодняшнего дня
############################################################

urls = []
# прямая ссылка на файл исторических данных в виде urls.append('http://... '), ненужные можно исключить с помощью #
# выбранный ТФ и параметры экспорта на странице финама значение имеют, интервал дат - нет
# urls.append('http://export.finam.ru/btsx.ltc/usd_190313_190313.txt?market=520&em=499047&code=btsx.ltc%2fusd&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=btsx.ltc%2fusd_190313_190313&e=.txt&cn=btsx.ltc%2fusd&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.si_130101_171231.txt?market=14&em=19899&code=spfb.si&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.si_130101_171231&e=.txt&cn=spfb.si&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.rts_130101_171231.txt?market=14&em=17455&code=spfb.rts&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.rts_130101_171231&e=.txt&cn=spfb.rts&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.br_130101_171231.txt?market=14&em=22460&code=spfb.br&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.br_130101_171231&e=.txt&cn=spfb.br&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.ed_130101_171231.txt?market=14&em=21989&code=spfb.ed&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.ed_130101_171231&e=.txt&cn=spfb.ed&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.eu_130101_171231.txt?market=14&em=22010&code=spfb.eu&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.eu_130101_171231&e=.txt&cn=spfb.eu&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.sbrf_130101_171231.txt?market=14&em=17456&code=spfb.sbrf&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.sbrf_130101_171231&e=.txt&cn=spfb.sbrf&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.sbpr_130101_171231.txt?market=14&em=81026&code=spfb.sbpr&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.sbpr_130101_171231&e=.txt&cn=spfb.sbpr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.gazr_130101_171231.txt?market=14&em=17451&code=spfb.gazr&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.gazr_130101_171231&e=.txt&cn=spfb.gazr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.mxi_130101_171231.txt?market=14&em=436202&code=spfb.mxi&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.mxi_130101_171231&e=.txt&cn=spfb.mxi&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.gold_130101_171231.txt?market=14&em=19898&code=spfb.gold&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.gold_130101_171231&e=.txt&cn=spfb.gold&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.vtbr_130101_171231.txt?market=14&em=19891&code=spfb.vtbr&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.vtbr_130101_171231&e=.txt&cn=spfb.vtbr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.mgnt_130101_171231.txt?market=14&em=390848&code=spfb.mgnt&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.mgnt_130101_171231&e=.txt&cn=spfb.mgnt&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.lkoh_130101_171231.txt?market=14&em=17453&code=spfb.lkoh&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.lkoh_130101_171231&e=.txt&cn=spfb.lkoh&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.rosn_130101_171231.txt?market=14&em=19894&code=spfb.rosn&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.rosn_130101_171231&e=.txt&cn=spfb.rosn&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.silv_130101_171231.txt?market=14&em=19902&code=spfb.silv&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.silv_130101_171231&e=.txt&cn=spfb.silv&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.gmkr_130101_171231.txt?market=14&em=17452&code=spfb.gmkr&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.gmkr_130101_171231&e=.txt&cn=spfb.gmkr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.aflt_130101_171231.txt?market=14&em=484309&code=spfb.aflt&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.aflt_130101_171231&e=.txt&cn=spfb.aflt&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.hydr_130101_171231.txt?market=14&em=81025&code=spfb.hydr&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.hydr_130101_171231&e=.txt&cn=spfb.hydr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.tatn_130101_171231.txt?market=14&em=81024&code=spfb.tatn&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.tatn_130101_171231&e=.txt&cn=spfb.tatn&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.alrs_130101_171231.txt?market=14&em=461013&code=spfb.alrs&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.alrs_130101_171231&e=.txt&cn=spfb.alrs&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.fees_130101_171231.txt?market=14&em=81020&code=spfb.fees&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.fees_130101_171231&e=.txt&cn=spfb.fees&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.gbpu_130101_171231.txt?market=14&em=81010&code=spfb.gbpu&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.gbpu_130101_171231&e=.txt&cn=spfb.gbpu&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.nlmk_130101_171231.txt?market=14&em=453418&code=spfb.nlmk&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.nlmk_130101_171231&e=.txt&cn=spfb.nlmk&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.ujpy_130101_171231.txt?market=14&em=175893&code=spfb.ujpy&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.ujpy_130101_171231&e=.txt&cn=spfb.ujpy&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.sngr_130101_171231.txt?market=14&em=17457&code=spfb.sngr&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.sngr_130101_171231&e=.txt&cn=spfb.sngr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.sngp_130101_171231.txt?market=14&em=81021&code=spfb.sngp&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.sngp_130101_171231&e=.txt&cn=spfb.sngp&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.rtkm_130101_171231.txt?market=14&em=17454&code=spfb.rtkm&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.rtkm_130101_171231&e=.txt&cn=spfb.rtkm&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/spfb.moex_130101_171231.txt?market=14&em=390846&code=spfb.moex&apply=0&df=1&mf=0&yf=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=spfb.moex_130101_171231&e=.txt&cn=spfb.moex&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
#
# urls.append('http://export.finam.ru/gazp_130101_171231.txt?market=1&em=16842&code=gazp&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=gazp_171231_171231&e=.txt&cn=gazp&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/gmkn_130101_171231.txt?market=1&em=795&code=gmkn&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=gmkn_171231_171231&e=.txt&cn=gmkn&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/lkoh_130101_171231.txt?market=1&em=8&code=lkoh&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=lkoh_171231_171231&e=.txt&cn=lkoh&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/rosn_130101_171231.txt?market=1&em=17273&code=rosn&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=rosn_171231_171231&e=.txt&cn=rosn&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/sngs_130101_171231.txt?market=1&em=4&code=sngs&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=sngs_171231_171231&e=.txt&cn=sngs&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/sngsp_130101_171231.txt?market=1&em=13&code=sngsp&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=sngsp_171231_171231&e=.txt&cn=sngsp&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/aflt_130101_171231.txt?market=1&em=29&code=aflt&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=aflt_171231_171231&e=.txt&cn=aflt&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/vtbr_130101_171231.txt?market=1&em=19043&code=vtbr&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=vtbr_171231_171231&e=.txt&cn=vtbr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/sberp_130101_171231.txt?market=1&em=23&code=sberp&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=sberp_171231_171231&e=.txt&cn=sberp&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/sber_130101_171231.txt?market=1&em=3&code=sber&apply=0&df=31&mf=11&yf=2017&from=31.12.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=2&f=sber_171231_171231&e=.txt&cn=sber&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/chmf_180501_180501.txt?market=1&em=16136&code=chmf&apply=0&df=1&mf=4&yf=2018&from=01.05.2018&dt=1&mt=4&yt=2018&to=01.05.2018&p=2&f=chmf_180501_180501&e=.txt&cn=chmf&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/nvtk_180501_180501.txt?market=1&em=17370&code=nvtk&apply=0&df=1&mf=4&yf=2018&from=01.05.2018&dt=1&mt=4&yt=2018&to=01.05.2018&p=2&f=nvtk_180501_180501&e=.txt&cn=nvtk&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/mtss_181129_181129.txt?market=1&em=15523&code=mtss&apply=0&df=29&mf=10&yf=2018&from=29.11.2018&dt=29&mt=10&yt=2018&to=29.11.2018&p=2&f=mtss_181129_181129&e=.txt&cn=mtss&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/mgnt_181129_181129.txt?market=1&em=17086&code=mgnt&apply=0&df=29&mf=10&yf=2018&from=29.11.2018&dt=29&mt=10&yt=2018&to=29.11.2018&p=2&f=mgnt_181129_181129&e=.txt&cn=mgnt&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/hydr_181129_181129.txt?market=1&em=20266&code=hydr&apply=0&df=29&mf=10&yf=2018&from=29.11.2018&dt=29&mt=10&yt=2018&to=29.11.2018&p=2&f=hydr_181129_181129&e=.txt&cn=hydr&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/chmf_181129_181129.txt?market=1&em=16136&code=chmf&apply=0&df=29&mf=10&yf=2018&from=29.11.2018&dt=29&mt=10&yt=2018&to=29.11.2018&p=2&f=chmf_181129_181129&e=.txt&cn=chmf&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/nlmk_181129_181129.txt?market=1&em=17046&code=nlmk&apply=0&df=29&mf=10&yf=2018&from=29.11.2018&dt=29&mt=10&yt=2018&to=29.11.2018&p=2&f=nlmk_181129_181129&e=.txt&cn=nlmk&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/tatn_181129_181129.txt?market=1&em=825&code=tatn&apply=0&df=29&mf=10&yf=2018&from=29.11.2018&dt=29&mt=10&yt=2018&to=29.11.2018&p=2&f=tatn_181129_181129&e=.txt&cn=tatn&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
#
# urls.append('http://export.finam.ru/yndx_190313_190313.txt?market=1&em=388383&code=yndx&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=yndx_190313_190313&e=.txt&cn=yndx&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/alrs_190313_190313.txt?market=1&em=81820&code=alrs&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=alrs_190313_190313&e=.txt&cn=alrs&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/irao_190313_190313.txt?market=1&em=20516&code=irao&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=irao_190313_190313&e=.txt&cn=irao&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/tatnp_190313_190313.txt?market=1&em=826&code=tatnp&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=tatnp_190313_190313&e=.txt&cn=tatnp&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/upro_190313_190313.txt?market=1&em=18584&code=upro&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=upro_190313_190313&e=.txt&cn=upro&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/moex_190313_190313.txt?market=1&em=152798&code=moex&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=moex_190313_190313&e=.txt&cn=moex&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/magn_190313_190313.txt?market=1&em=16782&code=magn&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=magn_190313_190313&e=.txt&cn=magn&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/rual_190313_190313.txt?market=1&em=414279&code=rual&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=rual_190313_190313&e=.txt&cn=rual&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/plzl_190313_190313.txt?market=1&em=17123&code=plzl&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=plzl_190313_190313&e=.txt&cn=plzl&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/afks_190313_190313.txt?market=1&em=19715&code=afks&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=afks_190313_190313&e=.txt&cn=afks&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/fees_190313_190313.txt?market=1&em=20509&code=fees&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=fees_190313_190313&e=.txt&cn=fees&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/poly_190313_190313.txt?market=1&em=175924&code=poly&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=poly_190313_190313&e=.txt&cn=poly&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/five_190313_190313.txt?market=1&em=491944&code=five&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=five_190313_190313&e=.txt&cn=five&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/rsti_190313_190313.txt?market=1&em=20971&code=rsti&apply=0&df=13&mf=2&yf=2019&from=13.03.2019&dt=13&mt=2&yt=2019&to=13.03.2019&p=2&f=rsti_190313_190313&e=.txt&cn=rsti&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
#
# urls.append('http://export.finam.ru/MINISANDP500_190601_190904.txt?market=7&em=13944&code=MINISANDP500&apply=0&df=1&mf=5&yf=2019&from=01.06.2019&dt=4&mt=8&yt=2019&to=04.09.2019&p=2&f=MINISANDP500_190601_190904&e=.txt&cn=MINISANDP500&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/DANDI.MINIFUT_190601_190904.txt?market=7&em=21718&code=DANDI.MINIFUT&apply=0&df=1&mf=5&yf=2019&from=01.06.2019&dt=4&mt=8&yt=2019&to=04.09.2019&p=2&f=DANDI.MINIFUT_190601_190904&e=.txt&cn=DANDI.MINIFUT&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/SANDP-FUT_190601_190904.txt?market=7&em=108&code=SANDP-FUT&apply=0&df=1&mf=5&yf=2019&from=01.06.2019&dt=4&mt=8&yt=2019&to=04.09.2019&p=2&f=SANDP-FUT_190601_190904&e=.txt&cn=SANDP-FUT&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
# urls.append('http://export.finam.ru/NQ-100-FUT_190601_190904.txt?market=7&em=21719&code=NQ-100-FUT&apply=0&df=1&mf=5&yf=2019&from=01.06.2019&dt=4&mt=8&yt=2019&to=04.09.2019&p=2&f=NQ-100-FUT_190601_190904&e=.txt&cn=NQ-100-FUT&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')
urls.append('http://export.finam.ru/DSX_190601_190904.txt?market=7&em=12997&code=DSX&apply=0&df=1&mf=5&yf=2019&from=01.06.2019&dt=4&mt=8&yt=2019&to=04.09.2019&p=2&f=DSX_190601_190904&e=.txt&cn=DSX&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1')

now = datetime.now()
nameFolder = str(now.day).zfill(2)+'_'+str(now.month).zfill(2)+'_'+str(now.year).zfill(2)

if os.path.exists(nameFolder):
    shutil.rmtree(nameFolder)

os.mkdir(nameFolder)
os.chdir(nameFolder)

print('start date ' + str(startDate))
now = datetime.now() - timedelta(days=1)
endDate = date(now.year, now.month, now.day)
print('end date ' + str(endDate))

cmps = 30 # сжатие на кол-во дней

currentDate = startDate
dates = endDate - startDate
countDates = dates.days//cmps
nameFiles = [None] * (countDates+1)
print('total ' + str(countDates+1) + ' days')

for url in urls:
    currentDate = startDate
    # nextDate = currentDate + timedelta(days=cmps)
    for i in range(countDates+1):
        nextDate = currentDate + timedelta(days=cmps-1)
        if nextDate > endDate :
            nextDate = endDate
        # forming download link
        strings = str.split(url, '&')
        strings[4] = 'df=' + str(currentDate.day)
        strings[5] = 'mf=' + str(currentDate.month - 1)
        strings[6] = 'yf=' + str(currentDate.year)
        strings[7] = 'from=' + str(currentDate.day).zfill(2) + str('.') + str(currentDate.month).zfill(2) + str('.') + str(currentDate.year)
        strings[8] = 'dt=' + str(nextDate.day)
        strings[9] = 'mt=' + str(nextDate.month - 1)
        strings[10] = 'yt=' + str(nextDate.year)
        strings[11] = 'to=' + str(nextDate.day).zfill(2) + str('.') + str(nextDate.month).zfill(2) + str('.') + str(nextDate.year)

        newurl = "&".join(strings)
        # downloading files
        print("downloading file " + str(i+1) + " of " + str(countDates+1) + " files")
        f = requests.get(newurl, headers={'User-Agent': 'Mozilla/59.0'})
        nameFiles[i] = str(i + 1) + '_' + str(currentDate.day).zfill(2) + str('.') + str(currentDate.month).zfill(2) + str('.') + str(currentDate.year) + ".txt"
        with open(nameFiles[i], "wb") as code:
            code.write(f.content)
        time.sleep(1)
        currentDate += timedelta(days=cmps)

    print("All files was downloaded")

    time.sleep(5)
    # merging files
    print("Start merge files...")
    i = 0
    firstStr = '<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>\n'
    # nmefile = url.split('_')[0].split('ru/')[1] + '_' + str(endDate.day).zfill(2) + str(endDate.month).zfill(2) + str(endDate.year).zfill(2)
    nmefile = url.split('_')[0].split('ru/')[1].replace('/', '')
    with open(nmefile + '.txt', 'w') as outfile:
        outfile.write(firstStr)
        for fname in nameFiles:
            i += 1
            print("Merging file " + str(i) + " of " + str(countDates+1) + " files")
            with open(fname) as infile:
                for line in infile:
                    if line != firstStr:
                        outfile.write(line)
            # os.remove(fname)
            print("Removing file " + str(i) + " of " + str(countDates+1) + " files")

    print("All files was merged")

    time.sleep(5)
    for fname in nameFiles:
        os.remove(fname)
    time.sleep(5)

print("All operation was finished")
