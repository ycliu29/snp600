from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Record

# returning 3 dictionaries to template | top growth/decline/volume | plus latest record date
def index(request):
    # calling methods to get full dictionaries
    latest_record_date = Record.objects.filter(ticker='AAPL')[0].latest_record_date
    top_growth_dict = Record.objects.filter(ticker='AAPL')[0].sorted_price_change_dict(10)
    most_decline_dict = Record.objects.filter(ticker='AAPL')[0].sorted_price_change_dict(-10)
    most_traded_dict = Record.objects.filter(ticker='AAPL')[0].sorted_volume_dict(10)

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
        # reverse the list as the lists were start generated from the latest dates
        'last_30_trading_dates': last_30_trading_dates[::-1],
        "last_30_close_price": last_30_close_price[::-1]
    })