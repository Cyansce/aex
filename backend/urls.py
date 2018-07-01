from django.urls import path

from . import views
from backend.view import coin_views, zone_views, api_accounts_views

from backend.view import api_trade_views, log_views, trade_views
from backend.view import account_views, strategy_loop_views

urlpatterns = [
    path('zone', views.zone, name='zone'),
]

# 数据修改区
urlpatterns += {
    path('add_zone', zone_views.add_zone, name='add_zone'),
    path('zones', zone_views.zones, name='zones'),
    path('del_zone', zone_views.del_zone, name='del_zone'),

    path('coins', coin_views.coins, name='coins'),
    path('coin/<int:id>', coin_views.coin, name='coin'),
    path('add_coin', coin_views.add_coin, name='add_coin'),
    path('del_coin/<int:id>', coin_views.del_coin, name='del_coin'),

    path('api_accounts', api_accounts_views.api_accounts, name='api_accounts' ),
    path('add_api_account', api_accounts_views.add_api_account, name='add_api_account' ),
    path('del_api_account/<int:id>', api_accounts_views.del_api_account, name='del_api_account' ),

    path('accounts', account_views.accounts, name='accounts' ),
    path('add_account', account_views.add_account, name='add_account' ),
    path('del_account/<int:id>', account_views.del_account, name='del_account' ),
    path('update_account/<int:id>', account_views.update_account, name='update_account' ),

    path('strategys', strategy_loop_views.strategys, name='strategys' ),
    path('add_strategy', strategy_loop_views.add_strategy, name='add_strategy' ),
    path('del_strategy/<int:id>', strategy_loop_views.del_strategy, name='del_strategy' ),
    path('update_strategy/<int:id>', strategy_loop_views.update_strategy, name='update_strategy' ),
}

# api交易区
urlpatterns += [
    path('ticker', api_trade_views.ticker, name='ticker'),
    path('balance/<int:account_id>', api_trade_views.balance, name='balance'),
    path('order', api_trade_views.order, name='order'),

    path('strategy_api_order', api_trade_views.make_order, name='strategy_api_order'),
]

# log
urlpatterns += [
    path('init_order_logs', log_views.init_order_logs, name='init_order_logs'),
    path('order_logs', log_views.order_logs, name='order_logs'),
    path('cancel_order/<int:id>', log_views.cancel_order, name='cancel_order'),
]

# 直接交易区
urlpatterns += [
    path('make_order', trade_views.make_order, name='make_order'),
    path('login/<int:account_id>', trade_views.login, name='login'),
    path('test_make_order/<int:account_id>', trade_views.test_make_order, name='test_make_order'),
    path('get_order_list', trade_views.get_order_list, name='get_order_list'),
    path('cancel_order_with_trade', trade_views.cancel_order, name='cancel_order_with_trade'),
]