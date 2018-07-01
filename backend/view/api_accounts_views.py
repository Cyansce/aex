from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
import json

from backend.ext import JsonEncoder

from backend.models import APIAccount
# Create your views here.

def api_accounts(request):
    api_accounts = APIAccount.objects.all().order_by('-id')
    res_data = []
    for api_account in api_accounts:
        res_data.append({
            'id': api_account.id, 
            'name': api_account.name, 
            'key': api_account.key, 
            'skey': api_account.skey, 
            'user_id': api_account.user_id
            })

    json_coins = json.dumps(res_data, cls=JsonEncoder)
    return HttpResponse(json_coins)

def add_api_account(request):
    name = json.loads(request.body).get('name')
    key = json.loads(request.body).get('key')
    skey = json.loads(request.body).get('skey')
    user_id = json.loads(request.body).get('user_id')
    if key == '' or skey == '' or user_id == '':
        return HttpResponse('')
    api_account = APIAccount.objects.create(name=name, key=key, skey=skey, user_id=user_id)
    api_account.save()
    res_data = {'id': api_account.id, 'name': api_account.name, 'key': api_account.key, 'skey': api_account.skey, 'user_id': api_account.user_id }
    return HttpResponse(json.dumps(res_data, cls=JsonEncoder))

def del_api_account(request, id):
    if id == '' or id <= 0:
        return HttpResponse('')
    api_account = APIAccount.objects.get(id=id)
    api_account.delete()
    return HttpResponse('succ')