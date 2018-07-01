from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
import json

from backend.ext import JsonEncoder

from backend.models import StrategyOrderLoop
from backend.tool import trade
# Create your views here.

def strategys(request):
    strategys = StrategyOrderLoop.objects.all().order_by('-id')
    res_data = []
    for strategy in strategys:
        res_data.append({
            'id': strategy.id, 
            'account_name': strategy.account.name,
            'account_id': strategy.account.id,
            'zone_name': strategy.zone_name,
            'coin_name': strategy.coin_name,
            'percent': strategy.percent,
            'point': strategy.point,
            'start_time': strategy.start_time,
            'min_price': strategy.min_price,
            'max_price': strategy.max_price
            })

    json_coins = json.dumps(res_data, cls=JsonEncoder)
    return HttpResponse(json_coins)

def add_strategy(request):
    try:
        account_id = json.loads(request.body).get('account_id')
        zone_name = json.loads(request.body).get('zone_name')
        coin_name = json.loads(request.body).get('coin_name')
        percent = json.loads(request.body).get('percent')
        point = json.loads(request.body).get('point')
    except:
        return HttpResponse('params error')
    
    if(account_id is None or zone_name is None or coin_name is None or percent is None or point is None):
        return HttpResponse('params error')

    try:
        min_price = json.loads(request.body).get('min_price')
        max_price = json.loads(request.body).get('max_price')
        start_time = json.loads(request.body).get('start_time')
    except:
        min_price = None
        max_price = None
        start_time = None

    strategy = StrategyOrderLoop.objects.create(
        account_id=account_id, 
        zone_name=zone_name.upper(),
        coin_name=coin_name.upper(),
        percent=percent,
        point=point,
        min_price=min_price,
        max_price=max_price,
        start_time = start_time
        )
    
    strategy.save()
    return HttpResponse('succ')

def update_strategy(request, id):
    if id == '' or id <= 0:
        return HttpResponse('')
    strategy = StrategyOrderLoop.objects.get(id=id)
    if strategy is None:
        return HttpResponse('')
    try:
        account_id = json.loads(request.body).get('account_id')
        zone_name = json.loads(request.body).get('zone_name')
        coin_name = json.loads(request.body).get('coin_name')
        percent = json.loads(request.body).get('percent')
        point = int(json.loads(request.body).get('point'))
    except:
        return HttpResponse('params error')
    try:
        min_price = json.loads(request.body).get('min_price')
        max_price = json.loads(request.body).get('max_price')
        start_time = json.loads(request.body).get('start_time')
    except:
        min_price = None
        max_price = None
        start_time = None
    
    strategy.account_id = account_id
    strategy.zone_name = zone_name
    strategy.coin_name = coin_name
    strategy.percent = percent
    strategy.point = point
    strategy.min_price = min_price
    strategy.max_price = max_price
    if start_time is not None:        
        strategy.start_time = start_time
    strategy.save()
    return HttpResponse('succ')

def del_strategy(request, id):
    if id == '' or id <= 0:
        return HttpResponse('')
    strategy = StrategyOrderLoop.objects.get(id=id)
    strategy.delete()
    return HttpResponse('succ')









#  time_str: "2018-06-29 11:31:54"
def get_time_by_str(time_str):
    try:
        _date, _time = time_str.split(' ')
        y, M, d = _date.split('-')
        h, m, s = _time.split(':')
        return datetime.datetime(int(y), int(M), int(d), int(h), int(m), int(s))        
    except:
        return None