from backtesting import evaluateTick
from strategy import Strategy
from order import Order
from event import Event
import numpy as np

class MACD(Strategy):

    def __init__(self):
        self.signal = 0
        self.hist = []
        self.sizec = 12*7
        self.sized = 26*7
        self.conv = 0
        self.div = 0
        self.macd_hist = []
        self.size = 9*5
        self.exp_mm = None

    def push(self, event):
        orders = []
        if event.type == Event.TRADE:
            price = event.price
            self.hist.append(price)

            if len(self.hist) == self.sized:
                a = 2/(self.sizec + 1)
                self.conv = (1-a)*sum(self.hist[self.sized-self.sizec:])/self.sizec + a*self.conv
                a = 2/(self.sized + 1)
                self.div = (1-a)*sum(self.hist)/self.sized + a*self.div
                macd = self.conv - self.div
                # print(macd)
                self.macd_hist.append(macd)

                if len(self.macd_hist) == self.size:
                    if self.exp_mm is None:
                        self.exp_mm = sum(self.macd_hist)/self.size
                    else:
                        new_mm = self.exp_mm
                        a = 2/(self.size + 1)
                        self.exp_mm = (1 - a)*new_mm + a*self.macd_hist[-1]
                    diff = macd - self.exp_mm


                    if self.signal != 1 and diff > 0.001:
                        if self.signal == -1:
                            # print(orders)
                            orders.append(Order(event.instrument, 1, 0))
                        orders.append(Order(event.instrument, 1, 0))
                        self.signal = 1

                        
                    elif self.signal != -1 and diff < -0.001:
                        if self.signal == 1:
                            # print(orders)
                            orders.append(Order(event.instrument, -1, 0))
                        orders.append(Order(event.instrument, -1, 0))
                        self.signal = -1
                    del self.macd_hist[0]
                del self.hist[0]
        return orders



print(evaluateTick(MACD(), {'PETR4': '2018-03-07.csv'}))