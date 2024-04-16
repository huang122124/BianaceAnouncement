import decimal
import hmac
import time
import hashlib
import requests
import json
from urllib.parse import urlencode

import ConfigLoader
import LogHelper
import RequestHelper

""" This is a very simple script working on Binance API

- work with USER_DATA endpoint with no third party dependency
- work with testnet

Provide the API key and secret, and it's ready to go

Because USER_DATA endpoints require signature:
- call `send_signed_request` for USER_DATA endpoints
- call `send_public_request` for public endpoints

```python

python um_futures.py

```

"""

KEY = ConfigLoader.get('APIKEY')
SECRET = ConfigLoader.get('SECRETKEY')
BASE_URL = 'https://fapi.binance.com' # production base url
# BASE_URL = "https://testnet.binancefuture.com"  # testnet base url
# print("key:",KEY)
# print("SECRET:",SECRET)
""" ======  begin of functions, you don't need to touch ====== """


''' ======= My functions ============'''
def placeOrder(quantity):
    response = _placeOrder(quantity)
    LogHelper.print_info(response)
    if "code" in response.keys():
        response = _placeOrder(format(quantity*0.9,".2f"))
        LogHelper.print_info(response)
        if "code" in response.keys():
            response = _placeOrder(format(quantity*0.8,".2f"))
            LogHelper.print_info(response)
            if "code" in response.keys():
                response = _placeOrder(format(quantity * 0.7, ".2f"))
                LogHelper.print_info(response)
    if "code" in response.keys():
        LogHelper.print_info("BNB下单失败,"+str(response))
        RequestHelper.postToTG("BNB下单失败,"+str(response))
    else:
        LogHelper.print_info("BNB下单成功！！！ 数量：" + response['origQty'])
        RequestHelper.postToTG("BNB下单成功！！！ 数量：" + response['origQty'])
def _placeOrder(quantity):
    LogHelper.print_info("开始下单....",quantity)
    params = {"symbol": "BNBUSDT",
              "side": "BUY",
              "type": "MARKET",
              "quantity": quantity,
              }
    return send_signed_request("POST", "/fapi/v1/order", params)
# GET /fapi/v2/ticker/price
def updateBNBprice():
    params = {"symbol": "BNBUSDT"}
    r = send_public_request( "/fapi/v2/ticker/price", params)
    return decimal.Decimal(r["price"])

# GET /fapi/v2/balance   (USER_DATA)
def updateBalance():
    r = send_signed_request("GET","/fapi/v2/balance")
    if len(r)==0:
        LogHelper.print_error(r)
    usdt_index = 6
    balance = r[usdt_index].get("balance")
    return decimal.Decimal(balance)


''' ======= My functions end============'''


def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")


# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload)
    # replace single quote to double quote
    query_string = query_string.replace("%27", "%22")
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
            BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request("GET")(url=url)
    return response.json()


""" ======  end of functions ====== """

### public data endpoint, call send_public_request #####
# get klines
# response = send_public_request(
#     "/fapi/v1/klines", {"symbol": "BTCUSDT", "interval": "1d"}
# )
# print(response)


# get account informtion
# if you can see the account details, then the API key/secret is correct
# response = send_signed_request("GET", "/fapi/v2/account")
# print(response)

### 实际开仓配置
# placeOrder(0.12)



### USER_DATA endpoints, call send_signed_request #####
# place an order
# if you see order response, then the parameters setting is correct
# if it has response from server saying some parameter error, please adjust the parameters according the market.
# params = {
#     "symbol": "BNBUSDT",
#     "side": "BUY",
#     "type": "LIMIT",
#     "timeInForce": "GTC",
#     "quantity": 1,
#     "price": "15",
# }
# response = send_signed_request("POST", "/fapi/v1/order", params)
# print(response)
#
# # place batch orders
# # if you see order response, then the parameters setting is correct
# # if it has response from server saying some parameter error, please adjust the parameters according the market.
# params = {
#     "batchOrders": [
#         {
#             "symbol": "BNBUSDT",
#             "side": "BUY",
#             "type": "STOP",
#             "quantity": "1",
#             "price": "9000",
#             "timeInForce": "GTC",
#             "stopPrice": "9100",
#         },
#         {
#             "symbol": "BNBUSDT",
#             "side": "BUY",
#             "type": "LIMIT",
#             "quantity": "1",
#             "price": "15",
#             "timeInForce": "GTC",
#         },
#     ]
# }
# response = send_signed_request("POST", "/fapi/v1/batchOrders", params)
# print(response)
