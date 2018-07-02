import datetime, time

from backend.models import OrderLog, StrategyOrderLoop, OrderLoopNumbersLog

from backend.tool import trade, log

# 文件名：lo => loop_order 循环挂单
# 原理：
# 1.获取aex网站已成交的单
# 2.满足相应条件的单计算赢点挂会对应的单
#   比如：已成交一笔卖单，就减掉一定价格挂买单买回



def loop():
    print('-')
    print('-')
    print('-非API', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('-')

    # 1.找出所有配置的策略
    strategys = StrategyOrderLoop.objects.all()

    # 2.根据策略开始处理挂单
    for strategy in strategys:
        if strategy.account.is_api:
            continue
        # 1.查aex网站已完成订单，条件：
        #               1.第一页 page=1
        #               2.aex完成订单格式
        #                   [{
        #                       "id":"292311",
        #                       "buyer_id":"498514",
        #                       "seller_id":"0",
        #                       "volume":"600.00000000",
        #                       "price":"0.02000000",
        #                       "coinname":"gat",
        #                       "time":"2018-06-29 11:31:54"
        #                   }]
        clinch_orders = trade.get_clinch_orders(
                                    strategy.account.id, 
                                    strategy.zone_name, 
                                    strategy.coin_name,
                                    0
                                    )
        if len(clinch_orders) == 0:
            print('- 没有已完成单--------------------------')
            continue
        
        print('- 策略：', strategy.zone_name, '-', strategy.coin_name, '-', strategy.percent)
        print('-')

        # 2.查已经处理过的已完成单
        #   条件：
        #       1.时间为之前24小时之内的所有单号
        yestoday = datetime.datetime.now() - datetime.timedelta(days=1)
        order_numbers = extract_order_numbers(OrderLoopNumbersLog.objects.filter(create_at__gt=yestoday))

        # 3.开始卓条处理aex上面已完成的单
        #   条件：
        #       1.在一定价格之内 max_price, min_price
        #       2.时间在策略开始时间之后 time > start_time
        #       3.单号没有在已处理过的单号内 id not in order_numbers
        for clinch_order in clinch_orders:
            price = float(clinch_order['price'])
            order_time = get_time_by_str(clinch_order['time'])
            if order_time is None or order_time < strategy.start_time:
                continue
            if price > strategy.max_price or price < strategy.min_price:
                continue
            if clinch_order['id'] in order_numbers:
                continue
            # 4.满足条件后
            #   1.开始挂相对应盈利的单
            #   2.挂单成功保存记录
            #   3.挂单成功讲id写入numbers表内
            trade_type = 0
            new_price = 0
            # 如果是卖
            if clinch_order['buyer_id'] == '0' and clinch_order['seller_id'] is not '0':
                trade_type = 1
                new_price = round(price - price*strategy.percent, strategy.point)
            # 如果是买
            if clinch_order['seller_id'] == '0' and clinch_order['buyer_id'] is not '0':
                trade_type = 2
                new_price = round(price + price*strategy.percent, strategy.point)
            print('- 原始价格------------', price)
            print('-')
            print('- 盈利后价格------------', new_price)
            print('-')
            print('- trade_type------------', trade_type)
            print('-')
            amount = float(clinch_order['volume'])
            res = trade.make_order(strategy.account.id, strategy.zone_name, trade_type, strategy.coin_name, new_price, amount)

            print('- 挂单结果 ------', res)

            if res == 'succ':
                log.write_order_log_not_api_strategy_complete(
                    strategy.account.id,
                    'n_api strategy no account',
                    strategy.coin_name,
                    strategy.zone_name,
                    1 if trade_type==2 else 2,
                    price,
                    amount,
                    res + '|' + clinch_order['id']
                )
                write_numbers(clinch_order['id'])
            

        

def extract_order_numbers(orders):
    numbers = []
    for order in orders:
        if order.number not in numbers:
            numbers.append(order.number)
    
    return numbers

#  time_str: "2018-06-29 11:31:54"
def get_time_by_str(time_str):
    try:
        _date, _time = time_str.split(' ')
        y, M, d = _date.split('-')
        h, m, s = _time.split(':')
        return datetime.datetime(int(y), int(M), int(d), int(h), int(m), int(s))        
    except:
        return None

def write_numbers(number):
    OrderLoopNumbersLog.objects.create(number=number).save()



def start():
    while(True):
        loop()
        time.sleep(2)