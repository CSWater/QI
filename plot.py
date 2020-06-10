import matplotlib.pyplot as plt

def plotTransaction(hisCloseShow, interval_start, interval_end, buy_date, buy_point, sell_date, sell_point):
   x_axis = range(interval_start, interval_end)
   plt.plot(x_axis, hisCloseShow)

   plt.scatter(buy_date, buy_point,c='green',marker='v')
   plt.scatter(sell_date, sell_point, c='red', marker='*')
   plt.show()