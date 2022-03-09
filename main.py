import yfinance as yf
import pandas_datareader as pdr
from stockstats import StockDataFrame
import pandas as pd
import investpy

symbols = investpy.stocks.get_stocks(country="Thailand")
print("🚀 Get Total thai stocks  length: ", len(symbols))
symbols = list(symbols["symbol"])

# filter stock symbol not UPPER_CASE (for invester not take action with stock no_name)
symbols = [symbol for symbol in symbols if symbol.upper() == symbol]

print("💹 Filtered symbol UPPER_CASE thai stocks: ", len(symbols))

start = "2022-01-01"
# if end more than current time will get data from start date to current date
end = "2022-10-30"

countMatch = 0

for s in symbols:

    df = yf.download(
        s + ".BK", start=start, end=end, progress=False, interval="1d", show_errors=False)

    try:

        stock = StockDataFrame.retype(df)
        cols = ["open", "high", "low", "close", "volume",
                "volume_20_sma", "close_20_ema", "close_200_ema", "rsi_14"]
        stock = stock[cols]

        # # indicator for analysis
        currentStockIndex = stock.index.values[-1]
        currentStock = stock.iloc[-1]

        is_vol_more_than_vol_20_sma = currentStock[4] > currentStock[5]

        # #  oversold
        is_rsi_14_at_least_30 = currentStock[8] < 30

        if is_vol_more_than_vol_20_sma and is_rsi_14_at_least_30:
            print("📢 "+s + " info")
            print("Date :", currentStockIndex)
            print("💹 vol > vol_20_sma : ",     is_vol_more_than_vol_20_sma)
            print("💹 oversold : ", is_rsi_14_at_least_30)
            print("-----------------")
            countMatch = countMatch + 1

    except:
        continue

print('🔥 Got total match ', countMatch)
print("========= End stock scanned ========")
