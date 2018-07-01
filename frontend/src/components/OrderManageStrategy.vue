<template>
<div>
    <blockquote class="layui-elem-quote"><h2>策略挂单</h2></blockquote>
    <div class="layui-form">
    <table class="layui-table">
        <colgroup>
            <col width="80">
            <col width="200">
            <col width="80">
            <col width="200">
            <col width="60">
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
        <tr>
            <td colspan="4">
                <input type="checkbox" v-model="filter.is_strategy_complete" title="已完成" lay-filter="is_strategy_complete">
                <input type="checkbox" v-model="filter.is_cancel" title="已撤单" lay-filter="is_cancel">
                <input type="radio" name="trade_type" value="1" title="买入" v-model="filter.trade_type" lay-filter="trade_type">
                <input type="radio" name="trade_type" value="2" title="卖出" v-model="filter.trade_type"  lay-filter="trade_type">
                <input type="radio" name="trade_type" value="0" title="全部" v-model="filter.trade_type"  lay-filter="trade_type">
            </td>
            <td>时间</td>
            <td>
                <div class="layui-inline">
                    <input type="text" class="layui-input" id="date_start" v-model="filter.date_start">
                </div>
                <div class="layui-inline">
                    <input type="text" class="layui-input" id="date_end" v-model="filter.date_end">
                </div>
                <div class="layui-inline">
                    <button class="layui-btn" @click="get_orders()">刷新</button>
                </div>
            </td>
        </tr>
    </table>
    </div>
    <table class="layui-table">
        <tr>
            <td>总共 {{this.orders.count || 0}} 条</td>
            <td>最低价 {{this.orders.min_price || 0}}</td>
            <td>最高价 {{this.orders.max_price || 0}}</td>
            <td>总金额 {{this.orders.money_sum || 0}}</td>
        </tr>
    </table>
    <table class="layui-table">
        <colgroup>
            <col width="80">
            <col width="100">
            <col width="100">
            <col width="100">
            <col width="100">
            <col width="120">
            <col width="200">
            <col width="">
        </colgroup>
        <thead>
            <tr>
                <th>Id</th>
                <th>单号</th>
                <th>类型</th>
                <th class="load_more" @click="sort_price()">
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
            <tr v-for="item in orders.data" :key="item.id" :class="{buy_color: item.trade_type == '1',sell_color: item.trade_type == '2'}">
                <td>{{item.id}}</td>
                <td>{{item.number}}</td>
                <td>{{item.trade_type | buy-sell}}</td>
                <td>{{item.price}}</td>
                <td>{{item.amount}}</td>
                <td>{{(item.price * item.amount).toFixed(5)}}</td>
                <td>{{item.create_at}}</td>
                <td>
                    <button v-if="!item.is_strategy_complete && item.number && !item.is_cancel" class="layui-btn layui-btn-primary" @click="cancel_order(item.id)">撤单</button>
                </td>
            </tr>
        </tbody>        
    </table>
    <table class="layui-table">
        <tr>
            <td colspan="3" class="load_more" @click="load_more_pre">上一页</td>
            <td colspan="2" class="load_more">第 {{page+1}} 页</td>
            <td colspan="3" class="load_more" @click="load_more_next">下一页</td>
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
    order_logs_url,
    cancel_order_url,
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

            filter: {
                is_strategy_complete: false,
                trade_type: 0,
                date_start: '',
                date_end: '',
            },

            orders:[],
            page: 0,
            sort_d:true
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
            this.account = tool.get_storage_obj('account') || {}
            this.zone = tool.get_storage_obj('zone') || {}
            this.coin = tool.get_storage_obj('coin') || {}
            this.filter = tool.get_storage_obj('filter') || this.filter
            if(this.zone.id){
                this.fetch_coin(this.zone.id)
            }
            if(this.zone.id && this.coin.id && this.account.id){
                this.get_orders()
            }
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
                form.render()
            });
        },
        load_more_next: function(){
            if(this.page < parseInt(this.orders.count/20))
                this.page += 1
            this.get_orders()
        },
        load_more_pre: function(){
            this.page -= 1
            if(this.page<0)
                this.page = 0
            this.get_orders()
        },
        get_orders:function(){
            var index = layer.load()
            fetch.post(order_logs_url, Object.assign({
                'account_id': this.account.id,
                'zone_name': this.zone.name,
                'coin_name': this.coin.name,
                'page': this.page,
            },this.filter)).then(res => {
                this.orders = _.reverse(res.data)
                layer.close(index)
            })
        },
        cancel_order: function(id){
            var index = layer.load()
            var url = cancel_order_url + '/' + id
            fetch.get(url).then(res => {
                layer.close(index)
                layer.msg(res.data)
                this.get_orders()
            })
        },
        sort_price:function(){
            if(this.sort_d){
                this.orders.data = _.sortBy(this.orders.data, function(item){ return item.price  })
                this.sort_d = false
            }else{
                this.orders.data = _.sortBy(this.orders.data, function(item){ return -item.price  })
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
        this.$nextTick(function(){
            var _this = this    
            layui.use('form', function(){
                var form = layui.form    
                form.on("select(select-account)", function(data) {
                    _this.account = _.find(_this.accounts, function(item){return item.id == data.value})
                    tool.write_storage_obj('account', _this.account)
                });            
                form.on("select(select-zone)", function(data) {
                    _this.zone = _.find(_this.zones, function(item){return item.id == data.value})
                    _this.coin.id = 0
                    _this.fetch_coin(data.value)
                    tool.write_storage_obj('zone', _this.zone)
                });
                form.on("select(select-coin)", function(data) {
                    _this.coin = _.find(_this.coins, function(item){return item.id == data.value})
                    _this.get_orders()
                    tool.write_storage_obj('coin', _this.coin)
                });
                form.on('checkbox(is_strategy_complete)', function(data){
                    _this.filter.is_strategy_complete = data.elem.checked //是否被选中，true或者false
                   tool.write_storage_obj('filter', _this.filter)
                    _this.get_orders()
                }); 
                form.on('checkbox(is_cancel)', function(data){
                    _this.filter.is_cancel = data.elem.checked //是否被选中，true或者false
                   tool.write_storage_obj('filter', _this.filter)
                    _this.get_orders()
                }); 
                form.on('radio(trade_type)', function(data){
                    _this.filter.trade_type = data.value
                    tool.write_storage_obj('filter', _this.filter)
                    _this.get_orders()
                });  
            })
            layui.use('layer', function(){
                var layer = layui.layer
            })
            layui.use('laydate', function(){
                var laydate = layui.laydate;
                //执行一个laydate实例
                laydate.render({
                    elem: '#date_start', 
                    done: function(value){
                        _this.filter.date_start = value
                    }
                });
                laydate.render({
                    elem: '#date_end',
                    done: function(value){
                        _this.filter.date_end = value
                    }
                });
            });
            
            this.init_data()        
        })
    }
    
}
</script>

<style scoped>
.sell_color{color: #FF5722}
.buy_color{color: #01AAED}
.load_more{text-align:center; cursor: pointer;}
</style>

