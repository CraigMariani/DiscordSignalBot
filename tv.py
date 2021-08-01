from pandas.io.pytables import IndexCol
from tradingview_ta import TA_Handler, Interval, Exchange
import pandas as pd 


tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)
print(tesla.get_analysis().summary)
# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

# tesla_dataframe = pd.DataFrame.from_dict(tesla.get_analysis().moving_averages)

# SMA10 = tesla_dataframe.iloc[8]
# SMA20 = tesla_dataframe.iloc[10]
# # print(tesla_dataframe)
# print(SMA20.name)
# print(SMA20['RECOMMENDATION'])
# print(SMA10.name)
# print(SMA10['RECOMMENDATION'])