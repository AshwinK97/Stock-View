from app import query
from plot import *
import pandas as pd

def Volume(ticker, date):
  volume_data = query("SELECT volume, date FROM Prices WHERE ticker_id = 1 AND date >= '{}' AND date <= '{}' ORDER BY price_id ASC".format(date[0], date[1]), [])

  volume_df = pd.DataFrame(volume_data.fetchall())
  volume_df.columns = ['volume', 'date']

  return bar("Volume", volume_df.date.tolist(), volume_df.volume.tolist())

#def RSI():
#  return 4
#def SMA():
#
#def MACD():
#
#def OBV():
#
#def VWAP():