from get_tickers import Get_Tickers 
from secret import Secret

from discord.ext import commands, tasks 
from tradingview_ta import TA_Handler, Interval, Exchange 
import pytz
import datetime as dt
import pandas as pd

gt = Get_Tickers()

tickers = gt.penny_stocks()

tz_pacific = pytz.timezone('US/Pacific')
datetime_pacific = dt.datetime.now(tz_pacific)
current_time = datetime_pacific.strftime("%H:%M:%S")
now = dt.datetime.now()
market_open = now.replace(hour=6, minute=30, second=0, microsecond=0, tzinfo=tz_pacific) # 6:30 am 
market_close = now.replace(hour=13, minute=0, second=0, microsecond=0, tzinfo=tz_pacific) # 1:00 pm  

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("The bot is ready!")
    if datetime_pacific > market_open and datetime_pacific < market_close:
        print('market open')
        await bot.get_channel(Secret.signal_channel_id).send("The market is open")

# shows current stocks
@bot.command(name='show_stocks')
async def stock(ctx):
    tickers_dataframe = pd.DataFrame({'Tickers' : tickers})
    await ctx.send(tickers_dataframe.to_string())

# shows current time
@bot.command(name='show_time')
async def time(ctx):
    await ctx.send(current_time)

@tasks.loop(hours=1)
async def show_signal():
    message_channel = bot.get_channel(Secret.signal_channel_id)
    data = []
    signals = {}

    for ticker in tickers:

        try:
            current_ticker = TA_Handler(
                symbol=ticker,
                screener="america",
                exchange="NASDAQ",
                interval=Interval.INTERVAL_1_DAY
            )

            # current_ticker = pd.DataFrame.from_dict(current_ticker.get_analysis().moving_averages)
            current_ticker = current_ticker.get_analysis().summary
            data.append({
                'ticker' : ticker, 
                'signal' : current_ticker['RECOMMENDATION']
                })
            # signals.append('{} : {}'.format(ticker, current_ticker['RECOMMENDATION']))
            # await message_channel.send('{} : {}'.format(ticker, current_ticker['RECOMMENDATION']))

        except (RuntimeError, Exception) as e:
            # signals.append('{} : {}'.format(ticker, e))
            print('{} : {}'.format(ticker, e))
    signals = pd.DataFrame(data)
    await message_channel.send(signals.to_string())
    # await message_channel.send(data)

@show_signal.before_loop
async def before():
    await bot.wait_until_ready()

show_signal.start()
bot.run(Secret.token)



