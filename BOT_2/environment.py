import numpy as np
import pickle
import matplotlib.pyplot as plt

class Stock:
    'generic stock class'
    starting_capital = 1000
    capital = 1000
    stocks_holding = 0
    day = 0
    nb_days = 0
    data = []

    #graph data value
    graph_stk = []
    graph_holding = []

    reward_buy_nocapital = -1
    reward_sell_nostock = -1

    def __init__(self):
        self.stocks_holding = 0
        self.starting_capital = 1000
        self.capital = self.starting_capital
        self.data = pickle.load(open('pickles/stock/WIKI_GE','rb'))
        self.day = 0
        self.nb_days = len(self.data)-1
        self.reward_buy_nocapital = -1
        self.reward_sell_nostock = -1
        self.graph_stk = []

    def reset(self):
        self.stocks_holding = 0
        self.capital = self.starting_capital
        self.day = 0
        self.graph_stk = []
        return self.observation()

    def step(self,action):
        reward = 0
        if action == 0: #buy
            reward = self.buy()
        elif action == 1:    #sell
            reward = self.sell()
        elif action == 2:   #hold
            reward = self.hold()
        #go to the next day
        obs = self.observation()
        self.day = self.day + 1
        done = False
        if(self.nb_days == self.day):
            plt.plot(self.graph_holding)
            plt.show()
            done = True
        info = None
        return obs,float(reward),done,info

    def buy(self):
        i = self.day
        stock_today = self.data.iloc[i]['Close']
        nb_stocks_buyable = int(self.capital/stock_today)
        #Check if there is no capital
        if(nb_stocks_buyable == 0):
            return self.reward_buy_nocapital
        else:
            self.capital = self.capital - (stock_today*nb_stocks_buyable)
            self.stocks_holding = self.stocks_holding + nb_stocks_buyable
            return self.stocks_holding*stock_today

    def sell(self):
        i = self.day
        stock_today = self.data.iloc[i]['Close']
        if(self.stocks_holding == 0):
            return self.reward_sell_nostock
        else:
            self.capital = self.capital +(self.stocks_holding*stock_today)
            self.stocks_holding = 0
            return self.capital - self.starting_capital*1000

    def hold(self):
        return -1

    def observation(self):
        """[captial,stockvalue,prediction,stocks_holding]"""
        i = self.day
        stock_today = self.data.iloc[i]['Close']
        stock_tomorrow = self.data.iloc[i+1]['Close']
        diff = 0
        if (stock_tomorrow-stock_today)<0:
             diff = 0
        else:
            diff = 1
        # prediction is only 87% accurate
        if np.random.uniform() < 0.23:
            if(diff==0):
                diff = 1
            else:
                diff = 0
        l = []
        l.append(self.capital)
        l.append(stock_today)
        l.append(diff)
        l.append(self.stocks_holding)
        # graphing
        self.graph_stk.append(stock_today)
        self.graph_holding.append(self.stocks_holding)
        return l
