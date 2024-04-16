# This is a sample Python script.
import decimal
import string
import sys
import time
from random import random

import requests
from requests.exceptions import ProxyError, SSLError
from urllib3.exceptions import ConnectTimeoutError

import AnouncementParser
import BinanceHelper
import ConfigLoader
import LogHelper
import configparser

import RequestHelper
from LogHelper import *

# url = "https://www.binance.com/bapi/composite/v1/public/market/notice/get?page=1&rows=10"
url = ""
# proxy= {'https': 'http://efajwwhm:yii3oiijtbfy@45.252.57.170:6615'}
# proxy = {'https': 'overseas.tunnel.qg.net:14459'}
# proxy = {'https': 'http://127.0.0.1:7890'}
# catalogs index
New_Cryptocurrency_Listing = 0
Latest_Binance_News = 1
Latest_Activities = 2
New_Fiat_Listings = 3
Delisting = 4
Wallet_Maintenance_Updates = 5
API_Updates = 6
Crypto_Airdrop = 7

leverage = 10


def start():
    # Use a breakpoint in the code line below to debug your script.
    idList = [197537]
    balance = BinanceHelper.updateBalance()
    LogHelper.print_info("balance:", balance)
    # fast = ['103.75.68.233:50100', '103.75.68.216:50100', '103.75.68.61:50100', '103.75.68.129:50100', '103.75.68.135:50100', '103.75.68.131:50100', '103.75.68.117:50100', '103.75.68.247:50100', '103.75.68.242:50100', '103.75.68.241:50100', '103.75.68.157:50100', '103.75.68.154:50100', '103.75.68.233:50100', '103.75.68.215:50100', '103.75.68.216:50100', '103.75.68.61:50100', '103.75.68.129:50100', '103.75.68.135:50100', '103.75.68.131:50100', '103.75.68.117:50100', '103.75.68.247:50100', '103.75.68.242:50100', '103.75.68.241:50100', '103.75.68.157:50100', '103.75.68.154:50100']
    while True:
        proxies = RequestHelper.getProxies_qg()
        if len(proxies) > 0:
            while True:
                isExpired = False
                for proxy in proxies:
                    try:
                        bnb_price = BinanceHelper.updateBNBprice()  # BNB price
                        LogHelper.print_info("bnb_price:", bnb_price)
                        LogHelper.print_info("using proxy:", proxy)
                        for i in range(5):
                            start = time.time()
                            response = requests.get(url=url,params={"temp":random()}, proxies={'https': proxy}, timeout=5)
                            if response.status_code == 200:
                                (article_id, date, title, link) = AnouncementParser.parse(
                                    New_Cryptocurrency_Listing,
                                    response.text)
                                end = time.time()
                                duration = end - start
                                LogHelper.print_info(
                                    "finish parsing in " + format(duration, '.2f') + "s")  # print the time cost
                                if "Launchpool" in title and article_id not in idList:
                                    print("article_id:", article_id)
                                    idList.append(article_id)
                                    LogHelper.print_info(date + " " + "Found new title:" + title)
                                    # place order,safety to place 95% amount
                                    quantity = format(balance * leverage * decimal.Decimal(0.95) / bnb_price, ".2f")
                                    BinanceHelper.placeOrder(quantity)
                                    RequestHelper.postToTG(date + " " + title + "\n" + link)
                                    LogHelper.print_info('updating.....')
                            else:
                                LogHelper.print_error("request error:" + str(response.status_code))
                                break
                    except ProxyError as e:
                        isExpired = RequestHelper.checkProxyExpired_qg()
                        if isExpired:
                            LogHelper.print_error("Proxy expired!!!")
                            time.sleep(2)
                            break
                        else:
                            LogHelper.print_error("Proxy error:" + str(e))
                            continue
                    except (SSLError, ConnectTimeoutError, BaseException) as e:
                        RequestHelper.postToTG("ssl error:" + str(e))
                        LogHelper.print_error(e)
                        continue
                if isExpired:
                    break


# Press the green button in the gutter to run the script.
def loadConfig():
    global url
    url = ConfigLoader.get('URL')
    global tg_url
    tg_url = ConfigLoader.get("TG_URL")
    global chat_id
    chat_id = ConfigLoader.get("CHAT_ID")
    global qg_proxy
    qg_proxy = ConfigLoader.get("QG_HTTP_PROXIES")


if __name__ == '__main__':
    LogHelper.createLogFile("info", logging.INFO)
    loadConfig()
    start()
