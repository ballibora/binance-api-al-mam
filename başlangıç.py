from binance.client import Client
from os import *
import json

# api_key=""
# api_secret=""
client = Client(api_key, api_secret)
account = client.futures_account_balance()

def anamenu():
    system("cls")
    print("*"*50)
    print("ANAMENU")
    print("*"*50)
    print("1-Varlıklarım")
    print("2-Açık Emirlerim")
    print("3-Açık Pozisyonum")
    tercih=int(input("Tercih gir"))
    if tercih==1:
        varliklarim()
    elif tercih==2:
        acikemirlerim()
    elif tercih ==3:
        acikpozisyon()
    else:
        quit()


def varliklarim():

    system("cls")
    print("*"*50)
    print("VARLIKLARIM")
    print("*"*50)

    account = client.futures_account_balance()

    for assets in account:
        asset = assets["asset"]
        balance = assets["balance"]
        print(f"asset: {asset}")
        print(f"balance: {balance}")
        print("-"*50)
    
    input("Herhangi bir tuşa basın")
    anamenu()

def acikemirlerim():

    system("cls")
    print("*"*50)
    print("AÇIK EMİRLERİM")
    print("*"*50) 

    emirler = client.futures_get_open_orders(symbol="BTCUSDT")
    if len(emirler) == 0 :
        print("Açık emrin yok.")
        print("-"*50)
    else:
        print(emirler)
        print("-"*50)

    input("Herhangi bir tuşa basın")
    anamenu()

def acikpozisyon():

    system("cls")
    print("*"*50)
    print("AÇIK POZİSYONUM")
    print("*"*50) 

    pozisyon = client.futures_position_information(symbol="BTCUSDT")

    for i in pozisyon:
        sembol = i["symbol"]
        miktar = i["positionAmt"]
        giris = i["entryPrice"]
        kar = i["unRealizedProfit"]
        tip = i["marginType"]
        yon = i["positionSide"]
        margin = i["isolatedMargin"]
        if float(giris) <= 0 :
            print("Açık pozisyonun yok.")
            print("-"*50)
        elif float(giris) > 0 :
            print(f"symbol: {sembol}")
            print(f"işlem yönü: {yon}")
            print(f"miktar: {miktar}")
            print(f"giriş fiyatı: {giris}")
            print(f"marjin miktarı: {margin}")
            print(f"marjin tipi: {tip}")
            print(f"kar/zarar: {kar}")
            print("-"*50)
      
    input("Herhangi bir tuşa basın")
    anamenu()

anamenu()




