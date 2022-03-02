from django.core.management.base import BaseCommand, CommandError
import yfinance as yf
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snp600.settings')
django.setup()

from datetime import date
from main.models import Record, Stock, Person
from csv import reader
from django.core.mail import send_mail
from django.conf import settings

# import stock tickers(array) from main/tickers.py
from main.tickers import TICKERS


class Command(BaseCommand):
    def handle(self, *args, **options):
        
        # 1. download file from yfinance
        def download_csv():
            # tickers of target company 
            tickers = TICKERS

            # set variables for correct file directory
            file_dir = os.path.dirname(os.path.abspath(__file__))
            csv_folder = 'main/data/'

            # make calls to download each ticker record
            for i in range(len(tickers)):
                data = yf.download(tickers[i], start='2021-12-01', end=date.today())
                file_name= tickers[i]+".csv"
                file_path=os.path.join(file_dir, csv_folder, file_name)
                data.to_csv(file_path,index=True)

        # 2. check and create Stock models if deosn't exist
        def create_stock_models():
            for ticker in TICKERS:
                try:
                    object = Stock.objects.get(ticker=ticker)
                except Stock.DoesNotExist:
                    object = Stock(ticker=ticker)
                    object.save()

        # 3. populate Record models
        def update_model():
            for filename in os.listdir("main/management/commands/main/data/"):
                file_path = "main/management/commands/main/data/" + filename
                with open(file_path,"r",encoding='windows-1252') as f:
                    # removing NUL character
                    file_reader = reader((line.replace('\0','') for line in f))
                    #skipping first row(Date,Open,High,Low,Close,Adj Close,Volume)
                    next(file_reader)
                    for row in file_reader: 
                        # skip the row if there's an empty cell
                        if len(row[1]) <1 or len(row[2]) <1 or len(row[3]) <1 or len(row[4]) <1 or len(row[6]) <1:
                            pass
                        else:
                            # converting volume metric to avoid x.0 situation
                            new_record = Record(ticker=filename[:-4],date=row[0],open=row[1],high=row[2],low=row[3],close=row[4],volume=int(float(row[6])),stock=Stock.objects.get(ticker=filename[:-4]))
                            
                            #check date and ticker to avoid duplicates
                            if not Record.objects.filter(ticker=new_record.ticker).filter(date=new_record.date):
                                new_record.save()

        # TODO finish function
        # 4. query hgih volatility stocks and send out email
        # send out email / query high volatility stocks functions written in models
        def high_volatility_notif():
            # get sorted ticker/price change dict from models
            test = Record.objects.filter(ticker='AAPL')[0].sorted_high_valotility_dict()
            for key, value in list(test.items()):
                Stock.objects.get(ticker=key).email_notification()
            return print(list(test.items()))

        download_csv()
        create_stock_models()
        update_model()
        high_volatility_notif()