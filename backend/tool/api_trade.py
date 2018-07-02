import random, requests, json
from datetime import datetime

from backend.models import Account

from backend.tool import  log
from backend.apiconfig import TICKER_URL, HEADERS, BALANCE_URL, balance_params, submitOrder_params, SUBMITORDER_URL
from backend.apiconfig import ORDER_LIST_URL, order_list_params
from backend.apiconfig import CANCEL_ORDER_URL, cancel_order_params

# 
# api 使用策略挂单
# 
def make_order(account_id, zone, coin, trade_type, price, amount):
    account = Account.objects.get(id=account_id)
    if account is None:
        return 'account is null'

    params = submitOrder_params(account, trade_type, zone, price, amount, coin)

    try:
        res = requests.post(
            SUBMITORDER_URL,
            headers = HEADERS,
            data = params,
            timeout = 5
        )
        res_data = res.content.decode('utf-8')
        if 'succ' in res_data:
            log.write_order_log(
                True, 
                True,
                account_id,
                account.name, 
                coin,
                zone,
                trade_type,
                price,
                amount,
                res_data 
                )
    except:
        res_data = 'make order error-----'  
    
    return res_data


def get_order_list(account_id, zone, coin):
    account = Account.objects.get(id=account_id)
    if account is None:
        return 'account is null'
    
    params = order_list_params(account, zone, coin)

    try:
        res = requests.post(
            ORDER_LIST_URL,
            headers=HEADERS,
            data=params,
            timeout=5
        )
        res_data = json.loads(res.content.decode('utf-8'))
    except:
        res_data = []

    return res_data


def cancel_order(account_id, order_id, zone, coin):
    account = Account.objects.get(id=account_id)
    if account is None:
        return 'account is null'
    
    params = cancel_order_params(account, order_id, zone, coin)

    try:
        res = requests.post(
            CANCEL_ORDER_URL,
            headers=HEADERS,
            data=params,
            timeout=5
        )
        res_data = res.text
    except:
        res_data = 'cancel error'
    
    return res_data