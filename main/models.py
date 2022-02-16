from django.db import models
from datetime import timedelta, date

# Create your models here.

class Record(models.Model):
    ticker = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    open = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    high = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    low = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    close = models.DecimalField(max_digits=10, decimal_places=5,null=True,blank=True)
    volume = models.IntegerField(null=True,blank=True)

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

    # find the latest record date by looping from today up to 19 days ago
    @property
    def latest_record_date(self):
        for i in range(0,20):
            if len(Record.objects.filter(ticker=self.ticker).filter(date=date.today()-timedelta(i))) != 0:
                latest_record_date = date.today()-timedelta(i)
                break
        return latest_record_date
    
    # not the last_30_trading/closeprice returns list of 30 elements in DESC order
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

        

