from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
import json

from backend.ext import JsonEncoder
from backend.tool import trade

from backend.models import GatFlushLog, Account

def balance(request, account_id):
    if account_id <= 0:
        return HttpResponse('account is null')
    return HttpResponse(json.dumps(trade.get_balance(account_id)))

def get_trade_list30(request, account_id):
    if account_id <= 0:
        return HttpResponse('account is null')
    try:
        zone = json.loads(request.body).get('zone')
        coin = json.loads(request.body).get('coin')
    except:
        return HttpResponse('params error')
    return HttpResponse(json.dumps(trade.get_trade_list30(account_id, zone, coin)))

def make_order(request):
    try:
        account_one_id = json.loads(request.body).get('account_one_id')
        account_two_id = json.loads(request.body).get('account_two_id')
        zone = json.loads(request.body).get('zone')
        coin = json.loads(request.body).get('coin')
        price = json.loads(request.body).get('price')
        amount = json.loads(request.body).get('amount')
        come_from = int(json.loads(request.body).get('come_from'))
    except:
        return HttpResponse('params error')
    
    account_one = Account.objects.get(id=account_one_id)
    account_two = Account.objects.get(id=account_two_id)
    if account_one is None or account_two is None:
        return HttpResponse('account is null')
    print(account_one, account_two, zone, coin, price, amount, come_from)
    
    if come_from == 1: # 账户1 买
        res_data = 'account1 buy -'
        res1 = trade.make_order(account_one.id, zone, 1, coin, price, amount)
        res_data += res1
        if 'succ' in res1:
            write_gat_flush_log(account_one.id, coin, zone, price, amount, 1)
            res2 = trade.make_order(account_two.id, zone, 2, coin, price, amount)
            res_data += ' | account2 sell -' + res2
            if 'succ' in res2:
                write_gat_flush_log(account_two.id, coin, zone, price, amount, 2)
        return HttpResponse(res_data)

    if come_from == 2: # 账户1 卖
        res_data = 'account1 sell -'
        print('----22-------')
        res1 = trade.make_order(account_one.id, zone, 2, coin, price, amount)
        print('--res1 ----', res1)
        res_data += res1
        print(res_data)
        if 'succ' in res1:
            write_gat_flush_log(account_one.id, coin, zone, price, amount, 2)
            res2 = trade.make_order(account_two.id, zone, 1, coin, price, amount)
            res_data += ' | account2 sell -' + res2
            if 'succ' in res2:
                write_gat_flush_log(account_two.id, coin, zone, price, amount, 1)
        return HttpResponse(res_data)

    if come_from == 3: # 账户2 买
        res_data = 'account2 buy -'
        res1 = trade.make_order(account_two.id, zone, 1, coin, price, amount)
        res_data += res1
        if 'succ' in res1:
            write_gat_flush_log(account_two.id, coin, zone, price, amount, 1)
            res2 = trade.make_order(account_one.id, zone, 2, coin, price, amount)
            res_data += ' | account1 sell -' + res2
            if 'succ' in res2:
                write_gat_flush_log(account_one.id, coin, zone, price, amount, 2)
        return HttpResponse(res_data)

    if come_from == 4: # 账户2 卖
        res_data = 'account2 sell -'
        res1 = trade.make_order(account_two.id, zone, 2, coin, price, amount)
        res_data += res1
        if 'succ' in res1:
            write_gat_flush_log(account_two.id, coin, zone, price, amount, 2)
            res2 = trade.make_order(account_one.id, zone, 1, coin, price, amount)
            res_data += ' | account1 buy -' + res2
            if 'succ' in res2:
                write_gat_flush_log(account_one.id, coin, zone, price, amount, 1)
        return HttpResponse(res_data)


def gat_flush_logs(request):
    logs = GatFlushLog.objects.order_by('-id').all()[0:20]

    res_data = []
    for log in logs:
        res_data.append({
            'id': log.id,
            'account_name': log.account.name,
            'zone_name': log.zone_name,
            'coin_name': log.coin_name,
            'trade_type': log.trade_type,
            'price': log.price,
            'amount': log.amount,
            'create_at': log.create_at,
        })

    return HttpResponse(json.dumps(res_data, cls=JsonEncoder))



def write_gat_flush_log(account_id, coin_name, zone_name, price, amount, trade_type):
    log = GatFlushLog.objects.create(
        account_id = account_id,
        coin_name = coin_name,
        zone_name = zone_name,
        price = price,
        amount = amount,
        trade_type = trade_type
    )
    log.save()