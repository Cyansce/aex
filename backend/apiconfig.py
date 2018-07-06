import time, hashlib

from backend.models import APIConfig

config = APIConfig.objects.filter(is_default=True).first()

SUBMITORDER_URL = 'https://api.bit.cc/submitOrder.php'
TICKER_URL = 'https://api.bit.cc/ticker.php'
BALANCE_URL = 'https://api.bit.cc/getMyBalance.php'
ORDER_LIST_URL = 'https://api.bit.cc/getOrderList.php'
CANCEL_ORDER_URL = 'https://api.bit.cc/cancelOrder.php'

if config is not None:
    SUBMITORDER_URL = 'https://{url}/submitOrder.php'.format(url=config.url)
    TICKER_URL = 'https://{url}/ticker.php'.format(url=config.url)
    BALANCE_URL = 'https://{url}/getMyBalance.php'.format(url=config.url)
    ORDER_LIST_URL = 'https://{url}/getOrderList.php'.format(url=config.url)
    CANCEL_ORDER_URL = 'https://{url}/cancelOrder.php'.format(url=config.url)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def get_md5(time_str, account):
    md5_str = account.key + '_' + account.user_id + '_' + account.skey + '_' + time_str
    return hashlib.md5(md5_str.encode('utf-8')).hexdigest()

def submitOrder_params(account, type, mk_type, price, amount, coinname):
    time_str = str(time.time())
    return {
        'key': account.key,
        'time': time_str,
        'md5': get_md5(time_str, account),
        'type': type,
        'mk_type': mk_type,
        'price': price,
        'amount': amount,
        'coinname': coinname
    }

def balance_params(account):
    time_str = str(time.time())
    return {
        'key': account.key,
        'time': time_str,
        'md5': get_md5(time_str, account)
    }

def order_list_params(account, mk_type, coinname):
    time_str = str(time.time())
    return {
        'key': account.key,
        'time': time_str,
        'md5': get_md5(time_str, account),
        'mk_type': mk_type,
        'coinname': coinname
    }

def cancel_order_params(account, order_id, mk_type, coinname):
    time_str = str(time.time())
    return {
        'key': account.key,
        'time': time_str,
        'md5': get_md5(time_str, account),
        'mk_type': mk_type,
        'coinname': coinname,
        'order_id': order_id
    }