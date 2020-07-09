import FileIO as fio
class ETF:
  __close_price = []
  __open_price = []
  __high_price = []
  __low_price = []
  __trading_volume = []
  __rise_rate = []
  __date = []
  __history_length = -1
  def __init__(self, filename):
    self.__date, self.__close_price, self.__open_price, self.__high_price, self.__low_price, \
      self.__trading_volume, self.__rise_rate = fio.readFile(filename)
    self.__history_length = len(self.__close_price)
    
  def getClosePrice(self):
    return self.__close_price
  def getOpenPrice(self):
    return self.__open_price
  def getHistoryLength(self):
    return self.__history_length
  def dump(self):
    for item in self.__date:
      print(item)

class StrategyResult:
  __transaction_history = [] #record all the transaction history
  __in_process_transaction = [] #record buy actions that are not sold 
  __strategy_state = [] # tuple of (hold_cost, hold_shares, cur_price, investment)
  __max_investment = -1
  
  #def __init__(self):
  #t_type means transaction type, t for transaction
  #same for other variables
  def addTransaction(self, t_type, t_date, t_price, t_shares, t_profit):
    #each element of transaction history list is a four-element tuple
    self.__transaction_history.append((t_type, t_date, t_price, t_shares, t_profit))
    if(t_type == 'B'):
      self.__in_process_transaction.append((t_price, t_shares))
  def updateProfit(self, t_type, t_price, cur_price, t_shares):
    hold_cost = -1
    hold_shares = -1
    investment = -1
    if t_type == 'B':
        pre_hold_shares = self.__strategy_state[-1][1]
        pre_hold_cost = self.__strategy_state[-1][0]
        pre_investment = self.__strategy_state[-1][3]
        hold_shares = pre_hold_shares + t_shares
        hold_cost = (pre_hold_cost * pre_hold_shares + t_price * t_shares) / (hold_shares + t_shares)
        investment = pre_investment + t_price * t_shares
        self.__max_investment = max(self.__max_investment, investment)
        print(investment)
    elif t_type == 'S':
        #use transaction profit to reduce hold cost
        pre_hold_cost = self.__strategy_state[-1][0]
        pre_hold_shares = self.__strategy_state[-1][1]
        pre_investment = self.__strategy_state[-1][3]
        t_earnings = t_shares * (t_price - pre_hold_cost)
        hold_shares = pre_hold_shares - t_shares
        hold_cost = hold_cost - t_earnings / hold_shares
        investment = pre_investment - t_shares * t_price * 0.95
        print(investment)
    else:
        #buy 100 shares at the day start investing
        if len(self.__strategy_state) == 0:  #first day
          hold_cost = cur_price
          hold_shares = 100
          investment += hold_cost * hold_shares
        else:
          hold_cost = self.__strategy_state[-1][0]
          hold_shares = self.__strategy_state[-1][1]
          investment = self.__strategy_state[-1][3]
    self.__strategy_state.append((hold_cost, hold_shares, cur_price, investment))

  def getTransactionHistory(self):
    return self.__transaction_history
  def getProfit(self):
    return self.__strategy_state[-1]
    # cost = self.__strategy_state[-1][0]
    # shares = self.__strategy_state[-1][1]
    # cur_price = self.__strategy_state[-1][2]
    # print("cost", cost)
    # print("shares", shares)
    # print("current price", cur_price)
    # return (cur_price - cost) * shares

  def getStrategyState(self):
    return self.__strategy_state
  def getInProgressTransaction(self):
    return self.__in_process_transaction
  def getMaxInvestment(self):
    return self.__max_investment
  def getSellHistory(self):
    sell_history = []
    for tranc in self.__transaction_history:
      if tranc[0] == 'S':
        sell_history.append(tranc[1], tranc[2])
    return sell_history
  def getBuyHistory(self):
    buy_history = []
    for tranc in self.__transaction_history:
      if tranc[0] == 'B':
        buy_history.append(tranc[1], tranc[2])
  