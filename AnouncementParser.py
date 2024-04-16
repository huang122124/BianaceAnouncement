
from bs4 import BeautifulSoup

import json
import time

import LogHelper

anm_url = "https://www.binance.com/en/amp/support/announcement/c-48?navId=48"
# # catalogs index
# New_Cryptocurrency_Listing = 0
# Latest_Binance_News = 1
# Latest_Activities = 2
# New_Fiat_Listings = 3
# Delisting = 4
# Wallet_Maintenance_Updates = 5
# API_Updates = 6
# Crypto_Airdrop = 7

def parse(catalog,html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.find_all(id="__APP_DATA")[0].string
    try:
        catalogs = json.loads(text).get("appState").get("loader").get("dataByRouteId").get("d969").get("catalogs")
        if len(catalogs) > 0 and catalog is not None:
            articles = catalogs[catalog].get("articles")
            if len(articles) > 0:
                id = articles[0].get("id")
                code = articles[0].get("code")
                title = articles[0].get("title")
                releaseDate = articles[0].get("releaseDate")
                # tranfer
                date = time.strftime("%m-%d %H:%M:%S", time.localtime(float(releaseDate / 1000)))
                url = "https://www.binance.com/en/support/announcement/" + code
                return id,date, title, url
    except Exception as e:
        print(text)
        LogHelper.print_error(e)

