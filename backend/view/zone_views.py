from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
import json

from backend.ext import JsonEncoder

from backend.models import Zone
# Create your views here.

def zone(request):
    return HttpResponse([{"id": 1, "zone": "CNC"}, {"id": 2, "zone": "BTC"}])

def zones(request):
    return res_zones()

def add_zone(request):
    zone_name = json.loads(request.body).get('zone')    
    if zone_name == '':
        return HttpResponse('')
    zone = Zone.objects.create(name=zone_name.upper())
    zone.save()
    return res_zones()

def del_zone(request):
    id = json.loads(request.body).get('id')
    if id == '' or id <= 0:
        return HttpResponse('')
    zone = Zone.objects.get(id=int(id))
    zone.delete()
    return res_zones()


def res_zones():
    zones = Zone.objects.values('id', 'name', 'create_at').order_by('-id')
    return HttpResponse(json.dumps(list(zones), cls=JsonEncoder))