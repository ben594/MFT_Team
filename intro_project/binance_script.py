import requests
import time

url = 'https://data.binance.com/api/v3/aggTrades'
symbol = 'BTCUSDT'
end_time = time.time()
start_time = end_time - 300 * 1000
limit = 10000
params = {'symbol': symbol, 'limit': limit}

trades = requests.get(url, params).json()
cur_time = time.time()

vol_weighted_sum = 0
total_quantity = 0
index = len(trades) - 1
while index >= 0:
    trade = trades[index]
    if cur_time - int(trade['T']) > 300 * 1000:
        break
    qty = float(trade['q'])
    price = float(trade['p'])
    vol_weighted_sum += qty * price
    total_quantity += qty
    # print(trade)
    index -= 1

vol_weighted_avg_price = vol_weighted_sum / total_quantity
print("Volume weighted average price of BTCUSDT: ", vol_weighted_avg_price)