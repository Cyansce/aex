<template>
    <div>
        <blockquote class="layui-elem-quote"><h2>API挂单</h2></blockquote>


        <!-- <button class="layui-btn" @click="test()">测试</button> -->

        <div class="layui-form">
            <table class="layui-table">
                <tr>
                    <td>账户</td>
                    <td>
                        <select id="account" v-model="account.id" lay-filter="select-account">
                            <option v-for="item in accounts" :key="item.id" :value="item.id">{{item.name}}</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>交易区</td>
                    <td>
                        <select id="zone" v-model="zone.id" lay-filter="select-zone">
                            <option v-for="item in zones" :key="item.id" :value="item.id">{{item.name}}</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>币种</td>
                    <td>
                        <select id="coin" v-model="coin.id" lay-filter="select-coin">
                            <option v-for="item in coins" :key="item.id" :value="item.id">{{item.name}}</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>当前价格</td>
                    <td>
                        <div class="layui-col-xs2">
                            <input type="text" class="layui-input" v-model="ticker.buy" placeholder="买" readonly @click="get_price(ticker.buy)">
                        </div>
                        <div class="layui-col-xs2">
                            <input type="text" class="layui-input" v-model="ticker.sell" placeholder="卖" readonly @click="get_price(ticker.sell)">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>挂单价格</td>
                    <td>
                        <input type="text" class="layui-input" v-model="price">
                    </td>
                </tr>
                <tr>
                    <td>数量</td>
                    <td>
                        <input type="text" class="layui-input" v-model="amount">
                    </td>
                </tr>
                <tr>
                    <td>差价</td>
                    <td>
                        <input type="text" class="layui-input" v-model="percent">
                    </td>
                </tr>
                <tr>
                    <td>挂单条数</td>
                    <td>
                        <input type="text" class="layui-input" v-model="order_amount">
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <button class="layui-btn layui-btn-primary" @click="open_wrapper(1)">预览买单</button>
                        <button class="layui-btn">开始挂买单</button>
                        <button class="layui-btn layui-btn-primary" @click="open_wrapper(2)">预览卖单</button>
                        <button class="layui-btn">开始挂卖单</button>
                    </td>
                </tr>
            </table>

        </div>

        <div id="wrapper">
            <table class="layui-table">
                <colgroup>
                    <col width="80">
                    <col width="100">
                    <col width="100">
                    <col width="">
                </colgroup>
                <thead>
                    <tr>
                        <th>类型</th>
                        <th>价格</th>
                        <th>数量</th>
                        <th>总价</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in previews" :key="item.id">
                        <td>{{preview_trade_type | buy-sell}}</td>
                        <td>{{item.price}}</td>
                        <td>{{item.amount}}</td>
                        <td>{{(item.price * item.amount).toFixed(6)}}</td>
                    </tr>
                    <tr>
                        <td colspan="3"></td>
                        <td>{{preview_sum}}</td>
                    </tr>
                    <tr v-if="previews.length > 0">
                        <td colspan="4">
                            <button v-if="preview_trade_type == 1" class="layui-btn" @click="start_make_order()">开始买挂单</button>
                            <button v-if="preview_trade_type == 2" class="layui-btn" @click="start_make_order()">开始卖挂单</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <table class="layui-table">
            <tr v-if="logs.length>0">
                <th>交易类型</th>
                <th>单价</th>
                <th>数量</th>
                <th>总价</th>
                <th>结果</th>
            </tr>
            <tr v-for="item in logs" :key="item.id">
                <td>{{item.trade_type}}</td>
                <td>{{item.price}}</td>
                <td>{{item.amount}}</td>
                <td>{{(item.price*item.amount).toFixed(6)}}</td>
                <td>{{item.res_data}}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import fetch from '@/fetch.js'

import {
    accounts_url,
    zones_url,
    coins_url,
    ticker_url,
    strategy_api_order_url,
    tool
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

            ticker: {},
            price: 0,
            amount: 0,
            percent: 0.003,
            order_amount: 50,

            previews: [],
            preview_trade_type: 0,
            preview_sum: 0,

            logs: []
        }
    },
    methods: {
        init_data: function(){
            fetch.get(accounts_url).then(res => {
                this.accounts = res.data
            })
            fetch.get(zones_url).then(res => {
                this.zones = res.data
            })
        },
        open_wrapper: function(type){
            this.previews = []
            this.preview_trade_type = type
            if(type == 1){
                for(var i=0;i<this.order_amount;i++){
                    this.previews.push({
                        price: _.round(_.multiply(this.price, _.subtract(1, _.multiply(i,this.percent))), this.coin.point),
                        amount: this.amount                        
                    })
                }
            }
            if(type == 2){
                for(var i=0;i<this.order_amount;i++){
                    this.previews.push({
                        price: _.round(_.multiply(this.price, _.add(1, _.multiply(i,this.percent))), this.coin.point),
                        amount: this.amount                        
                    })
                }
            }
            this.preview_sum = _.sumBy(this.previews, function(item){return item.price * item.amount})
            layer.open({
                title: '预览',
                type: 1, 
                content: $('#wrapper'),
                area: ['500','600px']
            })
        },     
        refresh_form: function() {
            layui.use("form", function() {
                var form = layui.form
                form.render()
            });
        },
        fetch_coin: function(zone_id) {
            fetch.get(coins_url).then(res => {
                this.coins = _.filter(res.data, function(item) {
                    return item.zone_id == zone_id
                })
            })
        },
        get_price: function(price) {
            this.price = price
        },
        get_ticker: function(coin_id) {
            if (coin_id == 0) return;
                fetch.post(ticker_url, { coin_id: coin_id }).then(res => {
                this.ticker = res.data.ticker;
            });
        },

        start_make_order: function(){
            layer.load(0, {time: 10*1000})
            var count = 0
            if(this.previews.length > 0 && this.price > 0 && this.amount > 0){
                for(var item in this.previews){                    
                    var params = {
                        'zone': this.zone.name, 
                        'coin': this.coin.name,
                        'account_id': this.account.id,
                        'trade_type': this.preview_trade_type,
                        'price': this.previews[item].price,
                        'amount': this.previews[item].amount
                    }
                    console.log(count)
                    fetch.post(strategy_api_order_url,params).then(res => {
                        var param = JSON.parse(res.config.data)
                        this.logs.push({
                            'price': param.price,
                            'amount': param.amount,
                            'trade_type': param.trade_type,
                            'res_data': res.data
                            })
                        count++
                        if(count == this.previews.length){
                            layer.closeAll()
                        }
                    })
                }
            }
            
        },
        test: function(){
            for(var item in this.previews){
                tool.sleep(200)
                console.log(item)
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
                    _this.get_ticker(data.value)
                });
            })
            layui.use('layer', function(){
                var layer = layui.layer
            })
            
        })
    }
}
</script>

<style scoped>
.layui-table{ width: 500px}
.layui-col-xs2{ width: 150px;}
#wrapper{display: none}
</style>
