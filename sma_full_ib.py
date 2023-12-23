import random
import time
import datetime
from ib_insync import *
import pandas_ta as ta
import pandas as pd
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=10)


tickers=['BTC','ETH']
capital=100


ticker_contracts={}
for tick in tickers:
    ticker_contracts[tick]=Crypto(tick,'PAXOS','USD')



def stockprice(temp):
    a=ib.reqMktData(temp)
    util.sleep(1)
    price=a.last
    ib.cancelMktData(temp)
    return price


def get_historical_data(ticker_contract):
    bars = ib.reqHistoricalData(
    ticker_contract, endDateTime='', durationStr='1 D',
    barSizeSetting='1 min', whatToShow='AGGTRADES', useRTH=True)
    # convert to pandas dataframe:
    df = util.df(bars)
    print(df)
    df['sma1']=ta.sma(df.close,10)
    df['sma2']=ta.sma(df.close,20)

    
    return df


def trade_buy_stocks(stock_name,stock_price):
    #market order
    contract = ticker_contracts[stock_name]
    contract=ib.qualifyContracts(contract)[0]
    ord=MarketOrder(action='BUY',totalQuantity=1)
    trade=ib.placeOrder(contract,ord)
    ib.sleep(1)
    print(trade)

    #stop loss order
    ord=StopOrder(action='SELL',totalQuantity=1,stopPrice=int(0.90*stock_price))
    trade=ib.placeOrder(contract,ord)
    ib.sleep(1)
    print(trade)
    

def trade_sell_stocks(stock_name,stock_price):
    #market order
    contract = ticker_contracts[stock_name]
    contract=ib.qualifyContracts(contract)[0]
    ord=MarketOrder(action='SELL',totalQuantity=1)
    trade=ib.placeOrder(contract,ord)
    ib.sleep(1)
    print(trade)

    #stop loss order
    ord=StopOrder(action='BUY',totalQuantity=1,stopPrice=int(1.10*stock_price))
    trade=ib.placeOrder(contract,ord)
    ib.sleep(1)
    print(trade)

            
def trail_buy_stock(pos_df,ord_df,ticker,open_trade):

    print('inside trail')
    
    #buy price
    pos_df['name']=[i.symbol for i in pos_df.contract ]
    buy_price=pos_df[pos_df.name==ticker].avgCost.iloc[0]
    buy_price

    #last price
    cont=pos_df[pos_df.name==ticker].contract.iloc[0]
    last_price=stockprice(cont)
    print(last_price)

    #stop order price and order object
    
    
    open_trade['price']=[i.auxPrice for i in  open_trade.order]
    t_s=open_trade[open_trade.name==ticker].price.iloc[-1]
    print(ticker)
    print(t_s)
    stop_order_id=open_trade[open_trade.name==ticker].order.iloc[-1]

    #modify order
    trail_condition=last_price>(2*(buy_price/10))+t_s

    if trail_condition:
        print('modify order')
        new_t_s=round(t_s+(buy_price/10),1)
        print('new stop limit is',new_t_s)
        ib.cancelOrder(stop_order_id)

        contract = ticker_contracts[ticker]
        contract=ib.qualifyContracts(contract)[0]
        ord=StopOrder(action='SELL',totalQuantity=1,stopPrice=new_t_s)
        trade=ib.placeOrder(contract,ord)
        ib.sleep(1)
        print(trade)
    else:
        print('trailing condition not met')


def trail_sell_stock(pos_df,ord_df,ticker,open_trade):


    print('inside trail')
    
    #buy price
    pos_df['name']=[i.symbol for i in pos_df.contract ]
    buy_price=pos_df[pos_df.name==ticker].avgCost.iloc[0]
    buy_price

    #last price
    cont=pos_df[pos_df.name==ticker].contract.iloc[0]
    last_price=stockprice(cont)
    print(last_price)

    #stop order price and order object
    open_trade['price']=[i.auxPrice for i in  open_trade.order]
    t_s=open_trade[open_trade.name==ticker].price.iloc[-1]
    print(ticker)
    print(t_s)
    stop_order_id=open_trade[open_trade.name==ticker].order.iloc[-1]
    
    #modify order
    if last_price<+t_s-(2*(buy_price/10)):
        print('modify order')
        new_t_s=round(t_s-(buy_price/10),1)
        print('new stop order',new_t_s)
        
        ib.cancelOrder(stop_order_id)

        contract = ticker_contracts[ticker]
        contract=ib.qualifyContracts(contract)[0]
        ord=StopOrder(action='BUY',totalQuantity=1,stopPrice=new_t_s)
        trade=ib.placeOrder(contract,ord)
        ib.sleep(1)
        print(trade)
    else:
        print('trailing condition not met')


def strategy(data,ticker):
    print('inside strategy')
    print(ticker)
    print(data)
    
    # buy_condition=data['sma1'].iloc[-1]>data['sma2'].iloc[-1] and data['sma1'].iloc[-2]<data['sma2'].iloc[-2]
    buy_condition=data['sma1'].iloc[-1]>data['close'].iloc[-1]
    sell_condition=data['sma1'].iloc[-1]<data['sma2'].iloc[-1] and data['sma1'].iloc[-2]>data['sma2'].iloc[-2]
    current_balance=int(float([v for v in ib.accountValues() if v.tag == 'AvailableFunds' ][0].value))
    if current_balance>data.close.iloc[-1]:
        if buy_condition:
            print('buy condiiton satisfied')
            trade_buy_stocks(ticker,data.close.iloc[-1])
        elif sell_condition:
            print('sell condition satisfied')
            trade_sell_stocks(ticker,data.close.iloc[-1])
        else :
            print('no condition satisfied')
    else:
        print('we dont have enough money')
        print('current balance is',current_balance,'stock price is ',data.close[-1])


def main():
    ord_df=util.df(ib.reqOpenOrders())
    pos_df=util.df(ib.reqPositions())
    if pos_df is not None:
        pos_df['name']=[i.symbol for i in pos_df.contract ]
    else:
            pos_df=pd.DataFrame()
            pos_df['name']=0    
 
        
        
    print(pos_df)
    open_order_df=util.df(ib.openTrades())
    print(open_order_df)

    for ticker in tickers:
        print('ticker name is',ticker,'################')
        ticker_contract=ticker_contracts[ticker]
        ticker_contract=ib.qualifyContracts(ticker_contract)[0]
        hist_df=get_historical_data(ticker_contract)
        print(hist_df)
        print(hist_df.close.iloc[-1])
        capital=int(float([v for v in ib.accountValues() if v.tag == 'AvailableFunds' ][0].value))
        print(capital)
        quantity=int(capital/hist_df.close.iloc[-1])
        
        print(quantity)
        if quantity==0:
            print('we dont have enough money so we cannot trade')
            continue

        if pos_df.empty:
            print('we dont have any position')
            strategy(hist_df,ticker)


        elif len(pos_df)!=0 and ticker not in pos_df['name'].tolist():
            print('we have some position but current ticker is not in position')
            strategy(hist_df,ticker)
        elif len(pos_df)!=0 and ticker in pos_df["name"].tolist():
            print('we have some position and current ticker is in position')
            print(open_order_df)
            if pos_df[pos_df["name"]==ticker]["position"].values[0] == 0:
                print('we have current ticker in position but quantity is 0')
                strategy(hist_df,ticker)

            elif pos_df[pos_df["name"]==ticker]["position"].values[0] > 0  :
                print('we have current ticker in position and is long')
                if ord_df is not None:
                    open_order_df['name']=[i.symbol for i in  open_order_df.contract]
                    if ticker in open_order_df['name'].to_list():
                        trail_buy_stock(pos_df,ord_df,ticker,open_order_df)

            elif pos_df[pos_df["name"]==ticker]["position"].values[0] < 0 :
                print('we have current ticker in position and is short')
                if ord_df is not None:
                    open_order_df['name']=[i.symbol for i in  open_order_df.contract]
                    if ticker in open_order_df['name'].to_list():
                        trail_sell_stock(pos_df,ord_df,ticker,open_order_df)
            else:
                print('trail condition not met')

current_time=datetime.datetime.now()
print(current_time)

print(datetime.datetime.now())

#start time
start_hour,start_min=9,30
#end time
end_hour,end_min=23,30
start_time=datetime.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min)
end_time=datetime.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min)
print(start_time)
print(end_time)

while True:
    if datetime.datetime.now()>start_time:
        break
    print(datetime.datetime.now())


candle_size=60

while datetime.now()<end_time:
    now = datetime.now()
    seconds_until_next_minute = candle_size - now.second+1

    # Sleep until the end of the current minute
    time.sleep(seconds_until_next_minute)

    # Run your function
    main()
