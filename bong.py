import pyupbit 
import pandas 
import datetime 
import time

access = "access key"   # access key
secret = "secret key"   # secret key

upbit = pyupbit.Upbit(access, secret)


def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")


# 이용할 코인 리스트 
coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-DOT"] # Coin ticker 추가 
lower28 = []


# 시장가 매수 함수 
def buy(coin): 
    money = upbit.get_balance("KRW") 
    if money > 501000 : 
        res = upbit.buy_market_order(coin, 500000) 
    return

# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(), "Sold")
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount)     
    return

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    

while(True):
    for i in range(len(coinlist)):
        try :
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
            now_rsi = rsi(data, 14).iloc[-1]            
            av_buy = float(upbit.get_avg_buy_price(coinlist[i]))
            profit_price = round(av_buy*1.02, 4)   
            
            print(coinlist[i], "< RSI > :", now_rsi)

            if now_rsi <= 28 :
                lower28[i] = True
                buy(coinlist[i])
                
            elif now_rsi <= 20 and lower28[i] == True :
                buy(coinlist[i])
                
            elif cur_price >= profit_price and av_buy > 0 :
                sell(coinlist[i])                
                                
            elif now_rsi >= 60 :
                lower28[i] = False
                
            time.sleep(0.1)
            
        except Exception as e:
            print(e)
            time.sleep(0.1)  
