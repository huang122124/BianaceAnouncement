import json
import urllib.parse

import requests
import os
from proxy_seller_user_api import Api

import ConfigLoader
import LogHelper




def getProxies_proxy_seller():
    proxies = []
    api = Api({'key': '8e85010efea393e65e3664d07d46f85a'})
    proxy_type = 'ipv4?orderId=2136249'
    # api.setPaymentId(1)
    # api.setGenerateAuth('N')
    LogHelper.print_info('loading proxies....')
    _proxies = api.proxyList(proxy_type).get('items').values()
    for proxy in _proxies:
        ip = proxy['ip']
        port_http = proxy['port_http']
        proxies.append(ip+':'+str(port_http))
    print(proxies)
    return proxies

def getProxies_qg():
    proxies = []
    LogHelper.print_info('loading proxies....')
    response = requests.get(url=ConfigLoader.get('QG_HTTP_PROXIES'),timeout=5)
    if response.json().get('code') == 'NO_AVAILABLE_CHANNEL':
        # LogHelper.print_error(response.json().get("message"))
        raise Exception("没有可用的空闲通道")
    _proxies = response.json().get('data')
    if len(_proxies) > 0:
        for proxy in _proxies:
            ip = proxy['server']
            proxies.append(ip)
        print(proxies)
    return proxies

def checkProxyExpired_qg():
    response = requests.get(ConfigLoader.get("QG_IP_AVAILBLE"),timeout=10)
    data = response.json().get("data")
    if len(data) == 0:
        return True
    else:
        return False
def getAnouncementTest():
    proxy = {'https': '103.122.177.110:12525'}
    reponse = requests.get('https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48',proxies=proxy,timeout=5)
    print(reponse.text)

def postToTG(title):
    requests.post(url=ConfigLoader.get('TG_URL'), params={
        'chat_id': ConfigLoader.get('CHAT_ID'),
        'text': title
    })


if __name__ == '__main__':
    getAnouncementTest()
    # getProxies_proxy_seller()