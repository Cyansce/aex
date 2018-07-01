from django.shortcuts import render
from django.http import request, HttpResponse
import json, requests

from backend.ext import JsonEncoder
from backend.tool.log import write_order_log

from backend.models import Account, Coin
from backend.apiconfig import TICKER_URL, HEADERS, BALANCE_URL, balance_params, submitOrder_params, SUBMITORDER_URL
from backend.tool import api_trade
# Create your views here.

def ticker(request):
    coin_id = json.loads(request.body).get('coin_id')
    if coin_id == 0 or coin_id == '':
        return HttpResponse('')
    coin = Coin.objects.get(id=coin_id)
    if coin is None:
        return HttpResponse('')
    url = TICKER_URL.format(coin, coin.zone.name)

    res = requests.get(url, headers = HEADERS)
    return HttpResponse(res)

def balance(request, account_id):
    if account_id <= 0 or account_id == '':
        return HttpResponse('')
    account = Account.objects.get(id=account_id)
    if account is None: 
        return HttpResponse('')
    res = requests.post(
        BALANCE_URL,
        headers = HEADERS,
        data = balance_params(account)
    )
    return HttpResponse(res.content)

def order(request):
    coin_id = json.loads(request.body).get('coin_id')
    account_id = json.loads(request.body).get('account_id')
    if coin_id == 0 or coin_id == '' or account_id == 0 or account_id == '':
        return HttpResponse('')
    coin = Coin.objects.get(id=coin_id)
    account = Account.objects.get(id=account_id)
    if coin is None or account is None:
        return HttpResponse('')
    price = json.loads(request.body).get('price')
    amount = json.loads(request.body).get('amount')
    trade_type = json.loads(request.body).get('trade_type')

    params = submitOrder_params(account, trade_type, coin.zone, price, amount, coin.name)

    res = requests.post(
        SUBMITORDER_URL,
        headers = HEADERS,
        data = params
    )
    if 'succ' in res.content.decode('utf-8'):
        write_order_log(
            True, 
            False,
            account_id,
            account.name, 
            coin.name,
            coin.zone.name,
            trade_type,
            price,
            amount,
            res.content.decode('utf-8')
            )

    return HttpResponse(res.content)


# 
# api 使用策略挂单
# 
def make_order(request):
    try:        
        account_id = json.loads(request.body).get('account_id')
    except:
        return HttpResponse('account_id is null')
    try:
        price = json.loads(request.body).get('price')
        amount = json.loads(request.body).get('amount')
        trade_type = json.loads(request.body).get('trade_type')
        coin = json.loads(request.body).get('coin')
        zone = json.loads(request.body).get('zone')
    except:
        return HttpResponse('params error')
    

    res_data = api_trade.make_order(account_id, zone, coin, trade_type, price, amount)

    return HttpResponse(res_data)