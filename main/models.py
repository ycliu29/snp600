from django.db import models
from datetime import timedelta, date
from django.contrib.auth.models import User
from .tickers import TICKERS
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10, null=True, blank=True)
    in_watchlist = models.ManyToManyField('Person',related_name='in_watchlist',blank=True)
    in_notification_list = models.ManyToManyField('Person',related_name='in_notification_list',blank=True)

    def __str__(self):
        return self.ticker

    # send volatility email notif to Person in notification field
    def email_notification(self):
        notif_list = self.in_notification_list
        # check if there's any r/s in the field
        if notif_list.exists():
            latest_record_date = Record.objects.filter(ticker='AAPL')[0].latest_record_date
            price_change = Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date)[0].daily_change
            mail_title = self.ticker + ' volatility notification'
            mail_content = self.ticker + '\'s colsed price changed ' + str(round(price_change * 100,2))+'% in the last trading day, we\'re informing you with this email(from S&P500 Tracker).'
            person_list = self.in_notification_list.all()
            receipient_list =[]
            for person in person_list: 
                receipient_list.append(person.email)
            send_mail(
                mail_title,
                mail_content,
                settings.EMAIL_HOST_USER,
                receipient_list
            )
        else:
            pass
                           
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    watchlist = models.ManyToManyField(Stock,related_name='watchlist', blank=True)
    notification_list= models.ManyToManyField(Stock,related_name='notification', blank=True)

    def __str__(self):
        string = self.username + "(Person)"
        return string

    def sorted_following_stocks(request, username):
        price_change_dict = {}
        latest_record_date = Record.objects.filter(ticker='AAPL')[0].latest_record_date
        person = Person.objects.get(username=username)
        for ticker in person.watchlist.all():
            # if == 0 is triggered, need to look into specail events(might be index change)
            if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date)) == 0:
                print("error: " + ticker)
            elif len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
                price_change_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change
        sorted_price_change_dict = dict(sorted(price_change_dict.items(),key=lambda item:item[1],reverse=True))
        return sorted_price_change_dict

    def sorted_notification_stocks(request, username):
        price_change_dict = {}
        latest_record_date = Record.objects.filter(ticker='AAPL')[0].latest_record_date
        person = Person.objects.get(username=username)
        for ticker in person.notification_list.all():
            # if == 0 is triggered, need to look into specail events(might be index change)
            if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date)) == 0:
                print("error: " + ticker + latest_record_date + " data missing")
            elif len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
                price_change_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change
        sorted_notification_stocks = dict(sorted(price_change_dict.items(),key=lambda item:item[1],reverse=True))
        return sorted_notification_stocks

    # pass in username and ticker to check if the stock(ticker) is in this person's watchlist
    def stock_in_watchlist(self, username, ticker):
        stock_obj = Stock.objects.get(ticker=ticker)
        person = Person.objects.filter(username=username)
        if person.filter(watchlist=stock_obj).exists():
            return True
        elif not person.filter(watchlist=stock_obj).exists():
            return False

    def stock_in_notification_list(self, username, ticker):
        stock_obj = Stock.objects.get(ticker=ticker)
        person = Person.objects.filter(username=username)
        if person.filter(notification_list=stock_obj).exists():
            return True
        elif not person.filter(notification_list=stock_obj).exists():
            return False

class Record(models.Model):
    ticker = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    open = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    high = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    low = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    close = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    volume = models.IntegerField(null=True,blank=True)
    stock = models.ForeignKey(Stock,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # stringify datetime to print
        self_string = self.ticker + " " + self.date.strftime("%m/%d/%Y")
        # self_string = self.ticker
        return self_string
    
    # return daily stock price change(comparing to the last trading day)
    @property
    def daily_change(self):
        
        price_today = self.close

        # try querysets to find the previous trading day record(could be 1 to x days before), trying up to 19 days ago
        stock_queryset = Record.objects.filter(ticker=self.ticker)
        for i in range(1, 20):
            if len(stock_queryset.filter(date=self.date-timedelta(i))) != 0:
            # if such record exists
                price_ytd = stock_queryset.filter(date=self.date-timedelta(i))[0].close
                break
        
        # calculate changes and rounding the number for easier display
        price_change = (price_today-price_ytd)/price_ytd
        price_change = round(price_change,5)
        return price_change

    # return a return_items # of sorted(DESC) price change dict of all stocks in TICKERS of the latest trading day(arg can be negative to start access the last item)
    def sorted_price_change_dict(self, return_items):
        price_change_dict = {}
        latest_record_date = self.latest_record_date
        for ticker in TICKERS:
            # if == 0 is triggered, need to look into specail events(might be index change)
            if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date)) == 0:
                print("error: " + ticker)
            elif len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
                price_change_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change
        sorted_price_change_dict = dict(sorted(price_change_dict.items(),key=lambda item:item[1],reverse=True))
        l = list(sorted_price_change_dict.items())

        return_dict = {}
        if return_items > 0:
            for i in range(return_items):
                return_dict[l[i][0]] = l[i][1]
        elif return_items < 0:
            for i in range(len(l)-1,len(l)+return_items-1,-1):
                return_dict[l[i][0]] = l[i][1]
        return return_dict
    
    # return a return_items # of sorted(DESC) volume dict of all stocks in TICKERS of the latest trading day
    def sorted_volume_dict(self, return_items):
        volume_dict = {}
        latest_record_date = self.latest_record_date
        for ticker in TICKERS:
            if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
                volume_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].volume
        sorted_volume_dict = dict(sorted(volume_dict.items(),key=lambda item:item[1],reverse=True))
        
        return_dict = {}
        for i in range(return_items):
            return_dict[list(sorted_volume_dict.items())[i][0]] = list(sorted_volume_dict.items())[i][1]
        return return_dict

    # return a sorted dict of stocks that fluctuates more than 5%(of closing price).
    def sorted_high_valotility_dict(self):
        high_volatility_dict = {}
        latest_record_date = self.latest_record_date
        for ticker in TICKERS:
            # if == 0 is triggered, need to look into specail events(might be index change)
            if len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date)) == 0:
                print("error: " + ticker)
            elif len(Record.objects.filter(ticker=ticker).filter(date=latest_record_date))>0:
                if Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change >= 0.05 or Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change <= (-0.05):
                    high_volatility_dict[ticker] = Record.objects.filter(ticker=ticker).filter(date=latest_record_date)[0].daily_change
                else:
                    pass
        sorted_high_volatility_dict = dict(sorted(high_volatility_dict.items(),key=lambda item:item[1],reverse=True))
        l = list(sorted_high_volatility_dict.items())

        return_dict = {}
        for i in range(len(l)):
            return_dict[l[i][0]] = l[i][1]
        return return_dict

    # find the latest record date by looping from today up to 19 days ago
    @property
    def latest_record_date(self):
        for i in range(0,20):
            if len(Record.objects.filter(ticker=self.ticker).filter(date=date.today()-timedelta(i))) != 0:
                latest_record_date = date.today()-timedelta(i)
                break
        return latest_record_date
    
    # note the last_30_trading/closeprice returns lists of 30 elements in DESC order
    @property
    def last_30_trading_dates(self):
        return_list = []
        count = 0
        latest_record_date = self.latest_record_date
        for i in range(0,100):
            if len(Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date-timedelta(i))) > 0:
                return_list.append(Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date-timedelta(i))[0].date)
                count += 1
                if count >= 30:
                    break
        return return_list
    
    @property
    def last_30_close_price(self):
        return_list = []
        count = 0
        latest_record_date = self.latest_record_date
        for i in range(0,100):
            if len(Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date-timedelta(i))) > 0:
                return_list.append(Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date-timedelta(i))[0].close)
                count += 1
                if count >= 30:
                    break
        return return_list

    # return a list of record objects of the last 7 trading days(trace up to 49 calendar days ago)
    @property
    def last7d_records(self):
        return_list = []
        record_count = 0
        latest_record_date = self.latest_record_date
        for i in range(50):
            if len(Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date-timedelta(i))) == 0:
                pass
            else:
                # use .values() method to convert object fields into dictionaries for easier iteration
                return_list.append(Record.objects.filter(ticker=self.ticker).filter(date=latest_record_date-timedelta(i))[0])
                record_count += 1
                if record_count == 7:
                    break
        return return_list

# ---------------
# signal handling
# ---------------
# create Person object when User is created
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        object = Person(user=instance,username=instance.username,email=instance.email)
        object.save()

