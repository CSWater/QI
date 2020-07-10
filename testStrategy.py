import pandas as pd
import numpy as np
import plot
import strategy as st
import datatypes as dt
import FileIO as fio

etf_513030 = dt.ETF("./database/513030.csv")
grid_strategy = st.GridStrategy(2000, 1.2, 0.05, 0.05)
res_513030 = grid_strategy.executeStrategy(etf_513030)
account = res_513030.getLatestAccount()
max_investment = res_513030.getMaxInvestment()
max_loss_rate = res_513030.getMaxLossRate()
shares = account.getHoldShares()
cost = account.getHoldCost()
cur_price = account.getCurPrice()
investment = account.getInvestment()
profit = account.getProfit()
profit_rate = account.getProfitRate()
# profit = shares * (cur_price - cost) - investment
# rise_rate = profit / max_investment * 100
print("cost: ", cost)
print("shares: ", shares)
print("current price: ", cur_price)
print("investment: ", investment)
print("max investment: ", max_investment)
print("profit: ", max_investment)
print("max loss rate: ", max_loss_rate)
print("rise rate(price/cost): ", profit_rate)
print("profit rate(profit / max_investment): ", profit / max_investment)

# fio.reverseFile("./database/513030.csv")