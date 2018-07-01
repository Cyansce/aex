from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
import json

from backend.ext import JsonEncoder

from backend.models import Account
# Create your views here.

def accounts(request):
    try:
        is_api = json.loads(request.body).get('is_api')
    except:
        is_api = None
    accounts = Account.objects.all().order_by('-id')
    if type(is_api) is bool:
        accounts = accounts.filter(is_api=is_api)
    res_data = []
    for account in accounts:
        res_data.append({
            'id': account.id, 
            'email': account.email, 
            'md5': account.md5,
            'user_id': account.user_id,
            'url': account.url,
            'update_md5_at': account.update_md5_at,
            'name': account.name,
            'is_api': account.is_api,
            'key': account.key,
            'skey':account.skey[:5]+'**************'+account.skey[-5:] if account.skey else account.skey,
            'password':account.password[:2]+'**************'+account.password[-2:] if account.password else account.password,
            })

    json_coins = json.dumps(res_data, cls=JsonEncoder)
    return HttpResponse(json_coins)

def add_account(request):
    try:        
        is_api = json.loads(request.body).get('is_api')
        name = json.loads(request.body).get('name')
    except:
        return HttpResponse('error')
    account = Account.objects.create(
            is_api=is_api, 
            name=name
            )
    if is_api:        
        try:            
            key = json.loads(request.body).get('key')
            skey = json.loads(request.body).get('skey')
            user_id = json.loads(request.body).get('user_id')
        except:
            return HttpResponse('params error')
        account.key = key
        account.skey = skey
        account.user_id = user_id
    else:  
        try:      
            email = json.loads(request.body).get('email')
            password = json.loads(request.body).get('password')
            user_id = json.loads(request.body).get('user_id')
            url = json.loads(request.body).get('url')
        except:
            return HttpResponse('params error')
        if email == '' or password == '':
            return HttpResponse('email or password not null')
        account.email = email
        account.password = password
        account.user_id = user_id
        account.url = url
    account.save()
    return HttpResponse('succ')

def update_account(request, id):
    if id == '' or id <= 0:
        return HttpResponse('id error')
    account = Account.objects.get(id=id)
    if account is None:
        return HttpResponse('')
    if account.is_api:
        try:
            account.key = json.loads(request.body).get('key')
            account.name = json.loads(request.body).get('name')
            account.user_id = json.loads(request.body).get('user_id')
        except:
            return HttpResponse('params error')
    else:
        try:
            account.name = json.loads(request.body).get('name')
            account.email = json.loads(request.body).get('email')
            account.md5 = json.loads(request.body).get('md5')
            account.user_id = json.loads(request.body).get('user_id')
            account.url = json.loads(request.body).get('url')
        except:
            return HttpResponse('params error')            
    account.save()
    return HttpResponse('succ')

def del_account(request, id):
    if id == '' or id <= 0:
        return HttpResponse('')
    account = Account.objects.get(id=id)
    account.delete()
    return HttpResponse('succ')