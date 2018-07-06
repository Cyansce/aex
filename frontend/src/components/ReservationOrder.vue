<template>
    <div>
        <blockquote class="layui-elem-quote"><h2>预约挂单</h2></blockquote>

        <div class="layui-form">
            <table class="layui-table" style="width:500px;">
                <colgroup>
                    <col width="120">
                    <col width="">
                </colgroup>
                <tr>
                    <td>账户</td>
                    <td>
                        <select name="account" v-model="account.id" lay-filter="account-select">
                            <option v-for="item in accounts" :key="item.id" :value="item.id">{{item.name}}</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>交易区</td>
                    <td>
                        <select name="zone" v-model="zone.id" lay-filter="zone-select">
                            <option v-for="item in zones" :key="item.id" :value="item.id">{{item.name}}</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>币种</td>
                    <td>
                        <select name="coin" v-model="coin.id" lay-filter="coin-select">
                            <option v-for="item in coins" :key="item.id" :value="item.id">{{item.name}}</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>当前价格</td>
                    <td>
                        <div class="layui-inline">
                        <input type="text" class="layui-input layui-inline" v-model="ticker.buy" placeholder="买" readonly @click="get_price(ticker.buy)">
                        </div>
                        <div class="layui-inline">
                        <input type="text" class="layui-input" v-model="ticker.sell" placeholder="卖" readonly @click="get_price(ticker.sell)">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>挂单价格</td>
                    <td>
                        <input type="text" v-model="price" class="layui-input">
                    </td>
                </tr>
                <tr>
                    <td>数量</td>
                    <td>
                        <input type="text" v-model="amount" class="layui-input">
                    </td>
                </tr>
                <tr>
                    <td>总价</td>
                    <td>
                        <input type="text" readonly v-model="sum" class="layui-input">
                    </td>
                </tr>
                <tr>
                    <td>预约价格</td>
                    <td>
                        <input type="text" class="layui-input" v-model="reservation_price">
                    </td>
                </tr>
                <tr>
                    <td>预约总价</td>
                    <td>
                        <input type="text" class="layui-input" v-model="reservation_sum">
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <button class="layui-btn" style="width:220px" @click="open_wrapper(1)">买入</button>
                        <button class="layui-btn layui-btn-danger" style="width:220px" @click="open_wrapper(2)">卖出</button>
                    </td>
                </tr>

            </table>
        </div>

        <div class="" id="reservation-logs">
            <table class="layui-table">
                <colgroup>
                    <col width="">
                </colgroup>
                <thead>
                    <tr>
                        <td>Id</td>
                        <td>Number</td>
                        <td>类型</td>
                        <td>价格</td>
                        <td>数量</td>
                        <td>总价</td>
                        <td>预约价格</td>
                        <td>预计盈利</td>
                        <td>状态</td>
                        <td>操作</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in reservation_orders" :key="item.id">
                        <td>{{ item.id }}</td>
                        <td>{{ item.number }}</td>
                        <td>{{ item.trade_type | buy-sell }}</td>
                        <td>{{ item.price }}</td>
                        <td>{{ item.amount }}</td>
                        <td>{{ (item.amount * item.price).toFixed(6) }}</td>
                        <td>{{ item.reservation_price }}</td>
                        <td v-if="item.trade_type == 1">{{ ((item.reservation_price - item.price) * item.amount).toFixed(6) }}</td>
                        <td v-if="item.trade_type == 2">{{ ((item.price - item.reservation_price) * item.amount).toFixed(6) }}</td>
                        <td>{{ item.is_cancel ? '已取消' : item.is_complete ? '已完成' : '挂单中' }}</td>
                        <td>
                            <div v-if="!item.is_cancel && !item.is_complete">
                                <button class="layui-btn layui-btn-primary" @click="cancel_order(item.id)">取消</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div id="wrapper">
            <table class="layui-table">
                <colgroup>
                    <col width="150px">
                    <col width="150px">
                    <col width="150px">
                </colgroup>
                <thead>
                    <tr>
                        <th></th>
                        <th>原始</th>
                        <th>预约</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>交易类型</td>
                        <td>{{trade_type==1 ? '买': '卖'}}</td>
                        <td>{{trade_type==2 ? '买': '卖'}}</td>
                    </tr>
                    <tr>
                        <td>价格</td>
                        <td>{{this.price}}</td>
                        <td>{{this.reservation_price}}</td>
                    </tr>
                    <tr>
                        <td>数量</td>
                        <td>{{this.amount}}</td>
                        <td>{{this.amount}}</td>
                    </tr>
                    <tr>
                        <td>总价</td>
                        <td>{{(this.price*this.amount).toFixed(6)}}</td>
                        <td>{{(this.reservation_price*this.amount).toFixed(6)}}</td>
                    </tr>
                    <tr style="background:#FFB800">
                        <td>预计盈利</td>
                        <td colspan="2">
                            <div v-if="trade_type==1">
                                {{((this.reservation_price*this.amount).toFixed(6) -  (this.price*this.amount).toFixed(6)).toFixed(6)}}
                            </div>
                            <div v-if="trade_type==2">
                                {{((this.price*this.amount).toFixed(6) -  (this.reservation_price*this.amount).toFixed(6)).toFixed(6)}}
                            </div>
                            
                        </td>
                    </tr>
                    <tr>
                        <td colspan="3">
                            <div v-if="trade_type==1">
                                <button class="layui-btn" style="width:330px" @click="make_order()">买入</button>
                            </div>
                            <div v-if="trade_type==2">
                                <button class="layui-btn layui-btn-danger" style="width:330px" @click="make_order()">卖出</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import fetch from '@/fetch.js'

import {
    accounts_url,
    zones_url,
    coins_url,
    ticker_url,
    reservation_orders_url,
    add_reservation_order_url,
    cancel_reservation_order_url,
    tool
} from '@/config.js'

export default {

    data: function(){
        return {
            accounts:[],
            account:{},
            zones:[],
            zone:{},
            coins:[],
            coin:{},
            ticker: {},

            price: 0,
            amount: 0,
            sum: 0,
            trade_type: '',

            reservation_price: 0,
            reservation_sum: 0,

            reservation_orders: []
        }
    },
    methods: {
        init_data:function(){
            fetch.get(accounts_url).then(res=>{this.accounts=res.data})
            fetch.get(zones_url).then(res=>{this.zones=res.data})
            this.account = tool.get_storage_obj('s_account') || {}
            this.zone = tool.get_storage_obj('s_zone') || {}
            if (this.zone.id){
                this.fetch_coin(this.zone.id)
            }
            this.coin = tool.get_storage_obj('s_coin') || {}
            if (this.coin.id){
                this.get_ticker(this.coin.id)
            }
            this.get_reservation_orders()
        },
        refresh_form:function(){
            // layui.form.render()
            layui.use('form', function(){
                var form = layui.form
                form.render()
            })
        },
        fetch_coin:function(zone_id){
            fetch.get(coins_url).then(res=>{
                this.coins = _.filter(res.data, item => {return item.zone_id == zone_id})
            })
        },
        get_ticker: function(coin_id) {
            if (coin_id == 0) return;
            layer.load()
            fetch.post(ticker_url, { coin_id: coin_id }).then(res => {
                layer.closeAll()
                this.ticker = res.data.ticker;
            }).catch(error => {
                layer.closeAll()
                layer.msg(error.message)              
            });
        },
        get_price: function(price){
            this.price = price
            this.reservation_price = price
        },
        get_reservation_orders: function(){
            fetch.get(reservation_orders_url).then(res => {
                this.reservation_orders = res.data
            })
        },
        open_wrapper: function(trade_type){
            this.trade_type = trade_type
            layer.open({
                title: '预览',
                type: 1,
                content: $('#wrapper'),
                area: ['', '380px']
            })
        },
        preview_order: function(){

        },
        make_order: function(){
            var index = layer.load()
            if(!this.account.id || !this.zone.id || !this.coin.id || this.price <= 0 || this.reservation_price <= 0){
                return false
            }
            fetch.post(add_reservation_order_url, {
                'account_id': this.account.id,
                'zone_name': this.zone.name,
                'coin_name': this.coin.name,
                'price': this.price,
                'reservation_price': this.reservation_price,
                'amount' : this.amount,
                'trade_type': this.trade_type
            }).then(res => {
                layer.closeAll()
                layer.msg(res.data)
                this.get_reservation_orders()
            }).catch(error => {
                layer.closeAll()
                layer.msg(error.message)
            })


        },
        cancel_order: function(id){
            layer.load()
            var url = cancel_reservation_order_url + '/' + id
            fetch.post(url, {
                'account_id': this.account.id,
                'zone_name': this.zone.name,
                'coin_name': this.coin.name
            }).then(res => {
                layer.closeAll()
                layer.msg(res.data)
            }).catch(error => {
                layer.closeAll()
                layer.msg(error.message)
            })
        },
    },
    watch: {
        accounts: function(){ this.$nextTick(()=>{this.refresh_form()})},
        zones: function(){ this.$nextTick(()=>{this.refresh_form()}) },
        coins: function(){ this.$nextTick(()=>{this.refresh_form()}) },
        price: function(){ 
            this.sum = _.round(this.price * this.amount, 6)
            },
        amount: function(){ 
            this.sum = _.round(this.price * this.amount, 6)
            this.reservation_sum = _.round(this.reservation_price * this.amount, 6)
            },
        reservation_price: function(){
            this.reservation_sum = _.round(this.reservation_price * this.amount)
        }
    },
    mounted() {
        var _this = this
        layui.use('form', function(){
            var form = layui.form
            form.render()
            form.on('select(account-select)', data => {
                _this.account = _.find(_this.accounts, item => {return item.id == data.value})
                tool.write_storage_obj('s_account', _this.account)
            })
            form.on('select(zone-select)', data => {
                _this.zone = _.find(_this.zones, item => {return item.id == data.value})
                _this.coins = _this.fetch_coin(data.value)
                tool.write_storage_obj('s_zone', _this.zone)
            })
            form.on('select(coin-select)', data => {
                _this.coin = _.find(_this.coins, item => {return item.id == data.value})
                _this.get_ticker(_this.coin.id)
                tool.write_storage_obj('s_coin', _this.coin)
            })

        })
        this.init_data()
    },
    
}
</script>

<style scoped>
#wrapper{display: none}
</style>


