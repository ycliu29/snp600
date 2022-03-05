from genericpath import exists
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
import json
from .models import Record, Person, Stock
from django.core.mail import send_mail
from django.conf import settings

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        elif user is None:
            return render(request, 'main/login.html',{
                'error_message': "Invalid username or password, please try again."
            })
    elif request.method == "GET":
        return render(request, 'main/login.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    if not request.user.is_authenticated:
        return render(request, 'main/login.html',{
                'error_message': "Login first to use this function."
            })

def create_account(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        email = request.POST['email']
        if password == password_confirmation and username and password and password_confirmation and email:
            u,created = User.objects.get_or_create(username=username, email=email)
            if created:
                u.set_password(password)
                u.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('index')
        else:
            return render(request, 'main/create_account.html',{
                'error_message': "Invalid credentials, please try again."
            })
    elif request.method == "GET":
        if request.user.is_authenticated:
           return redirect('index')
        elif not request.user.is_authenticated:
            return render(request, 'main/create_account.html')

# returning 3 dictionaries to template | top growth/decline/volume | plus latest record date
def index(request):
    # calling methods to get full dictionaries
    latest_record_date = Record.objects.get(ticker='AAPL',date="2022-02-01").latest_record_date
    top_growth_dict = Record.objects.get(ticker='AAPL',date="2022-02-01").sorted_price_change_dict(10)
    most_decline_dict = Record.objects.get(ticker='AAPL',date="2022-02-01").sorted_price_change_dict(-10)
    most_traded_dict = Record.objects.get(ticker='AAPL',date="2022-02-01").sorted_volume_dict(10)

    return render(request, 'main/index.html',{
        'top_growth_dict': top_growth_dict,
        'most_decline_dict': most_decline_dict,
        'most_traded_dict': most_traded_dict,
        'latest_record_date': latest_record_date
    })

# handle individual stock page
def detailed_view(request, ticker):
    return_list = Record.objects.filter(ticker=ticker)[0].last7d_records
    last_30_trading_dates = Record.objects.filter(ticker=ticker)[0].last_30_trading_dates
    last_30_close_price = Record.objects.filter(ticker=ticker)[0].last_30_close_price
    try:
        if_stock_in_watchlist = Person.objects.get(username=request.user.username).stock_in_watchlist(request.user.username, ticker)
    except Person.DoesNotExist:
        if_stock_in_watchlist = ""
    try: 
        if_stock_in_notification_list = Person.objects.get(username=request.user.username).stock_in_notification_list(request.user.username, ticker)
    except Person.DoesNotExist:
        if_stock_in_notification_list = ""
    return render(request,'main/ticker.html',{
        'ticker': ticker,
        'return_list': return_list,
        # reverse the list as the lists were start generated from the latest dates
        'last_30_trading_dates': last_30_trading_dates[::-1],
        "last_30_close_price": last_30_close_price[::-1],
        "if_stock_in_watchlist": if_stock_in_watchlist,
        "if_stock_in_notification_list": if_stock_in_notification_list
    })

@login_required
def following(request):
    username = request.user.username
    person = Person.objects.get(username=username)
    following_stocks = person.sorted_following_stocks(username)
    notification_stocks = person.sorted_notification_stocks(username)
    latest_record_date = Record.objects.filter(ticker='AAPL')[0].latest_record_date
    # test = Record.objects.filter(ticker='AAPL')[0].sorted_high_valotility_dict()
    
    return render(request, 'main/following.html',{
        'following_stocks': following_stocks,
        'notification_stocks': notification_stocks,
        'latest_record_date': latest_record_date,
        # 'test': test
    })

# api routes
@login_required
def update_follow(request): 
    if request.method == "POST":
        data = json.loads(request.body)
        user = data['user']
        ticker = data['ticker']
        person_model = Person.objects.get(username=user)
        stock_model = Stock.objects.get(ticker = ticker)

        if Person.objects.filter(username=user).filter(watchlist=stock_model).exists():
            person_model.watchlist.remove(stock_model)
            stock_model.in_watchlist.remove(person_model)
            response = 'removed'
            return JsonResponse(response, safe=False)
        elif not Person.objects.filter(username=user).filter(watchlist=stock_model).exists():
            person_model.watchlist.add(stock_model)
            stock_model.in_watchlist.add(person_model)
            response = 'added'
            return JsonResponse(response, safe=False)
    else:
        return JsonResponse('Incorrect user flow, please return to mainpage', safe=False)

@login_required
def update_notification_list(request): 
    if request.method == "POST":
        data = json.loads(request.body)
        user = data['user']
        ticker = data['ticker']
        person_model = Person.objects.get(username=user)
        stock_model = Stock.objects.get(ticker = ticker)

        if Person.objects.filter(username=user).filter(notification_list=stock_model).exists():
            person_model.notification_list.remove(stock_model)
            stock_model.in_notification_list.remove(person_model)
            response = 'removed'
            return JsonResponse(response, safe=False)
        elif not Person.objects.filter(username=user).filter(notification_list=stock_model).exists():
            person_model.notification_list.add(stock_model)
            stock_model.in_notification_list.add(person_model)
            response = 'added'
            return JsonResponse(response, safe=False)
    else:
        return JsonResponse('Incorrect user flow, please return to mainpage', safe=False)

@login_required
def test_notification(request):
    if request.method== "POST":
        data = json.loads(request.body)
        user = data['user']
        ticker = data['ticker']
        latest_record_date = Record.objects.filter(ticker='AAPL')[0].latest_record_date
        price_change = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change
        mail_title = ticker + ' volatility notification(test)'
        mail_content = 'THIS IS A TEST EMAIL. ' + ticker + '\'s colsed price changed ' + str(round(price_change * 100,2))+'% in the last trading day, we\'re informing you with this email(from S&P500 Tracker).'
        receipient_list = []
        receipient_list.append(Person.objects.get(username=user).email)
        send_mail(
            mail_title,
            mail_content,
            settings.EMAIL_HOST_USER,
            receipient_list
        )
        return JsonResponse('email sent', safe=False)



        
    

    