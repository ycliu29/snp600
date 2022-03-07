# S&P500 資訊網 #

此專案透過 [yfinance](https://pypi.org/project/yfinance/) 套件存取 Yahoo Finance 的股市交易資料，涵蓋組成 S&P500 指數的 505 檔標的，主要功能包括：
1. 首頁，顯示前一交易日前十交易量、漲和跌幅標的和個別漲跌幅、交易量
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
#### 首頁瀏覽 ####
- 顯示前一交易日前十交易量、漲和跌幅標的和個別漲跌幅、交易量

![Screen Shot 2022-03-07 at 8 13 15 PM](https://user-images.githubusercontent.com/81467494/157032433-ab0d73ad-f250-4bbc-9523-3eceb161e761.png)

#### 個股瀏覽 ####
- 顯示前三十交易日成交價折線圖及前七交易日詳細資訊表格
- 登入用戶可選擇追蹤股票及開啟通知

![Screen Shot 2022-03-07 at 8 06 24 PM](https://user-images.githubusercontent.com/81467494/157031855-a4cae4fd-a3b3-46ca-bcec-7bb2172b53df.png)

#### 追蹤頁面 ####
- 用戶可看到追蹤中及已開啟通知的標的

![Screen Shot 2022-03-07 at 8 07 56 PM](https://user-images.githubusercontent.com/81467494/157031968-dea39fe7-0f9f-4d9e-ac59-ea2f011e926c.png)

#### 帳號管理 ####
- 用戶可以註冊、登入、登出網站

![Screen Shot 2022-03-07 at 8 10 31 PM](https://user-images.githubusercontent.com/81467494/157032038-09073a18-4e4d-4d3a-b582-3c2d19c67b17.png)
![Screen Shot 2022-03-07 at 8 10 37 PM](https://user-images.githubusercontent.com/81467494/157032052-d3fb4e24-f7a3-4fdc-9fef-dcd3ca086043.png)

### 專案架構 ### 
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
