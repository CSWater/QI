import pandas as pd
import numpy as np
def readFile(filename):
    nums = np.array(pd.read_csv(filename, sep='\t'))
    # 读取从英为财情读到的数据
    # date, close_price, open_price, high_price, low_price
    # trade_volume, rise_rate
    return nums[:, 0], nums[:, 1], nums[0, 2], nums[0, 3], \
      nums[:, 4], nums[:, 5], nums[:, 6]

def formatFile(filename):
  #TODO
  return