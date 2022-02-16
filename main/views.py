from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Record
from .tickers import TICKERS

# returning 2 dictionaries to template
# 1: price change percetage | 2: trade volume 
def index(request):
    # 1. create a sorted price_change_percentage dictionary
    price_change_dict = {}
    latest_record_date = Record.objects.filter(ticker='AAPL').filter(date='2022-01-27')[0].latest_record_date
    for ticker in TICKERS:
        # if == 0 is triggered, need to look into specail events(might be index change)
        if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date)) == 0:
            print("error: " + ticker)
        if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
            price_change_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change
    sorted_price_change_dict = dict(sorted(price_change_dict.items(),key=lambda item:item[1],reverse=True))
    #---
    # 2. create a sorted trade_volume dictionary(descending order)
    volume_dict = {}
    for ticker in TICKERS:
        if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
            volume_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].volume
    sorted_volume_dict = dict(sorted(volume_dict.items(),key=lambda item:item[1],reverse=True))

    # 3. pre-process returning items (top10 increase, top 10 decrease, 10 most traded)
    l = list(sorted_price_change_dict.items())
    top_growth_dict = {}
    for i in range(10):
        top_growth_dict[l[i][0]] = l[i][1] 
    
    most_decline_dict = {}
    # use len to catch if there's less than 505 stocks
    for i in range(len(sorted_volume_dict)-10,len(sorted_volume_dict)):
        most_decline_dict[l[i][0]] = l[i][1]
    
    most_traded_dict = {}
    for i in range(10):
        most_traded_dict[list(sorted_volume_dict.items())[i][0]] = list(sorted_volume_dict.items())[i][1]

    return render(request, 'main/index.html',{
        'top_growth_dict': top_growth_dict,
        'most_decline_dict': most_decline_dict,
        'most_traded_dict': most_traded_dict,
        'latest_record_date': latest_record_date
    })

def detailed_view(request, ticker):

    return_list = Record.objects.filter(ticker=ticker)[0].last7d_records
    last_30_trading_dates = Record.objects.filter(ticker=ticker)[0].last_30_trading_dates
    last_30_close_price = Record.objects.filter(ticker=ticker)[0].last_30_close_price
    return render(request,'main/ticker.html',{
        'ticker': ticker,
        'return_list': return_list,
        'last_30_trading_dates': last_30_trading_dates[::-1],
        "last_30_close_price": last_30_close_price[::-1]
    })