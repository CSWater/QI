import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# pro = ts.pro_api('3d8cedf99d2132948985ba68d27926f5c50ccadbbc4f769499aefcc5')
# df = pro.index_global(ts_code='HSI', start_date='20140201', end_date='20160201')
# df.to_csv("HSItest12-16.csv")
# exit()

def readfile(filename):
    nums = np.array(pd.read_csv(filename))
    # 读取从tushare的index_global接口读到的数据
    # date = nums[:,0]
    # closeIndex = nums[:,3]
    # high = nums[0:4]
    # low = nums[0:5]
    # print(nums)
    # exit()
    # 读取从英为财情读到的数据
    date = nums[:,0]
    closeIndex = nums[:,2]
    high = nums[:,4]
    low = nums[:,5]
    return date, closeIndex, high, low
date, hisClose, hisHigh, hisLow= readfile("./database/HSIreal.csv")
hisClose = list(reversed(hisClose))
hisHigh = list(reversed(hisHigh))
hisLow = list(reversed(hisLow))
# print(hisClose)
# exit()
#  策略1：使用高点的90%,85%,75%。。。。来买入，当达到任何买入价格的 1.05倍以上则卖出



def searchSeg(intervalStart, intervalEnd, hisClose):
    #init high point
    high_price = float(hisClose[interval_start])
    danger_thredhold = 28000
    const_base = 0.05
    drop_base = const_base
    drop_step = 0.05
    transaction = []
    sum = 0.0
    maxlen = 0
    sell_point = []
    sell_date = []
    buy_point = []
    buy_date = []
    date_step = 1
    for date_id in range(interval_start, interval_end, date_step):
        #sell
        if len(transaction) > 0 and float(hisClose[date_id]) > transaction[-1] * (1 + drop_step) :
            sell_price = transaction.pop() * 1.05
            sum += drop_step
            drop_base = const_base
            sell_point.append(sell_price)
            sell_date.append(date_id)
            high_price = sell_price
            print(sell_price)
            #new high point pre > now
            #buy
        else:
            drop_rate = (high_price - float(hisClose[date_id])) / high_price
            if drop_rate >= drop_base:
                buy_price = high_price * (1 - drop_rate)
                transaction.append(buy_price)
                transaction.sort(reverse=1)
                print(transaction)
                drop_base += drop_step
                buy_point.append(buy_price)
                buy_date.append(date_id)
        #update high price
        if drop_rate <= const_base + 0.001 and float(hisClose[date_id - date_step]) > float(hisClose[date_id]):
            if float(hisClose[date_id - date_step]) > high_price:
                high_price = float(hisClose[date_id - date_step])
            if high_price > danger_thredhold:
                high_price = danger_thredhold
        maxlen = max(maxlen, len(transaction))
    print(sum/drop_step)
    print(maxlen)
    print(len(transaction))
    return sell_point, buy_point, sell_date, buy_date


interval_end = len(hisClose)
interval_start = interval_end - 1219
sell_point, buy_point, sell_date, buy_date = searchSeg(interval_start, interval_end, hisClose)

hisCloseShow = hisClose[interval_start: interval_end]
# for i in range(0, len(buy_date)):
#     print("buy ", buy_date[i], buy_point[i])
# for i in range(0, len(sell_date)):
#     print("sell ", sell_date[i], sell_point[i])
def plotTransaction():
   x_axis = range(interval_start, interval_end)
   plt.plot(x_axis, hisCloseShow)

   plt.scatter(buy_date, buy_point,c='green',marker='v')
   plt.scatter(sell_date, sell_point, c='red', marker='*')
   plt.show()
plotTransaction()


