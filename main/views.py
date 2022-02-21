from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Record

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