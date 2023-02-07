import pandas as pd
from trader_class import Trader, SampleTrader
from enum import Enum, auto
from typing import Type
from attr import dataclass
from math import floor

MAX_NOTIONAL_TOTAL = 1_000_000
MAX_NOTIONAL_STOCK = 600_000


@dataclass
class SimulationResults:
    pnl: float
    history: Type[pd.DataFrame]


class Game:
    def __init__(self, trader: Type[Trader], price_history) -> None:
        self.trader = trader
        self.price_history = price_history[0:600]
        print("price history: ", self.price_history)

    def run_game(self, delay_list, simple=True, n_stocks=4):
        stock_list = [f"Stock{s}" for s in range(1, n_stocks+1)]
        position_dict = {stock: [] for stock in stock_list}
        bought_data_list = [
            stock+"_Delay" if stock in delay_list else stock for stock in stock_list]
        price_history_bought = self.price_history.loc[:, bought_data_list]

        for idx, row in price_history_bought.iterrows():
            trades = self.trader.MakeTrades(idx, row)
            net_notional = 0
            for stock in stock_list:
                allowed_notional = min(
                    MAX_NOTIONAL_TOTAL - net_notional, MAX_NOTIONAL_STOCK)
                curr_price = row[stock]
                allowed_size = floor(allowed_notional/curr_price)
                intended_size = trades[stock] if stock in trades else 0
                allowed_pos = min(
                    max(intended_size, -allowed_size), allowed_size)
                net_notional += allowed_pos*curr_price
                position_dict[stock].append(allowed_pos)

        price_history = self.price_history.loc[:, stock_list]
        shifted_price_history = price_history.shift(
            -1).fillna(method="ffill")
        price_history = price_history.merge(
            shifted_price_history, left_index=True, right_index=True, suffixes=("", "_Next"))
        df_position = pd.DataFrame(position_dict)
        df_position = price_history.merge(
            df_position, left_index=True, right_index=True, suffixes=("", "_Positions"))
        df_position["Pnl"] = 0
        for stock in stock_list:
            df_position[stock+"_Pnl"] = (df_position[stock+"_Next"] -
                                         df_position[stock]) * df_position[stock+"_Positions"]
            df_position["Pnl"] += df_position[stock + "_Pnl"]
        return SimulationResults(pnl=df_position["Pnl"].sum(), history=df_position)
