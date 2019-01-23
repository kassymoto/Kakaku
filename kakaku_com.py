# -*- coding: utf-8 -*-
"""kakaku_com.ipynb
価格コムの商品（URL指定）をスクレイピングし、
各商品の直近の価格変動をプロットする
"""

# ライブラリのインポート
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass, field
from typing import List

# 商品のデータをまとめたクラス
@dataclass
class Kakaku:
    product_url : str = None  # 商品のURL
    product_title : str = None  # 商品名
    product_price : List[int] = field(default_factory=list)  # 商品の価格
    product_date : List[str] = field(default_factory=list)  # 商品の価格が変動した日付

    @classmethod
    def import_from_url(cls, url):
        product_url = url  # URL設定
        soup = BeautifulSoup(requests.get(product_url).content, "html.parser")  # スクレイピング先を指定

        source_date = soup.find_all("td", class_="alignL")  # 日付情報をスクレイピング
        source_price = soup.find_all("td", class_="alignR itemviewColor06")  # 値段情報をスクレイピング
        product_title = str(" ".join(soup.find("title").string.split(" ")[2:-1:]))  # 商品名を設定

        # 取得したデータの体裁を整えつつ、価格、日付を登録していく。
        product_date = []
        product_price = []

        for date, price in zip(source_date[0::2], source_price):
            if(str(date.string)=="現在"):  # 最新のものは日付ではなく現在と表記されている。
                product_date.append(datetime.now().strftime('%Y-%m-%d'))  # 日付形式に直して登録する

            else:
                product_date.append("".join(str(date.string).split(" ")[:-1:]).replace("年","-").replace("月","-").replace("日",""))  # 体裁を整えて登録する

            product_price.append(int(str(price.string[1::]).replace(',','')))  # 体裁を整えて登録する

        return cls(product_url, product_title, product_price, product_date)

# define urls
urls = [
    "http://kakaku.com/item/K0001014634/pricehistory/",
    "http://kakaku.com/item/K0001095746/pricehistory/",
    "http://kakaku.com/item/K0001095680/pricehistory/",
    "http://kakaku.com/item/K0001095676/pricehistory/",
    "http://kakaku.com/item/K0001019734/pricehistory/"
]

kakaku_list = []
for url in urls:
    kakaku_cls = Kakaku().import_from_url(url)
    kakaku_list.append(kakaku_cls)

#デバッグ用Print文
for kakaku in kakaku_list:
    print(kakaku.product_title)
    for date, price in zip(kakaku.product_date,kakaku.product_price):
        print(date, price)
    print()

import pandas as pd
kakaku_Title = []
kakaku_Date = []
kakaku_Price = []

for kakaku in kakaku_list:
    for j in range(len(kakaku.product_date)):
        kakaku_Title.append(kakaku.product_title)  # タイトルだけのリストを作成
    kakaku_Date += kakaku.product_date  # 日付だけのイストを作成
    kakaku_Price += kakaku.product_price  # 値段だけのリストを作成

kakaku_data = pd.DataFrame(
        {"Title":kakaku_Title,
         "Date":kakaku_Date,
         "Price":kakaku_Price})


import altair as alt

alt.Chart(kakaku_data, height=500 ,width=700).configure(background='white').configure_legend(labelLimit=0).mark_line().encode(
        x="Date:T",
        y="Price:Q",
        color="Title:N"
        )
