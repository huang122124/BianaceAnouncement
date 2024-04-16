import random
import time

import requests
from proxy_seller_user_api import Api
import json

import BinanceHelper

url1 = 'https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48'
url2 = 'https://www.binance.com/en/amp/support/announcement/c-48?navId=48#module-0'

def placeOrder():
    params = {"symbol": "BNBUSDT",
              "side": "BUY",
              "type": "MARKET",
              "quantity": 0.01,
              }
    r = BinanceHelper.send_signed_request("POST", "/fapi/v1/order", params)
    print(r)
def test():
    response = requests.get(url='https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48',
                            proxies={'https': '45.133.237.169:12626'}, timeout=5)
    print(response.text)

if __name__ == '__main__':
    test()