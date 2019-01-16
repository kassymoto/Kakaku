# -*- coding: utf-8 -*-
"""kakaku_com.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WyPpwvClssS_3e_lf5t7P5gaIiEZAkLm
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Kakaku:
  url = ""
  price = []
  date = []
  title = ""

# define urls
url = []
url.append(requests.get("http://kakaku.com/item/K0001014634/pricehistory/"))
url.append(requests.get("http://kakaku.com/item/K0001095746/pricehistory/"))
url.append(requests.get("http://kakaku.com/item/K0001095680/pricehistory/"))
url.append(requests.get("http://kakaku.com/item/K0001095676/pricehistory/"))
url.append(requests.get("http://kakaku.com/item/K0001019734/pricehistory/"))

# define class of kakaku num of urls
kakaku_list = []
for i in url:
  kakaku_tmp = Kakaku()
  kakaku_tmp.url = i
  kakaku_list.append(kakaku_tmp)
  
for kakaku in kakaku_list:
    soup = BeautifulSoup(kakaku.url.content, "html.parser")
    
    date = soup.find_all("td", class_="alignL")
    price = soup.find_all("td", class_="alignR itemviewColor06")
    
    title = soup.find("title").string.split(" ")[2:-1:]
    kakaku.title = str(" ".join(title))
    
    date_tmp = []
    price_tmp = []
    
    for i,j in zip(date[0::2],price):
        if(str(i.string)=="現在"):
            date_tmp.append(datetime.now().strftime('%Y-%m-%d'))
        else:
            date_tmp.append("".join(str(i.string).split(" ")[:-1:]).replace("年","-").replace("月","-").replace("日",""))
        price_tmp.append(int(str(j.string[1::]).replace(',','')))
    
    kakaku.date = date_tmp
    kakaku.price = price_tmp
    
"""
for i in kakaku_list:
    print(i.title)
    for j,k in zip(i.date,i.price):
        print(j,k)
    print()
    
"""
import pandas as pd
kakaku_Title = []
kakaku_Date = []
kakaku_Price = []

for i in kakaku_list:
    for j in range(len(i.date)):
        kakaku_Title.append(i.title)
    kakaku_Date += i.date
    kakaku_Price += i.price

kakaku_data = pd.DataFrame(
        {"Title":kakaku_Title,
         "Date":kakaku_Date,
         "Price":kakaku_Price})




import altair as alt

alt.Chart(kakaku_data, height=500 ,width=700).configure_legend(labelLimit=0).mark_line().encode(
        x="Date:T",
        y="Price:Q",
        color="Title:N"
        )



