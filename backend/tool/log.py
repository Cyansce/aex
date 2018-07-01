from backend.models import OrderLog


def write_order_log(is_api, is_strategy, account_id, account, coin, zone, trade, price, amount, res_data):
    complete = False
    number = ''
    res = res_data.split('|')
    if len(res) == 2:
        number = res[1]
    else:
        complete = True
    
    log = OrderLog.objects.create(
        is_api=is_api,
        is_strategy = is_strategy,
        account_id = account_id,
        account_name = account,
        coin_name = coin.upper(),
        zone_name = zone.upper(),
        trade_type = trade, 
        number = number,
        price = price,
        amount = amount,
        complete = complete,        
    )

    log.save()


def write_order_log_not_api_strategy_complete(account_id, account, coin, zone, trade, price, amount, res_data):
    complete = False
    number = ''
    res = res_data.split('|')
    if len(res) == 2:
        number = res[1]
    else:
        complete = True
    
    log = OrderLog.objects.create(
        is_api=False,
        is_strategy = True,
        is_strategy_complete = True,
        account_id = account_id,
        account_name = account,
        coin_name = coin.upper(),
        zone_name = zone.upper(),
        trade_type = trade, 
        number = number,
        price = price,
        amount = amount,
        complete = complete,        
    )

    log.save()


