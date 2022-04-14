import pandas as pd
import numpy as np
import FileIO as fio
import datatypes as dt

#网格交易策略：使用高点的90%,85%,75%。。。。来买入，当达到任何买入价格的 1.05倍以上则卖出
class GridStrategy1:
  #strategy constant for each instance
  __danger_thredhold = -1
  __const_base = -1
  __step = -1
  __per_share = -1
  #strategy init
  def __init__(self, per_share, danger_threadhold, const_base, step):
    self.__danger_thredhold = danger_threadhold
    self.__const_base = const_base
    self.__step = step
    self.__per_share = per_share

  def executeStrategy(self, etf, start_date = 0, end_date = 1300):
      result = dt.StrategyResult()
      his_close = etf.getClosePrice()
      #print(his_close)
      #init high point
      high_price = float(his_close[0])
      drop_base = self.__const_base
      self._step = 0.05
      #if end_date > etf.getHistoryLength():
      end_date = etf.getHistoryLength()
      for date_id in range(start_date, end_date, 1):
          t_type = 'N'
          t_shares = -1
          t_price = -1
          #sell
          if len(result.getInProgressTransaction()) > 0 and float(his_close[date_id]) > result.getInProgressTransaction()[-1][0] * (1 + self.__step) :
              buy_record = result.getInProgressTransaction().pop()
              t_type = 'S'
              t_price = buy_record[0] * (1 + self.__step)
              t_shares = buy_record[1]
              print("sell,", t_shares, ",", t_price)
              drop_base = self.__const_base
              result.addTransaction(t_type, date_id, t_price, t_shares, t_price * 0.05)
              high_price = t_price
          #buy
          else:
              drop_rate = (high_price - float(his_close[date_id])) / high_price
              if drop_rate >= drop_base:
                  t_type = 'B'
                  t_price = high_price * (1 - drop_rate)
                  t_shares = int(self.__per_share / t_price / 100) * 100
                  result.addTransaction(t_type, date_id, t_price, t_shares, 0)
                  result.getInProgressTransaction().sort(reverse=1)
                  print("buy,", t_shares, ",", t_price)     
                  drop_base += self._step
          #update high price
          if drop_rate <= self.__const_base + 0.001 and float(his_close[date_id - 1]) > float(his_close[date_id]):
              if float(his_close[date_id - 1]) > high_price:
                  high_price = float(his_close[date_id - 1])
              if high_price > self.__danger_thredhold:
                  high_price = self.__danger_thredhold
          #update profit rate
          result.updateProfit(t_type, t_price, his_close[date_id], t_shares)
      return result


#interval_end = len(hisClose)
#interval_start = interval_end - 1219
#sell_point, buy_point, sell_date, buy_date = searchSeg(interval_start, interval_end, hisClose)

#hisCloseShow = hisClose[interval_start: interval_end]
# for i in range(0, len(buy_date)):
#     print("buy ", buy_date[i], buy_point[i])
# for i in range(0, len(sell_date)):
#     print("sell ", sell_date[i], sell_point[i])
#def plotTransaction():
#   x_axis = range(interval_start, interval_end)
#   plt.plot(x_axis, hisCloseShow)

#   plt.scatter(buy_date, buy_point,c='green',marker='v')
#   plt.scatter(sell_date, sell_point, c='red', marker='*')
#   plt.show()
#splotTransaction()

