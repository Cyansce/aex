import json, requests, datetime
from datetime import datetime as dt

from django.shortcuts import render
from django.http import request, HttpResponse

from backend.ext import JsonEncoder
from backend.tool import api_trade

from backend.models import ReservationOrder,Account

# Create your views here.

def reservation_orders(request):
    r_orders = ReservationOrder.objects.order_by('-id').values()
    return HttpResponse(json.dumps(list(r_orders), cls=JsonEncoder))


def add_reservation_order(request):
    try:
        account_id = json.loads(request.body).get('account_id')
        account = Account.objects.get(id=account_id)
        if account is None:
            return HttpResponse('account is null')
    except:
        return HttpResponse('account is null')

    try:
        price = json.loads(request.body).get('price')
        reservation_price = json.loads(request.body).get('reservation_price')
        trade_type = json.loads(request.body).get('trade_type')
        amount = json.loads(request.body).get('amount')
        coin_name = json.loads(request.body).get('coin_name')
        zone_name = json.loads(request.body).get('zone_name')
    except:
        return HttpResponse('params error')
    
    res = api_trade.make_order_reservation(account_id, zone_name, coin_name, trade_type, price, amount, reservation_price)

    return HttpResponse(res)

def cancel_reservation_order(request, id):
    if id == 0 or id is None:
        return HttpResponse('order is null')
    
    r_order = ReservationOrder.objects.get(id=id)
    if r_order is None:
        return HttpResponse('order is null')
    
    try:
        account_id = json.loads(request.body).get('account_id')
        zone = json.loads(request.body).get('zone_name')
        coin = json.loads(request.body).get('coin_name')
    except:
        return HttpResponse('account is null')
    
    res_data = 'cancel - '
    if r_order.number:
        res_data += api_trade.cancel_order(account_id, r_order.number, zone, coin)
    r_order.is_cancel = True
    r_order.save()
    return HttpResponse(res_data)
    