from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
import json

from backend.ext import JsonEncoder

from backend.models import Coin, Zone
# Create your views here.

def coin(request, id):
    if id <= 0 or id == '':
        return HttpResponse('')
    coin = Coin.objects.get(id=id)
    if coin is None:
        return HttpResponse('')
    res_data = {
        'id': coin.id, 
        'name': coin.name, 
        'point': coin.point, 
        'zone_name': coin.zone.name, 
        'create_at': coin.create_at 
        }
    return HttpResponse(json.dumps(res_data, cls=JsonEncoder))

def coins(request):
    coins = Coin.objects.all().order_by('-id')
    res_data = []
    for coin in coins:
        res_data.append({
            'id': coin.id, 
            'name': coin.name, 
            'point': coin.point, 
            'create_at': coin.create_at, 
            'zone_id': coin.zone.id, 
            'zone_name': coin.zone.name
            })

    json_coins = json.dumps(res_data, cls=JsonEncoder)
    return HttpResponse(json_coins)

def add_coin(request):
    coin_name = json.loads(request.body).get('coin_name')
    zoin_id = json.loads(request.body).get('zone_id')
    point = json.loads(request.body).get('point')
    if coin_name == '' or zoin_id == '':
        return HttpResponse('')
    zone = Zone.objects.get(id=zoin_id)
    if zone is None:
        return HttpResponse('')
    coin = Coin.objects.create(name=coin_name.upper(), zone=zone, point=point)
    coin.save()
    res_data = {
        'id': coin.id, 
        'name': coin.name, 
        'point': coin.point, 
        'zone_name': coin.zone.name, 
        'create_at': coin.create_at 
        }
    return HttpResponse(json.dumps(res_data, cls=JsonEncoder))

def del_coin(request, id):
    if id == '' or id <= 0:
        return HttpResponse('')
    coin = Coin.objects.get(id=id)
    coin.delete()
    return HttpResponse('succ')