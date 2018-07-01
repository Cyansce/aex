from django.shortcuts import render
from django.http import request, HttpResponse
import json, requests, random

from backend.ext import JsonEncoder

from backend.models import OrderLog

from backend.tool import trade, log

# Create your views here.


def login(request, account_id):
    if account_id == 0 or account_id == '':
        return HttpResponse('')
    if trade.login(account_id):
        return HttpResponse('登录成功')
    else:
        return HttpResponse('登录失败')

def test_make_order(request, account_id):
    if account_id == 0 or account_id == '':
        return HttpResponse('')    
    try:
        gg_code = json.loads(request.body).get('gg_code')
    except:
        gg_code = ''
    if gg_code is None or gg_code == '':
        return HttpResponse('gg_code is null')
    return HttpResponse(trade.test_make_order(account_id, gg_code))


def make_order(request):
    try:
        account_id = json.loads(request.body).get('account_id')
    except:
        return HttpResponse('account is null')
    try:
        zone = json.loads(request.body).get('zone')
        coin = json.loads(request.body).get('coin')
        trade_type = json.loads(request.body).get('trade_type')
        price = json.loads(request.body).get('price')
        amount = json.loads(request.body).get('amount')
    except:
        return HttpResponse('params error')
    res = trade.make_order(account_id, zone, trade_type, coin, price, amount)
    return HttpResponse(res)

def get_order_list(request):
    try:
        account_id = json.loads(request.body).get('account_id')
    except:
        return HttpResponse('account is null')
    try:
        zone = json.loads(request.body).get('zone')
        coin = json.loads(request.body).get('coin')
    except:
        return HttpResponse('params error')
    res = trade.get_order_list(account_id, zone, coin)
    return HttpResponse(json.dumps(res))

def cancel_order(request):
    try:
        order_id = json.loads(request.body).get('order_id')
        zone = json.loads(request.body).get('zone')
        coin = json.loads(request.body).get('coin')
        account_id = json.loads(request.body).get('account_id')
    except:
        return HttpResponse('order_id is null')
    res = trade.cancel_order(account_id, order_id, zone, coin)
    return HttpResponse(res)