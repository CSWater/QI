# coding: utf-8
import re,time,csv,datetime
from urllib.request import urlopen
from urllib.request import Request
import matplotlib as mpl
import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
import mplfinance as mpf
import matplotlib.dates as mpd
import pandas as pd
import os
import sys

# get the data range include year & season
t = time.localtime()
year = range(1978, t[0]+1, 1)
season = range(1, 5, 1)

def pullData(url, f_csv):
  data = pd.read_html(url, attrs={'class': 'table_bg001 border_box limit_sale'}, flavor=['lxml', 'bs4'])
  for ta in data:
    if ta.empty:
      continue;
    else:
      ta.sort_values("日期",inplace=True)
      ta.to_csv(f_csv, mode='a', header=None, index=False)

# get the data for code input
def get_stock_price_history(code, f_csv):
  url1 = "http://quotes.money.163.com/trade/lsjysj_"
  url2 = ".html?year="
  url3 = "&season="
  urllist = []
  for k in year:
    for v in season:
      urllist.append(url1+str(code)+url2+str(k)+url3+str(v))  
  for url in urllist:
    pullData(url, f_csv)

target_stocks = ['600036', '000651']
for code in target_stocks:
  csv_datafile=sys.path[0]+'\database\\'+code+'.csv'
  print(csv_datafile)
  #create table header
  df = pd.DataFrame(columns=['日期', '开盘价', '最高价', '最低价', '收盘价', '涨跌额', '涨跌幅(%)',	'成交量(手)',	'成交金额(万元)', '振幅(%)', '换手率(%)'])
  df.to_csv(csv_datafile, mode='w', index=False, encoding='utf_8_sig')
  get_stock_price_history(code, csv_datafile)


