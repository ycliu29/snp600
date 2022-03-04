##About##

SNP500 Tracker is a web app that trakcs and update daily changes of the S&P500 component stocks. 
The tracker displays 10 highest growth, decline and most traded stocks of the day. User can choose to follow stocks or turn on notification to receive email notif of drastic(>5%) price changes.

How to use
After setting up env. variables (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS) this site should run fine in local or host server.
Running 'python manage.py data_update' at project folder should update db with the latest data.

Directories(only listing major files)
SNP600(project folder)├──│└──
├──main(web app)
│   ├──management/commands
│   │   ├──data_update.py(custom command)
│   │   └──main/data(storing .csv files from Yahoo Finance)
│   ├──migrations
│   ├──static(JS, css files)
│   ├──templates/main(HTML pages and template)
│   ├──templatetags
│   ├──models.py/main_extras(custome templatetag to display percentage changes)
│   ├──tickers.py(list of stocks to store and maintain)
│   ├──urls.py
│   ├──models.py(models and methods of most data logic)
│   └──views.py(calling model methods and feed data to templates)
├──SNP600(settings)
├──static(packaged JS, CSS file for servering static files at the same server via whitenoise)
├──requirements.txt
└──Procfile, runtime.txt(files for Heroku deployment)

Distinctiveness and Complexity
Data processing. The rough data handling looks like this:
1. Using yflinance(https://pypi.org/project/yfinance/), I'm able to access daily data of stocks in .csv file, I then need to save, read and extract the correct data to populate (Record)models.
2. Create model methods to sort ticker/price change dictionary, which involves data structure manipulation(dictionary->list->dictionary). For easier usage and rendering in view and template.

Javascript
1. Utilising JS to render daily price/date chart with chart.JS(https://www.chartjs.org/)
2. Making AJAX calls to update user's Person(model) notification/following field and changes element HTML with it. 

Others
1. Create custom command 'main/management/commands/data_update.py to automoate data download, check Stock models, update Record and send out notification. Using scheduler add on with Herokt deplyment, the site is able to auto update itself.
2. Deployment at Heroku(https://ycl-snp500.herokuapp.com/). 

Functions
Data
1. data download 
2. check Stock models
3. create Record models
4. send out notification

User
1. Register 
2. Login / Out
3. Follow / Unfollow / Get notified / Cancel notification
4. Test notification

Display
1. RWD
