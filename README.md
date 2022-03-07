## S&P500 資訊網 ##

此專案透過 [yfinance](https://pypi.org/project/yfinance/) 套件存取 Yahoo Finance 的股市交易資料，涵蓋組成 S&P500 指數的 505 檔標的，主要功能包括：
1. 首頁，前一交易日前十交易量、漲和跌幅標的
2. 個股頁面，使用 [chart.JS](https://www.chartjs.org/) 產出前三十交易日成交價折線圖及前七交易日詳細資訊表格
3. 用戶註冊、登出、登入功能
4. 用戶可選擇追蹤(follow)或取得個股通知(notification)，若標的成交價與前一交易日差距超過 5%，系統將發送通知信件
5. 追蹤(following)頁面，顯示用戶追蹤終及開啟通知之標的列表
6. 自訂資料更新指令(data_update)，透過排程工具（如 [Heroku Scheduler](https://elements.heroku.com/addons/scheduler)），可自動更新資料及網站

### Demo ###
SNP500 Tracker: https://ycl-snp500.herokuapp.com/

測試帳號: baz
測試密碼: baz

或是使用註冊功能建立新帳號

### 使用技術 ### 
- Django 後端框架
- 原生 HTML+CSS 完成 RWD 網頁
- 專案部署於 Heroku

### 功能介紹 ### 

### 專案架構 ### 
(only listing major files)
```
SNP600(project folder)   
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
```
