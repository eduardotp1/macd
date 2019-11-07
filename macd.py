from backtesting import evaluateTick
from strategy import Strategy
from order import Order
from event import Event
import numpy as np

class MACD(Strategy):

    def __init__(self):
        self.signal = 0
        self.historic = []
        self.sizec = 12*7
        self.sized = 26*7
        self.convergence = 0
        self.divergence = 0
        self.macdHistoric = []
        self.size = 9*7
        self.macdExpMa = None

    def push(self, event):
        orders = []
        if event.type == Event.TRADE:
            price = event.price
            self.historic.append(price)

            if len(self.historic) == self.sized:
                alpha = 2/(self.sizec + 1)
                self.convergence = (1-alpha)*sum(self.historic[self.sized-self.sizec:])/self.sizec + alpha*self.convergence
                alpha = 2/(self.sized + 1)
                self.divergence = (1-alpha)*sum(self.historic)/self.sized + alpha*self.divergence

                macd = self.convergence - self.divergence
                self.macdHistoric.append(macd)

                if len(self.macdHistoric) == self.size:
                    
                    self.exponentialMa()
                    diff = macd - self.macdExpMa

                    if self.signal != 1 and diff > 0.001:
                        if self.signal == -1:
                            orders.append(Order(event.instrument, 1, 0))
                        orders.append(Order(event.instrument, 1, 0))
                        self.signal = 1
                    elif self.signal != -1 and diff < -0.001:
                        if self.signal == 1:
                            orders.append(Order(event.instrument, -1, 0))
                        orders.append(Order(event.instrument, -1, 0))
                        self.signal = -1

                    del self.macdHistoric[0]
                
                del self.historic[0]
        
        return orders

    def exponentialMa(self):
        if self.macdExpMa is None:
            self.macdExpMa = sum(self.macdHistoric)/self.size
        else:
            lastMa = self.macdExpMa
            alpha = 2/(self.size + 1)
            self.macdExpMa = (1 - alpha)*lastMa + alpha*self.macdHistoric[-1]


print(evaluateTick(MACD(), {'PETR4': '2018-03-07.csv'}))