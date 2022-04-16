import csv
import pandas as pd
import numpy as np
import os

# transform chinese date to number-form date
def convertToStandardDate(date_string):
  s_year = date_string.split('年')[0]
  s_month = date_string.split('年')[1].split('月')[0]
  s_day = date_string.split('年')[1].split('月')[1].split('日')[0]
  if len(s_month) == 1: # add padding 0
    s_month = '0'+ s_month
  if len(s_day) == 1: #add padding 0
    s_day = '0' + s_day
  s_date = s_year + s_month + s_day
  return s_date


def readFile(filename):
    nums = np.array(pd.read_csv(filename))
    # 读取从英为财情读到的数据
    # date, close_price, open_price, high_price, low_price
    # trade_volume, rise_rate
    return nums[:, 0], nums[:, 1], nums[0, 2], nums[0, 3], \
      nums[:, 4], nums[:, 5], nums[:, 6]



#format the download raw file to standard file
def convertToStandardFile(filename):
  df = pd.read_csv(filename)
  #df.columns = ['date', 'close', 'open', 'high', 'low', 'volumn', "rise rate"]
  df.rename(columns={'日期':'date','收盘':'close','开盘':'open','高':"high",'低':"low",'交易量':"volumn",'涨跌幅':'rise_rate'}, inplace=True)
  df.date = df.date.apply(convertToStandardDate)
  #print(df)
  df.sort_index(ascending=False, inplace=True)
  df.to_csv(filename, index=False)

#record is a list [date, close, open, high, low, volumn, rise_rate]
def appendRecord(filename, record):
  if not os.path.isfile(filename):
    print(filename, "not exist!")
    return
  else:
    df = pd.DataFrame(data=record)
    df_T = df.T
    print(df_T)
    df_T.to_csv(filename, mode='a', header=False, index=False)


