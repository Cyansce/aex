import random, requests, json
from datetime import datetime

from backend.models import Account

from backend.tool import cache, log



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}



def login(account_id):
    account = Account.objects.get(id=account_id)
    if account is None:
        return False
    url = 'https://' + account.url + '/login.php?n=' + str(random.random())
    data = {
        'usermail': account.email,
        'password': account.password
    }
    res = requests.post(url, data, headers=headers)
    print(res.text)
    if res.text == 'succ':
        # print(res.headers)
        for header in res.headers:
            # print(header)
            if header == 'Set-Cookie':
                for cookie in res.headers[header].split(';'):
                    # print(cookie)
                    if 'AEX_md5' in cookie:
                        account.md5 = cookie.split('=')[1]
                        account.update_md5_at = datetime.now()        
        account.save()
        return True
    else:
        return False

def test_make_order(account_id, gg_code):
    return make_order(account_id, 'CNC', 2, 'GAT', 0.99, 500, gg_code)


def make_order(account_id, mk_type, trade_type, coinname, price, amount, gg_code=None):
    account = Account.objects.get(id=account_id)
    if account is None:
        return 'account is null'
    # 判断时间
    if account.update_md5_at:
        if (datetime.now()-account.update_md5_at).days >= 2:
            return '请重新登录，并测试交易'
    cookies = {
        'AEX_md5': account.md5,
        'AEX_id': account.user_id
    }
    params = {
        'check': account.md5,
        'coinname': coinname,
        'type': trade_type,
        'price': price,
        'amount': amount,
        'mk_type': mk_type
    }
    if gg_code:
        params['gg_code'] = gg_code

    url = 'https://' + account.url + '/trade/newOrder2.php?n=' + str(random.random())

    try:
        res = requests.post(
            url,
            data=params,
            headers=headers,
            cookies=cookies,
            timeout=5
        )
        res_data = res.content.decode('utf-8')
    except:
        res_data = 'FAPI make order error -----'
    
    return res_data


def get_order_list(account_id, mk_type, coinname):
    account = Account.objects.get(id=account_id)
    if account is None:
        return None
    url = 'https://' + account.url + '/trade/getUserOrder.php?mk_type={0}&coinname={1}&n='.format(mk_type, coinname) + str(random.random())
    # print(url)
    cookies = {
        'AEX_md5': account.md5,
        'AEX_id': account.user_id
    }

    try:
        res = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        res_data = json.loads(res.content.decode('utf-8'))
    except:
        res_data = None
    return res_data


def test(a, b, c):
    data = json.loads(get_order_list(a, b, c))
    print(data)
    

def get_clinch_orders(account_id, mk_type, coinname, page):
    account = Account.objects.get(id=account_id)
    if account is None:
        return None
    url = 'https://' + account.url + '/trade/getUserClinch.php?mk_type={0}&coinname={1}&page={2}&n='.format(mk_type, coinname, page) + str(random.random())
    cookies = {
        'AEX_md5': account.md5,
        'AEX_id': account.user_id
    }
    try:
        res = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        res_data = json.loads(res.content.decode('utf-8'))
    except:
        res_data = []
    return res_data

def cancel_order(account_id, order_id, mk_type, coinname):
    # https://www.aex88.com/trade/delOrder.php?mk_type=CNC&order_id=3795081&coinname=BTC&n=0.26961830490690253
    account = Account.objects.get(id=account_id)
    if account is None:
        return None
    url = 'https://' + account.url + '/trade/delOrder.php?mk_type={0}&order_id={1}&coinname={2}&n='.format(mk_type, order_id, coinname) + str(random.random())
    cookies = {
        'AEX_md5': account.md5,
        'AEX_id': account.user_id
    }
    try:
        res = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        res_data = res.text
    except Exception as e:
        print(e)
        res_data = 'cancel error -----'
    
    return res_data