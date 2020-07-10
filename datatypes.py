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

class Account:
  __hold_cost = -1
  __hold_shares = -1
  __cur_price = -1
  __investment = -1
  __profit = -1
  __profit_rate = -1

  def __init__(self, hold_cost, hold_shares, cur_price, investment):
    self.__hold_cost = hold_cost
    self.__hold_shares = hold_shares
    self.__cur_price = cur_price
    self.__investment = investment
    self.__profit = hold_shares * (cur_price - hold_cost) - investment
    self.__profit_rate = self.__profit / investment * 100

  def getProfit(self):
    return self.__profit
  def getProfitRate(self):
    return self.__profit_rate
  def getHoldCost(self):
    return self.__hold_cost
  def getHoldShares(self):
    return self.__hold_shares
  def getCurPrice(self):
    return self.__cur_price
  def getInvestment(self):
    return self.__investment

class StrategyResult:
  __transaction_history = [] #record all the transaction history
  __in_process_transaction = [] #record buy actions that are not sold 
  __strategy_state = [] # list of Account items
  __max_investment = -1 
  __max_drawdown_rate = -1
  
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
        pre_hold_shares = self.__strategy_state[-1].getHoldShares()
        pre_hold_cost = self.__strategy_state[-1].getHoldCost()
        pre_investment = self.__strategy_state[-1].getInvestment()
        hold_shares = pre_hold_shares + t_shares
        hold_cost = (pre_hold_cost * pre_hold_shares + t_price * t_shares) / (hold_shares + t_shares)
        investment = pre_investment + t_price * t_shares
        print(investment)
    elif t_type == 'S':
        #use transaction profit to reduce hold cost
        pre_hold_cost = self.__strategy_state[-1].getHoldCost()
        pre_hold_shares = self.__strategy_state[-1].getHoldShares()
        pre_investment = self.__strategy_state[-1].getInvestment()
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
          self.__max_loss_rate = 0
          self.__max_investment = investment
        else:
          hold_cost = self.__strategy_state[-1].getHoldCost()
          hold_shares = self.__strategy_state[-1].getHoldShares()
          investment = self.__strategy_state[-1].getInvestment()
    self.__max_investment = max(self.__max_investment, investment)
    self.__max_loss_rate = min(self.__max_loss_rate, cur_price / hold_cost)      
    account = Account(hold_cost, hold_shares, cur_price, investment)
    self.__strategy_state.append(account)

  def getTransactionHistory(self):
    return self.__transaction_history
  def getLatestAccount(self):
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
  def getMaxLossRate(self):
    return self.__max_loss_rate
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
  

  
  
