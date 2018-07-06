from django.shortcuts import render
from django.http import request, HttpResponse
import json

from backend.ext import JsonEncoder

from backend.models import APIConfig

def all(request):
    configs = APIConfig.objects.order_by('-id').values()

    return HttpResponse(json.dumps(list(configs)))

def add(request):
    try:
        url = json.loads(request.body).get('url')
    except:
        return HttpResponse('params error')

    config = APIConfig.objects.create(url=url)
    config.save()
    return HttpResponse('succ')

def set_default(request, id):
    config = APIConfig.objects.get(id=id)
    if config is None:
        return HttpResponse('config is null')
    configs = APIConfig.objects.all()
    for c in configs:
        c.is_default = False
        c.save()
    
    config.is_default = True
    config.save()
    return HttpResponse('succ')

def delete(request, id):
    config = APIConfig.objects.get(id=id)
    if config is None:
        return HttpResponse('config is null')
    config.delete()
    return HttpResponse('succ')

    