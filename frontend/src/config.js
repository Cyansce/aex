// 交易区
export const zones_url = '/zones'
export const add_zone_url = '/add_zone'
export const del_zone_url = '/del_zone'

// 币种
export const coins_url = '/coins'
export const coin_url = '/coin'
export const add_coin_url = '/add_coin'
export const del_coin_url = '/del_coin'

// key
export const api_accounts_url = '/api_accounts'
export const add_api_account_url = '/add_api_account'
export const del_api_account_url = '/del_api_account'

// api trade
export const ticker_url = '/ticker'
export const balance_url = '/balance'
export const order_url = '/order'

export const strategy_api_order_url = '/strategy_api_order'

// log
export const order_logs_url = '/order_logs'
export const init_order_logs_url = '/init_order_logs'
export const cancel_order_url = '/cancel_order'

// reservation_order
export const reservation_orders_url = '/reservation_orders'
export const add_reservation_order_url = '/add_reservation_order'
export const cancel_reservation_order_url = '/cancel_reservation_order'

// account
export const accounts_url = '/accounts'
export const add_account_url = '/add_account'
export const del_account_url = '/del_account'
export const update_account_url = '/update_account'
export const login_url = '/login'
export const test_make_order_url = '/test_make_order'

// strategy
export const strategys_url = '/strategys'
export const add_strategy_url = '/add_strategy'
export const del_strategy_url = '/del_strategy'
export const update_strategy_url = '/update_strategy'

// trade
export const make_order_url = '/make_order'
export const get_order_list_url = '/get_order_list'
export const cancel_order_with_trade_url = '/cancel_order_with_trade'








// 工具函数
export const tool = {
    write_storage_obj: function(name, obj){
        window.localStorage.setItem(name, JSON.stringify(obj))
    },
    get_storage_obj: function(name) {
        return JSON.parse(window.localStorage.getItem(name))
    },
    sleep: function(time) {
        var t = Date.now()
        while(Date.now() - t <= time){}
    }
}