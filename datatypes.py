import FileIO as fio
""" class DayData:
  def close_price() """
class ObjectDayData:
  def __init__(self):
    self.close_price :float= 0
    self.open_price :float= 0
    self.high_price :float= 0
    self.low_price :float= 0
    self.trading_volume :float= 0
    self.rise_rate :float= 0
    self.date :str = 19901201
  def __init__(self, cp:float, op:float, hp:float, lp:float, tv:float, rr:float, date:str):
    self.close_price :float= cp
    self.open_price :float= op
    self.high_price :float= hp
    self.low_price :float= lp
    self.trading_volume :float= tv
    self.rise_rate :float= rr
    self.date :str= date
  
class ETFObject:
  __index = 0
  __length = 0
  def __init__(self, id:str):
    self.id = id
    self.data :list[ObjectDayData]= []
  def __init__(self, id:str, etf:list[ObjectDayData]):
    self.id = id
    self.data :list[ObjectDayData]= etf
  def __getitem__(self, k):
    return self.data[k]
  def __setitem__(self, k, v):
    self.data[k] = v
  def __iter__(self):
    return self 
  def __next__(self):
    if self.__index < self.__length:
      ret = self.data[self.__index]
      self.__index += 1
      return ret
    else:
      raise StopIteration 

      
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
  

#class to descripe one transaction
class Transaction:
  #init function
  def __init__(self) -> None:
    self.investment_id = '000000'
    self.t_type :str= 'N'        
    self.t_date = 19901201   
    self.t_price :float= 0.0       
    self.t_share :float= 0.0  
  def __init__(self, investment_id:str, t_type:str, t_date:str, t_price:float, t_share:float) -> None:
    self.investment_id = investment_id    #投资品种
    self.t_type :str= t_type        #transaction type, B, S, N for buy, sell, undefine
    self.t_date = t_date        #transaction date
    self.t_price :float= t_price      #trade price of the transaction
    self.t_share :float= t_share      #trade shares of the transaction
  #set functions
  def set_date(self, t_date):
    self.t_date = t_date
  def set_type(self, t_type):
    self.t_type = t_type
  def set_price(self, t_price):
    self.t_price = t_price
  def set_share(self, t_share):
    self.t_share = t_share
  #get functions
  def get_date(self):
    return self.t_date
  def get_type(self):
    return self.t_type
  def get_price(self):
    return self.t_price
  def get_share(self):
    return self.t_share
  def isBuy(self):
    return self.t_type == 'B'
  def isSell(self):
    return self.t_type == 'S'
  
#Transaction history
class TransactionHistory:
  def __init__(self):
    self.history: list[Transaction] = []
  def __init__(self, trans_history: list[Transaction]):
    self.history: list[Transaction] = trans_history
  
  #return the history length
  def len(self):
    return len(self.history)
  #return the last transaction
  def top(self):
    return self.history[-1]
  #add one transaction, transaction history would never delete an item
  #since history can not be changed
  def add(self, trans:Transaction):
    self.history.append(trans)
  #override []
  def __getitem__(self, k):
    return self.history[k]
  def __setitem__(self, k, v):
    self.history[k] = v
  #return all the buy transactions
  def getAllBuys(self) -> list[Transaction]:
    buys :list[Transaction]= []
    for trans in self.history:
      if trans.isBuy():
        buys.append(trans)
    return buys
  #return all the sell transactions
  def getAllSells(self) -> list[Transaction]:
    sells :list[Transaction]= []
    for trans in self.history:
      if trans.isSell():
        sells.append(trans)
    return sells
  #return interval transactions
  #todo
    
    

#一个投资实例由交易品种，交易策略，交易历史构成
#是在一个给定品种，给定区间上运行给定策略的结果
class InvestmentCase:
  def __init__(self):
    self.investment_id = '000000'
    self.investment_strategy = None
    self.transaction_history = []
  def __init__(self, invest_id, invest_strategy):
    self.investment_id = invest_id
    self.investment_strategy = invest_strategy
    self.transaction_history = []
  def __init__(self, invest_id, invest_strategy, trans_history):
    self.investment_id = invest_id
    self.investment_strategy = invest_strategy
    self.transaction_history = trans_history
  #set methods
  def setInvestId(self, invest_id):
    self.investment_id = invest_id
  def setInvestStrategy(self, invest_strategy):
    self.investment_strategy = invest_strategy
  def setTransHistory(self, trans_history):
    self.transaction_history = trans_history
   
#投资账户由不同的投资实例组成
class InvestmentAccount:
  def __init__(self) -> None:
    self.investment_case = []      #投资品种实例列表
  
  #add new investment case
  def addInvestment(self, invest_case):
    self.investment_case.append(invest_case)
  #clear an investment case
  def clearInvestment(self, invest_id):
    for invest_case in self.investment_case:
      if invest_id == invest_id.getID():
        self.investment_case.remove(invest_case)
