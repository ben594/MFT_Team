import math
import pandas as pd

class Trader:
    def __init__(self):
        # Add any additional info you want
        pass

    def MakeTrades(self, time, stock_prices):
        """
        Grader will call this once per timestep to determine your buys/sells.
        Args:
            time: int
            stock_prices: dict[string -> float]
        Returns:
            trades: dict[string -> float] of your trades (quantity) for this timestep.
                Positive is buy/long and negative is sell/short.
        """
        trades = {}
        return trades


class BullishTrader(Trader):
    def MakeTrades(self, time, stock_prices):
        return {"Stock1": 1000000, "Stock2": 1000000, "Stock3": 1000000, "Stock4": 1000000}


class BearishTrader(Trader):
    def MakeTrades(self, time, stock_prices):
        return {"Stock1": -1000000, "Stock2": -1000000, "Stock3": -1000000, "Stock4": -1000000}


class SampleTrader(Trader):
    def MakeTrades(self, time, stock_prices):
        trades = {}
        # TODO: PICK HOW TO MAKE TRADES.
        trades['Stock1'] = 1000
        if 'Stock2' in stock_prices:
            if stock_prices['Stock2'] > 123:
                trades['Stock2'] = 1000
            else:
                trades['Stock2'] = -1000
        return trades


class BenTrader(Trader):
    def __init__(self):    
        self.weighted_avg_return = {"Stock1": 0, "Stock2": 0, "Stock3": 0, "Stock4": 0}
        self.history = {"Stock1": [1], "Stock2": [1], "Stock3": [1], "Stock4": [1]} 
        self.num_to_name = ["Stock1", "Stock2", "Stock3", "Stock4"]
        self.predicted_return = {"Stock1": 0, "Stock2": 0, "Stock3": 0, "Stock4": 0}
    
    def MakeTrades(self, time, stock_prices):
        trades = {}

        for i in range(4): 
            # currently at time t, but only know prices up to time t-1
            # estimate return from t-1 to t
            name = self.num_to_name[i]
            prev_price = stock_prices[name] # price at t-1
            prev_avg_return = self.weighted_avg_return[name] # average return until t-2
            prev_return = (prev_price - self.history[name][-1]) / self.history[name][-1] # return from t-2 to t-1
            self.history[name].append(prev_price) # add t-1 price to history
            if time < 10:
                cur_return = prev_return
            else:
                cur_return = prev_avg_return * 0.75 + prev_return * 0.25 # use average return until t-1 as return estimate from t-1 to t
            self.weighted_avg_return[name] = cur_return
            self.predicted_return[name] = cur_return
            
            quantity = 1
            if time >= 10:
                if math.fabs(prev_return) < math.fabs(prev_avg_return):
                    quantity = math.fabs(prev_return) / math.fabs(prev_avg_return) * 10
                else:
                    quantity = math.fabs(prev_return) / math.fabs(prev_avg_return) * 200
                quantity = int(quantity)
            
            quantity = min(quantity, 10000)
            
            # assume estimated return from t to t+1 is same as estimated return from t-1 to t
            if cur_return > 0:
                trades[name] = quantity
            else:
                trades[name] = -1 * quantity
        return trades