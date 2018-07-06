import time, datetime

from backend.models import OrderLog, StrategyOrderLoop, ReservationOrder

from backend.tool import api_trade

# 文件名：alo => api_loop_order 循环使用api挂单
# 原理：
# 1.查找数据库中挂好单的成交记录
# 2.计算盈利点后卖出，并修改数据库中已完成



def loop():
    print('-')
    print('-')
    print('-API:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('-')

    # 1.找出所有配置的策略
    strategys = StrategyOrderLoop.objects.all()

    # 2.根据策略开始处理挂单
    for strategy in strategys:
        if not strategy.account.is_api:
            continue
        # 1.查所有订单，条件：
        #               1.未完成 complete=False
        #               2.api单 is_api=True
        #               3.是策略单 is_strategy=True
        #               4.策略未完成 is_strategy_complete=False
        #               5.满足策略条件 
        init_orders = OrderLog.objects.filter(
                                # complete=0, 不完成也没关系
                                is_api=1, 
                                is_strategy=1, 
                                is_strategy_complete=0, 
                                account_id=strategy.account.id,
                                zone_name=strategy.zone_name,
                                coin_name=strategy.coin_name
                            )
        print('- 初始挂单条数：', len(init_orders))
        print('-')
        if len(init_orders) == 0:
            print('- 没有挂单~~~', str(strategy.account.id), strategy.zone_name, strategy.coin_name)
            continue
        # 2.查找并处理对应aex网站上的挂单
        aex_order_ids = extract_order_list_ids(api_trade.get_order_list(strategy.account.id, strategy.zone_name, strategy.coin_name))
        # print('----------------我的挂单id----------------')
        # print(aex_order_ids)
        if len(aex_order_ids) == 0:
            print('- 获取不到挂单，查下ip是否更改---')
            print('-')
            continue
                
        print('- 策略：', strategy.zone_name, '-', strategy.coin_name, '-', strategy.percent)
        print('-')

        # 3.处理初始挂单
        #   判断number是否还在挂单中
        for init_order in init_orders:
            # 如果不在说明已经成交，处理掉挂单；如果还在，不做处理
            if init_order.number not in aex_order_ids:   # 字符or 数字?????
                # 开始挂盈利的单
                price = 0
                trade_type = 0
                # 如果是买单，价格提升对应盈利点挂卖但
                print('-----------------------------------------')
                print('- 当前初始挂单类型---' + str(init_order.trade_type))
                print('-')
                print('- 当前初始挂单价格---' + str(init_order.price))
                print('-')

                if init_order.trade_type == 1: 
                    price = round(init_order.price + init_order.price*strategy.percent, strategy.point)
                    trade_type = 2
                # 如果是卖单，价格减去对应盈利点挂买但
                if init_order.trade_type == 2:
                    price = round(init_order.price - init_order.price*strategy.percent, strategy.point)
                    trade_type = 1
                print('- 盈利后价格---' + str(price))
                print('-')
                
                res_data = api_trade.make_order(
                    init_order.account_id,
                    init_order.zone_name,
                    init_order.coin_name,
                    trade_type,
                    price,
                    init_order.amount
                )
                print('- 挂单结果---' + str(res_data))
                print('-')

                if 'succ' in res_data:
                    init_order.complete = True
                    init_order.is_strategy_complete = True
                    init_order.save()
        
        # 开始循环预约单
        # 放这里目的是可以重复使用aex挂单列表 aex_order_ids
        loop_reservation_order(aex_order_ids)



def extract_order_list_ids(order_list):
    # 
    # 提取挂单ID
    # 
    order_ids = []
    # print(order_list)
    if order_list is not None and len(order_list) > 0:
        for order in order_list:
            order_ids.append(order['id'])
    return order_ids
    


# 
# 预约单循环
# 
def loop_reservation_order(aex_order_ids):
    print('-')
    print('- Reservation Order -')
    print('-')
    # 1.查找所有 已经挂的预约单 

    init_r_orders = ReservationOrder.objects.filter(
                                    is_complete=False,
                                    is_cancel=False
                                )
    # 2.如果该单已成交，便开始挂对应的预约价格的单
    #   并修改相应的状态
    print('- 当前预约单条数：', len(init_r_orders))
    print('-')
    for r_order in init_r_orders:
        if r_order.number not in aex_order_ids:
            trade_type = 2 if r_order.trade_type == 1 else 1
            print('-')
            print('- 原始预约价格：', r_order.price)
            print('-')
            print('- 预约交易类型：', trade_type)
            print('-')
            print('- 预约价格：', r_order.reservation_price)
            print('-')

            res_data = api_trade.just_make_order(
                        r_order.account_id,
                        r_order.zone_name,
                        r_order.coin_name,
                        trade_type,
                        r_order.reservation_price,
                        r_order.amount
                    )
            print('- 预约挂单结果：', res_data)
            print('-')
            if 'succ' in res_data:
                r_order.is_complete = True
                temp = res_data.split('|')
                if len(temp) == 2:
                    r_order.reservation_number = temp[1]
                r_order.save()





def start():
    while(True):
        loop()
        time.sleep(2)
