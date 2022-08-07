from fonksiyonlarım import *
import time
from binance.client import Client
from binance.client import BinanceAPIException
from datetime import datetime

api_key = ""
api_secret = ""

client = Client(api_key=api_key, api_secret=api_secret,testnet= True)

symbol = "BTCUSDT"
interval = "1m"
limit = "500"

print("Başlıyor")

while True:

    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    open = [float(entry[1]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    zaman = datetime.now()
    zaman = datetime.ctime(zaman)

    sar = sar_trend(high,low,close)
    ema = ema_trend(high,low,close)
    sar_deger = sar_hesapla(high,low)
    sar_s = sar_sinyal(high,low,open)



    if ema == "Boğa" and sar == "Boğa" and sar_s == "Boğa":

        sinyal = "Long"

        print(zaman)

        print("-"*50)

        print(sinyal)

        print("-"*50)

    elif ema == "Ayı" and sar == "Ayı" and sar_s == "Ayı":

        sinyal = "Short"

        print(zaman)

        print("-"*50)

        print(sinyal)

        print("-"*50)

    else:

        sinyal = "Yok"

    pozisyon=client.futures_position_information(symbol = "BTCUSDT")

    if float(pozisyon[0]["positionAmt"]) != 0 :

        pozisyon_yok = False
    else:

        pozisyon_yok = True

    acık_emirler = client.futures_get_open_orders(symbol="BTCUSDT")   

    if len(acık_emirler) == 0:
        acık_emir_var = False
    else:
        acık_emir_var = True


    if pozisyon_yok :

        

        if sinyal == "LONG":

            premium_index = client.futures_mark_price(symbol="BTCUSDT")
            mark_price = float(premium_index["markPrice"])
            account = client.futures_account_balance()
            usdt_balance = account[1]["balance"]
            usdt_balance = float(usdt_balance)
            maxq = (usdt_balance*5)/mark_price
            maxq = str(maxq)
            maxq = maxq[0:5]
            maxq = float(maxq)

            client.futures_create_order(symbol="BTCUSDT", 
                                side="BUY",                            
                                type = "MARKET", 
                                quantity = maxq,
                                )

            pozisyon=client.futures_position_information(symbol = "BTCUSDT")
            giris = float(pozisyon[0]["entryPrice"])
            miktar = float(pozisyon[0]["positionAmt"])
            stop = sar_deger
            yüzde = (giris - stop)/giris*100
            if yüzde >= 0.5 :
                karstop = giris + giris/100
                karstop = round(karstop,2)
            else:
                karstop = giris + (giris-stop)*2
                karstop = round(karstop,2)

            client.futures_create_order(symbol = "BTCUSDT", 
                                side = "SELL",
                                type = "STOP_MARKET", 
                                timeInForce = "GTC",
                                reduceOnly = True, 
                                quantity = miktar, 
                                stopPrice = stop,
                                )
            client.futures_create_order(symbol = "BTCUSDT", 
                                side ="SELL",
                                type = "LIMIT",
                                timeInForce = "GTC",
                                reduceOnly = True, 
                                price = karstop, 
                                quantity = miktar,
                                )
        elif sinyal == "SHORT":
            premium_index = client.futures_mark_price(symbol="BTCUSDT")
            mark_price = float(premium_index["markPrice"])
            account = client.futures_account_balance()
            usdt_balance = account[1]["balance"]
            usdt_balance = float(usdt_balance)
            maxq = (usdt_balance*5)/mark_price
            maxq = str(maxq)
            maxq = maxq[0:5]
            maxq = float(maxq)

            client.futures_create_order(symbol="BTCUSDT", 
                            side="SELL",                            
                            type = "MARKET", 
                            quantity = maxq,
                            )
            
            pozisyon=client.futures_position_information(symbol = "BTCUSDT")
            giris = float(pozisyon[0]["entryPrice"])
            miktar = - float(pozisyon[0]["positionAmt"])
            stop = sar_deger
            yüzde = - (giris - stop)/giris*100

            if yüzde >= 0.50 :
                karstop = giris- giris/100
                karstop = round(karstop,2)
            else:
                karstop = giris - (stop - giris)*2
                karstop = round(karstop,2)
            
            client.futures_create_order(symbol = "BTCUSDT", 
                                side = "BUY",
                                type = "STOP_MARKET", 
                                timeInForce = "GTC",
                                reduceOnly = True, 
                                quantity = miktar,
                                stopPrice = stop,
                                )
            
            client.futures_create_order(symbol = "BTCUSDT", 
                                side ="BUY",
                                type = "LIMIT",
                                timeInForce = "GTC",
                                reduceOnly = True, 
                                price = karstop, 
                                quantity = miktar,
                                )

        elif acık_emir_var:

            client.futures_cancel_all_open_orders(symbol="BTCUSDT")  


    
    

    time.sleep(1)
