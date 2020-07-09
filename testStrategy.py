import pandas as pd
import numpy as np
import plot
import strategy as st
import datatypes as dt
import FileIO as fio

etf_513030 = dt.ETF("./database/513030.csv")
grid_strategy = st.GridStrategy(2000, 1.2, 0.05, 0.05)
res_513030 = grid_strategy.executeStrategy(etf_513030)
(cost, shares, cur_price, investment) = res_513030.getProfit()
max_investment = res_513030.getMaxInvestment()
profit = shares * (cur_price - cost) - investment
rise_rate = profit / max_investment * 100
print("cost: ", cost)
print("shares: ", shares)
print("current price: ", cur_price)
print("investment: ", investment)
print("max investment: ", max_investment)
print("profit: ", max_investment)
print("rise rate: ", rise_rate)
# fio.reverseFile("./database/513030.csv")