<template>
<div>
    <blockquote class="layui-elem-quote"><h2>AEX网站挂单 - 非api操作</h2></blockquote>
    <div class="layui-form">
        <table class="layui-table">
            <colgroup>
                <col width="100">
                <col width="200">
                <col width="100">
                <col width="200">
                <col width="100">
                <col width="">
            </colgroup>
            <tr>
                <td>账户</td>
                <td>
                    <select id="account" v-model="account.id" lay-filter="select-account">
                        <option v-for="item in accounts" :key="item.id" :value="item.id">{{item.name}}</option>
                    </select>
                </td>
                <td>交易区</td>
                <td>
                    <select id="zone" v-model="zone.id" lay-filter="select-zone">
                        <option v-for="item in zones" :key="item.id" :value="item.id">{{item.name}}</option>
                    </select>
                </td>
                <td>币种</td>
                <td>
                    <select id="coin" v-model="coin.id" lay-filter="select-coin">
                        <option v-for="item in coins" :key="item.id" :value="item.id">{{item.name}}</option>
                    </select>
                </td>
            </tr>
        </table>

        <table class="layui-table">
            <tr>
                <td>
                    <input type="radio" name="trade_type" value="1" title="买入" lay-filter="trade_type">
                    <input type="radio" name="trade_type" value="2" title="卖出" lay-filter="trade_type">
                    <input type="radio" name="trade_type" value="0" title="全部" lay-filter="trade_type">
                </td>
            </tr>
        </table>
    </div>

    <table class="layui-table">
        <colgroup>
            <col width="100">
            <col width="80">
            <col width="120">
            <col width="120">
            <col width="150">
            <col width="200">
            <col width="">
        </colgroup>
        <thead>
            <tr>
                <th>Id</th>
                <th>类型</th>
                <th @click="sort_price()">
                    价格
                    <i class="layui-icon layui-icon-triangle-d"></i>
                </th>
                <th>数量</th>
                <th>总价</th>
                <th>时间</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in orders" :key="item.id" :class="{sell_color: item.type == '2', buy_color: item.type == '1'}">
                <td>{{item.id}}</td>
                <td>{{item.type | buy-sell}}</td>
                <td>{{item.price}}</td>
                <td>{{item.amount}}</td>
                <td>{{(item.price * item.amount).toFixed(6)}}</td>
                <td>{{item.time}}</td>
                <td>
                    <button class="layui-btn layui-btn-primary" @click="cancel_order(item.id)">撤单</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>    
</template>


<script>
import fetch from '@/fetch.js'

import {
    accounts_url,
    zones_url,
    coins_url,
    get_order_list_url,
    cancel_order_with_trade_url
} from '@/config.js'

export default {
    data: function(){
        return {
            accounts: [],
            account: {},
            zones: [],
            zone: {},
            coins: [],
            coin: {},

            old_orders: [],
            orders:[],
            sort_d:true
        }
    },
    methods: {
        init_data: function(){
            fetch.get(accounts_url).then(res => {
                this.accounts = _.filter(res.data, item=>{return !item.is_api})
            })
            fetch.get(zones_url).then(res => {
                this.zones = res.data
            })
        },
        fetch_coin: function(zone_id) {
            fetch.get(coins_url).then(res => {
                this.coins = _.filter(res.data, function(item) {
                    return item.zone_id == zone_id
                })
            })
        },  
        refresh_form: function() {
            layui.use("form", function() {
                var form = layui.form
                form.render('select')
            });
        },
        get_orders:function(){
            var index = layer.load()
            fetch.post(get_order_list_url, {
                'account_id': this.account.id,
                'zone': this.zone.name,
                'coin': this.coin.name
            }).then(res => {
                this.old_orders = this.orders = _.reverse(res.data)
                layer.close(index)
            })
        },
        cancel_order:function(order_id){
            var index = layer.load()
            var params = {
                'order_id': order_id,
                'zone': this.zone.name,
                'coin': this.coin.name,
                'account_id': this.account.id
            }
            fetch.post(cancel_order_with_trade_url, params).then(res=>{            
                layer.close(index)
                layer.msg(res.data)
                this.get_orders()    
            })
        },
        sort_price:function(){
            if(this.sort_d){
                this.orders = _.sortBy(this.orders, function(item){ return item.price  })
                this.sort_d = false
            }else{
                this.orders = _.sortBy(this.orders, function(item){ return -item.price  })
                this.sort_d = true
            }
        }
    },
    watch: {
        coins: function() {
            this.$nextTick(function() {
                this.refresh_form()
            });
        },
        accounts: function() {
            this.$nextTick(function() {
                this.refresh_form()
            });
        },
        zones: function() {
            this.$nextTick(function() {
                this.refresh_form()
            });
        },
    },
    mounted: function(){
        this.init_data()
        var _this = this
        this.$nextTick(function(){
            layui.use('form', function(){
                var form = layui.form    
                form.on("select(select-account)", function(data) {
                    _this.account = _.find(_this.accounts, function(item){return item.id == data.value})
                });            
                form.on("select(select-zone)", function(data) {
                    _this.zone = _.find(_this.zones, function(item){return item.id == data.value})
                    _this.coin.id = 0
                    _this.fetch_coin(data.value)
                });
                form.on("select(select-coin)", function(data) {
                    _this.coin = _.find(_this.coins, function(item){return item.id == data.value})
                    _this.get_orders()
                });
                form.on('radio(trade_type)', function(data){
                    if(data.value == 0)
                        _this.orders = _this.old_orders
                    else
                        _this.orders = _.filter(_this.old_orders, item=>{return item.type == data.value})
                });  
                form.render()
            })
            layui.use('layer', function(){
                var layer = layui.layer
            })
            
        })
    }
    
}
</script>

<style scoped>
.sell_color{color: #FF5722}
.buy_color{color: #01AAED}
</style>

