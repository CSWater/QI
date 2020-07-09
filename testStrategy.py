import tushare as ts
import pandas as pd
import numpy as np
import plot
import strategy as st
import datatypes as dt

etf_513030 = dt.ETF("./database/513030.csv")
#etf_513030.dump()
print(etf_513030.getHistoryLength())
grid_strategy = st.GridStrategy(1.2, 0.05, 0.05)
grid_strategy.executeStrategy(etf_513030)