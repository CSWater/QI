import tushare as ts
import pandas as pd
import numpy as np
import plot
import strategy
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


interval_end = len(hisClose)
interval_start = interval_end - 1219
buy_date, buy_point, sell_date, sell_point = strategy.searchSeg(interval_start, interval_end, hisClose)

print(len(buy_date), len(buy_point))
print(len(sell_date), len(sell_point))
hisCloseShow = hisClose[interval_start: interval_end]
plot.plotTransaction(hisCloseShow, interval_start, interval_end, buy_date, buy_point, sell_date, sell_point)