import time
from binance.client import Client
from binance.client import BinanceAPIException
import numpy as np
import talib as ta

# api_key=""
# api_secret=""

# client = Client(api_key, api_secret)
# symbol = "BTCUSDT"
# interval = "1m"
# limit = "500"
# klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
# open = [float(entry[1]) for entry in klines]
# close = [float(entry[4]) for entry in klines]
# high = [float(entry[2]) for entry in klines]
# low = [float(entry[3]) for entry in klines]


def ema_formül(src,time_period):
    alpha = 2 / (time_period + 1)
    first_ema = sum(src[:time_period]/time_period)
    ema_list = []
    for close in src:
        if len(ema_list)==0:
            ema = alpha*close + (1-alpha)*first_ema
        else:
            ema = alpha*close + (1- alpha)* ema_list[-1]
        ema_list.append(ema)

    return ema_list

def ema_mum_hesapla(close):
    
    close_array =  np.asanyarray(close)
    close_finished = close_array[:-1]

    ema = ema_formül(close_finished,200)

    return ema

def ema_trend(high,low,close):

    ema = round(ema_mum_hesapla(close)[-1],2)
    

    if high[-2] < ema :

        trend = "Ayı"

    elif low[-2] > ema :

        trend = "Boğa"

    else:

        trend = "Nötr"

    return trend

def sar_hesapla(high,low):


    high_array = np.asanyarray(high)
    low_array = np.asanyarray(low)
    high_finished = high_array[:-1]
    low_finished = low_array[:-1]
    sar = ta.SAR(high = high_finished,low = low_finished)
    
    return sar

def sar_trend(high,low,close):

    ema= round(ema_mum_hesapla(close)[-1],2)
    sar = round(sar_hesapla(high,low)[-1],2)

    if sar >ema :

        sinyal = "Boğa"

    elif sar < ema:

        sinyal = "Ayı"

    return sinyal

def sar_sinyal(high,low,open):

    sar_deger = round(sar_hesapla(high,low)[-1],2)

    sar_deger1 = round(sar_hesapla(high,low)[-2],2)

    if open[-2] > sar_deger and open[-3] < sar_deger1:

        sinyal = "Boğa"

    elif open[-2] < sar_deger and open[-3] > sar_deger1:

        sinyal = "Ayı"

    else:
        
        sinyal = "Nötr"

    return sinyal






