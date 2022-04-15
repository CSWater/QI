
def searchSeg(startDate, historyData, midPrice):
  #init high point
  high_price = historyData[startDate]
  drop_base = 0.1
  transaction = []
  sum = 0.0
  for date_id in range(startDate, startDate+1250):
    #sell
    if len(transaction) > 0 and historyData[date_id] > transaction[-1] * 1.05 :
      transaction.pop()
      sum += 0.05
      drop_base = 0.1
      #new high point pre > now
    #buy
    else:
      drop_rate = (high_price - historyData[date_id]) / high_price
      if drop_rate >= drop_base:
        buy_price = high_price * (1 - drop_rate)
        transaction.append(buy_price)
        drop_base -= 0.1
    #update high price
    if drop_rate == 0.1 and historyData[date_id - 1] > historyData[date_id]:
      if historyData[date_id - 1] > high_price:
        high_price = historyData[date_id - 1]
      if(high_price > midPrice):
        high_price = midPrice
    print(sum)