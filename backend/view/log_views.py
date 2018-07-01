import json
import requests
import datetime
from datetime import datetime as dt

from django.shortcuts import render
from django.http import request, HttpResponse

from backend.ext import JsonEncoder
from backend.tool import api_trade

from backend.models import OrderLog

# Create your views here.


def init_order_logs(request):
    order_logs = OrderLog.objects.order_by('-id').values()[0:20]
    res_data = json.dumps(list(order_logs), cls=JsonEncoder)

    return HttpResponse(res_data)


def order_logs(request):
    try:
        account_id = json.loads(request.body).get('account_id')
        zone_name = json.loads(request.body).get('zone_name')
        coin_name = json.loads(request.body).get('coin_name')
        trade_type = int(json.loads(request.body).get('trade_type'))
        is_cancel = json.loads(request.body).get('is_cancel')
        is_strategy_complete = json.loads(
            request.body).get('is_strategy_complete')
    except:
        return HttpResponse('params error')

    order_logs = OrderLog.objects.filter(
        account_id=account_id,
        zone_name=zone_name,
        coin_name=coin_name,
        is_cancel=is_cancel,
        is_strategy_complete=is_strategy_complete
    )

    if trade_type == 1 or trade_type == 2:
        order_logs = order_logs.filter(trade_type=trade_type)

    print(json.loads(request.body).get('date_start'))
    try:
        date_start = json.loads(request.body).get('date_start')
        y, m, d = date_start.split('-')
        date_start = dt(int(y), int(m), int(d))
    except:
        date_start = None
    try:
        date_end = json.loads(request.body).get('date_end')
        y, m, d = date_end.split('-')
        date_end = dt(int(y), int(m), int(d)) + datetime.timedelta(days=1)

    except:
        date_end = None

    if date_start is not None:
        order_logs = order_logs.filter(create_at__gte=date_start)
    if date_end is not None:
        order_logs = order_logs.filter(create_at__lt=date_end)

    count = len(order_logs)
    # print(count)
    money_sum = 0
    min_price = 0 if count <= 0 else order_logs[0].price
    max_price = 0 if count <= 0 else order_logs[0].price
    for item in order_logs:
        money_sum += item.price * item.amount
        min_price = item.price if item.price < min_price else min_price
        max_price = item.price if item.price > max_price else max_price

    try:
        page = int(json.loads(request.body).get('page'))
        if page < 0:
            page = 0
    except:
        page = 0
    order_logs = order_logs.order_by('-id').values(
        'id',
        'zone_name',
        'coin_name',
        'trade_type',
        'price',
        'amount',
        'number',
        'is_strategy_complete',
        'is_cancel',
        'create_at'
    )[page*20:(page+1)*20]

    res_data = dict(
        count=count,
        money_sum=round(money_sum, 6),
        min_price=min_price,
        max_price=max_price,
        data=list(order_logs)
    )

    return HttpResponse(json.dumps(res_data, cls=JsonEncoder))


def cancel_order(request, id):
    # 条件：
    #   策略设为完成 is_strategy_complete = 1
    #   并且撤销网站上的单
    order = OrderLog.objects.get(id=id)
    if order is None:
        return HttpResponse('order is null')

    if order.is_strategy_complete:
        return HttpResponse('already complete')

    res = api_trade.cancel_order(
        order.account_id, order.number, order.zone_name, order.coin_name)
    print(res)
    print(res == 'succ')
    print('succ' in res)
    print(type(res))
    if 'succ' in res or 'no_record' in res:
        order.is_strategy_complete = True
        order.is_cancel = True
        order.save()
        return HttpResponse('succ')
    else:
        return HttpResponse(res)
