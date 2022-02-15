# script functions
# 1. call yfinance api to update the csvs in /main/data
# 2. populate Record classes in django
# -----
import os
import django
import yfinance as yf
# import pandas as pd (not sure if it's needed)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snp600.settings')
django.setup()

from datetime import date
from main.models import Record
from csv import reader

# import stock tickers(array) from main/tickers.py
from main.tickers import TICKERS


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


# 2. populate Record classes
def update_model():
    for filename in os.listdir("main/data"):
        file_path = "main/data/" + filename
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
                    new_record = Record(ticker=filename[:-4],date=row[0],open=row[1],high=row[2],low=row[3],close=row[4],volume=int(float(row[6])))
                    
                    #check date and ticker to avoid duplicates
                    if not Record.objects.filter(ticker=new_record.ticker).filter(date=new_record.date):
                        new_record.save()

# ---
# call functions
download_csv()
update_model()
