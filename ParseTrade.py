# 10/10/2019 Chaoyi Ye
# Parses trades from NASDAQ_ITCH50 and Calculate VWAP
import gzip
import struct
import datetime
from pandas import DataFrame
import time
from datetime import timedelta

class PARSER():

    def __init__(self):
        self.times = []
        self.volumes = []
        self.tickers = []
        self.prices = []

    def ProcessMessage(self, filename) :
        # make sure .gz file is in the working directory
        with gzip.open(filename, "rb") as f:

            for _ in range(4000000):
                msg_size = int.from_bytes(f.read(2), byteorder='big', signed=False)
                msg_type = f.read(1).decode('ascii')
                if(msg_type == "S"):
                    f.read(msg_size - 1)
                elif(msg_type == "R"):
                    f.read(msg_size - 1)
                elif(msg_type == "H"):
                    f.read(msg_size - 1)
                elif(msg_type == "Y"):
                    f.read(msg_size - 1)
                elif(msg_type == "L"):
                    f.read(msg_size - 1)
                elif(msg_type == "V"):
                    f.read(msg_size - 1)
                elif(msg_type == "W"):
                    f.read(msg_size - 1)
                elif(msg_type == "K"):
                    f.read(msg_size - 1)
                elif(msg_type == "A"):
                    f.read(msg_size - 1)
                elif(msg_type == "F"):
                    f.read(msg_size - 1)
                elif(msg_type == "E"):
                    f.read(msg_size - 1)
                elif(msg_type == "C"):
                    f.read(msg_size - 1)
                elif(msg_type == "X"):
                    f.read(msg_size - 1)
                elif(msg_type == "D"):
                    f.read(msg_size - 1)
                elif(msg_type == "U"):
                    f.read(msg_size - 1)
                elif(msg_type == "P"):

                    trade_msg = f.read(msg_size - 1)
                    (time, volume, ticker, price) = self.ExtractTrade(trade_msg)
                    self.times.append(time)
                    self.volumes.append(volume)
                    self.tickers.append(ticker)
                    self.prices.append(price)

                elif(msg_type == "Q"):
                    f.read(msg_size - 1)
                elif(msg_type == "B"):
                    f.read(msg_size - 1)
                elif(msg_type == "I"):
                    f.read(msg_size - 1)
                elif(msg_type == "N"):
                    f.read(msg_size - 1)


    # A helper method for translate bytes to readable string, int, double
    def ExtractTrade(self, trade_msg) :

        result = struct.unpack('>HH6sQsI8sIQ',trade_msg)
        stamp = result[2]
        t = int.from_bytes(stamp, byteorder='big')
        x='{0}'.format(timedelta(seconds=t * 1e-9))
        hr=int(x.split(':')[0])
        #time = datetime.datetime.fromtimestamp(t / 1e9).strftime("%Y-%m-%d,%H")
        volume = result[5]
        ticker = result[6].strip().decode("utf-8")
        price = result[7]/10000.00

        return hr, volume, ticker, price

    # Calculate volume-weighted average price
    # This method would return a dictionary with ticker as keys and DataFrame as values
    def VWAP(self) :
        df = DataFrame({'Time': self.times, 'Tickers': self.tickers,
        'Prices': self.prices, 'Volumes': self.volumes})
        # create a dictionary to store vwap of each stock, so it is easy to find the stock you want
        dict_vwap = {}
        df['P*V']=df['Prices']* df['Volumes']
        # group by tickers first
        dict_by_Tickers = {k: v for k, v in df.groupby('Tickers')}
        # loop through every ticker
        for i in dict_by_Tickers:
            df2 = dict_by_Tickers[i].groupby(dict_by_Tickers[i]['Time'])['P*V', 'Volumes'].sum()
            df2['VWAP'] = round(df2['P*V']/df2['Volumes'],3)
            dict_vwap.update({i : df2})
        return dict_vwap
