<template>
    <div>
        <blockquote class="layui-elem-quote"><h2>GAT 刷单 - 仅供非API账户使用</h2></blockquote>

        <table class="layui-table layui-form">
            <tr>
                <td>
                    <select lay-filter="zone" v-model="zone.id">
                        <option v-for="(item, index) in zones" :key="index" :value="item.id">{{item.name}}</option>
                    </select>
                </td>
                <td>
                    <select lay-filter="coin" v-model="coin.id">
                        <option v-for="(item, index) in coins" :key="index" :value="item.id">{{item.name}}</option>
                    </select>
                </td>
            </tr>
        </table>

        <div class="layui-row">
            <div class="layui-col-xs9">
                <div class="layui-row">
                    <div class="layui-col-xs4">
                        <div class="layui-card">
                            <div class="layui-card-header">
                                账户 1
                            </div>
                            <div class="layui-card-body">
                                <div class="layui-form">
                                    <select lay-filter="account-one" v-model="account_one.id">
                                        <option value="0">请选择</option>
                                        <option v-for="(item, index) in accounts" :key="index" :value="item.id">{{item.name}}</option>
                                    </select>
                                    <table class="layui-table">
                                        <colgroup>
                                            <col width="50%">
                                            <col width="50%">
                                        </colgroup>
                                        <tr>
                                            <td colspan="2">
                                                余额
                                                <button class="layui-btn layui-btn-sm layui-btn-primary" style="float:right" @click="get_balance(account_one.id, true)">刷新</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>{{zone.name}}</td>
                                            <td>{{account_one_balance_zone}}</td>
                                        </tr>
                                        <tr>
                                            <td>{{coin.name}}</td>
                                            <td>{{account_one_balance_coin}}</td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <button class="layui-btn" style="width:100%" @click="make_order(1)">买</button>
                                            </td>
                                            <td>
                                                <button class="layui-btn layui-btn-danger" style="width:100%" @click="make_order(2)">卖</button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="layui-col-xs4">
                        <div class="layui-card">
                            <div class="layui-card-header" style="text-align:center">
                                <i class="layui-icon layui-icon-prev"></i> 互刷
                                <i class="layui-icon layui-icon-next"></i>
                            </div>
                            <div class="layui-card-body">
                                <table class="layui-table">
                                    <tr>
                                        <td colspan="2"><input type="text" placeholder="价格" class="layui-input" v-model="price"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2"><input type="text" placeholder="数量" class="layui-input" v-model="amount"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2"><input type="text" placeholder="金额" class="layui-input" v-model="sum"></td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="layui-col-xs4">
                        <div class="layui-card">
                            <div class="layui-card-header">
                                账户 2
                            </div>
                            <div class="layui-card-body">
                                <div class="layui-form">
                                    <select lay-filter="account-two" v-model="account_two.id">
                                        <option value="0"></option>
                                        <option v-for="(item, index) in accounts" :key="index" :value="item.id">{{item.name}}</option>
                                    </select>
                                    <table class="layui-table">
                                        <colgroup>
                                            <col width="50%">
                                            <col width="50%">
                                        </colgroup>
                                        <tr>
                                            <td colspan="2">
                                                余额
                                                <button class="layui-btn layui-btn-sm layui-btn-primary" style="float:right" @click="get_balance(account_two.id, false)">刷新</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>{{zone.name}}</td>
                                            <td>{{account_two_balance_zone}}</td>
                                        </tr>
                                        <tr>
                                            <td>{{coin.name}}</td>
                                            <td>{{account_two_balance_coin}}</td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <button class="layui-btn" style="width:100%" @click="make_order(3)">买</button>
                                            </td>
                                            <td>
                                                <button class="layui-btn layui-btn-danger" style="width:100%" @click="make_order(4)">卖</button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="layui-row">
                    <div class="layui-col-xs12">
                        <table class="layui-table">
                            <thead>
                                <tr>
                                    <th>Id</th>
                                    <th>账户</th>
                                    <th>交易区</th>
                                    <th>币种</th>
                                    <th>类型</th>
                                    <th>价格</th>
                                    <th>数量</th>
                                    <th>金额</th>
                                    <th>时间</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in gat_flush_logs" :key="index">
                                    <td>{{item.id}}</td>
                                    <td>{{item.account_name}}</td>
                                    <td>{{item.zone_name}}</td>
                                    <td>{{item.coin_name}}</td>
                                    <td>{{item.trade_type | buy-sell}}</td>
                                    <td>{{item.price}}</td>
                                    <td>{{item.amount}}</td>
                                    <td>{{(item.price * item.amount).toFixed(6)}}</td>
                                    <td>{{item.create_at}}</td>
                                </tr>
                            </tbody>

                        </table>
                    </div>
                </div>
            </div>              
            <div class="layui-col-xs3">
                <div class="layui-card">
                    <div class="layui-card-body">
                        <table class="layui-table">
                            <thead>
                                <tr>
                                    <th>价格</th>
                                    <th>数量</th>
                                    <th>总额</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in sell_str" :key="item.id" style="color: #FF5722" @click="get_price(item[0])">
                                    <td>{{item[0]}}</td>
                                    <td>{{item[1]}}</td>
                                    <td>{{(item[0] * item[1]).toFixed(6)}}</td>
                                </tr>
                                <tr v-for="item in buy_str" :key="item.id" style="color: #5FB878" @click="get_price(item[0])">
                                    <td>{{item[0]}}</td>
                                    <td>{{item[1]}}</td>
                                    <td>{{(item[0] * item[1]).toFixed(6)}}</td>
                                </tr>
                                <tr>
                                    <td colspan="3">
                                        <button class="layui-btn layui-btn-sm layui-btn-primary" @click="get_trade_list()" style="width:100%">刷新</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import {
    accounts_url,
    zones_url,
    coins_url,
    get_balance_url,
    get_trade_list30_url,
    gat_flush_make_order_url,
    gat_flush_logs_url,
    tool
} from '@/config.js'
import fetch from '@/fetch.js'

export default {

    data: function(){
        return {
            accounts: [],
            account_one: {},
            account_two: {},
            zones: [],
            zone: {},
            coins: [],
            coin: {},

            account_one_balance_zone: 0,
            account_one_balance_coin: 0,
            account_two_balance_zone: 0,
            account_two_balance_coin: 0,

            buy_str: [],
            sell_str: [],
            trade_list_index: 0,

            price: 0,
            amount: 0,
            sum: 0,

            gat_flush_logs: []

        }
    },
    methods: {
        init_data: function(){
            fetch.get(accounts_url).then(res => { this.accounts = _.filter(res.data, item => { return !item.is_api })})
            fetch.get(zones_url).then(res => { this.zones = res.data })
            this.zone = tool.get_storage_obj('zone') || {}
            this.coin = tool.get_storage_obj('coin') || {}
            this.account_one = tool.get_storage_obj('account_one') || {}
            this.account_two = tool.get_storage_obj('account_two') || {}
            if(this.zone.id){
                this.fetch_coin(this.zone.id)
            }
            if(this.account_one.id && this.zone.id && this.coin.id){
                this.get_trade_list()
                this.trade_list_index = setInterval(this.get_trade_list, 1000*4)
            }
            this.get_gat_flush_logs()
        },
        refresh_form: function() {
            layui.use("form", function() {
                var form = layui.form
                form.render()
            });
        },
        get_balance: function(account_id, is_one){
            layer.load()
            var url = get_balance_url + '/' + account_id
            fetch.get(url).then(res => {
                for(var item in res.data){
                    var balance_zone = this.zone.name.toLowerCase() + '_balance'
                    var balance_coin = this.coin.name.toLowerCase() + '_balance'

                    if(item == balance_zone && is_one){
                        this.account_one_balance_zone = res.data[item]
                    }
                    if(item == balance_coin && is_one)
                        this.account_one_balance_coin = res.data[item]
                    if(item == balance_zone && !is_one)
                        this.account_two_balance_zone = res.data[item]
                    if(item == balance_coin && !is_one)
                        this.account_two_balance_coin = res.data[item]
                }
                layer.closeAll()
            })
        },
        get_trade_list: function(){
            var url = get_trade_list30_url + '/' + this.account_one.id
            fetch.post(url, {'zone': this.zone.name, 'coin': this.coin.name}).then(res => {
                // console.log(res.data)
                this.sell_str = _.reverse(_.take(res.data.sellStr, 10))
                this.buy_str = _.take(res.data.buyStr, 10)
            })
        },
        fetch_coin: function(zone_id) {
            fetch.get(coins_url).then(res => {
                this.coins = _.filter(res.data, function(item) {
                    return item.zone_id == zone_id
                })
            })
        },  
        get_price: function(price){
            this.price = price
        },
        make_order: function(come_from){
            layer.load()
            if(this.zone.id && this.coin.id && this.account_one.id && this.account_two.id){
                fetch.post(gat_flush_make_order_url, {
                    'account_one_id': this.account_one.id,
                    'account_two_id': this.account_two.id,
                    'zone': this.zone.name,
                    'coin': this.coin.name,
                    'price': this.price,
                    'amount': this.amount,
                    'come_from': come_from,
                }).then(res => {
                    layer.closeAll()
                    layer.msg(res.data)
                    this.get_gat_flush_logs()
                }).catch(err => {
                    layer.closeAll()
                    layer.msg(err.message)
                })
            }
        },
        get_gat_flush_logs: function(){
            fetch.get(gat_flush_logs_url).then(res => {
                this.gat_flush_logs = res.data
            })
        }
    },
    watch: {
        accounts: function(){ 
            this.$nextTick(function(){
                this.refresh_form()
            })
        },
        zones: function(){ 
            this.$nextTick(function(){
                this.refresh_form()
            })
        },
        coins: function(){ 
            this.$nextTick(function(){
                this.refresh_form()
            })
        },
        price: function(){
            this.sum = _.round(this.price * this.amount, 6)
        },
        amount: function(){
            this.sum = _.round(this.price * this.amount, 6)
        }
    },
    mounted() {
        var _this = this
        this.$nextTick(function(){
            layui.use('form', function(){
                var form = layui.form
                form.on('select(account-one)', function(data){
                    _this.account_one = _.find(_this.accounts, item => { return item.id == data.value })
                    tool.write_storage_obj('account_one', _this.account_one)
                })
                form.on('select(account-two)', function(data){
                    _this.account_two = _.find(_this.accounts, item => { return item.id == data.value })
                    tool.write_storage_obj('account_two', _this.account_two)
                })
                form.on('select(zone)', function(data){
                    _this.coins = _this.fetch_coin(data.value)
                    _this.zone = _.find(_this.zones, item => {return item.id == data.value})
                    tool.write_storage_obj('zone', _this.zone)
                })
                form.on('select(coin)', function(data){
                    console.log(data.value)
                    _this.coin = _.find(_this.coins, item => {return item.id == data.value})
                    tool.write_storage_obj('coin', _this.coin)
                })
                form.render()
            })

            layui.use('layer', function(){
                var layer = layui.layer
            })
            this.init_data()
        })
        
    },
    beforeDestroy() {
        clearInterval(this.trade_list_index)
    },
    
}
</script>

<style scoped>

</style>


