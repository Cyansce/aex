<template>
<div>
    <blockquote class="layui-elem-quote"><h2>循环挂单侧率数据修改</h2></blockquote>

    <button class="layui-btn" v-on:click="open_wrapper(0)">新增</button>

    <div class="layui-card" v-for="item in strategys" :key="item.id">
        <div class="layui-card-header">账户 -  {{item.account_name}}</div>
            <div class="layui-card-body">
                <table class="layui-table">
                    <colgroup>
                        <col width="120">
                        <col width="">
                    </colgroup>
                    <tr>
                        <td>交易区</td>
                        <td>{{item.zone_name}}</td>
                    </tr>
                    <tr>
                        <td>币种</td>
                        <td>{{item.coin_name}}</td>
                    </tr>
                    <tr>
                        <td>百分比</td>
                        <td>{{item.percent}}</td>
                    </tr>
                    <tr>
                        <td>小数点</td>
                        <td>{{item.point}}</td>
                    </tr>
                    <tr>
                        <td>最大金额</td>
                        <td>{{item.max_price}}</td>
                    </tr>
                    <tr>
                        <td>最小金额</td>
                        <td>{{item.min_price}}</td>
                    </tr>
                    <tr>
                        <td>开始时间</td>
                        <td>{{item.start_time}}</td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <button class="layui-btn" v-on:click="open_wrapper(item.id)">修改</button>
                            <button class="layui-btn layui-btn-primary" v-on:click="del(item.id)">刪除</button>
                        </td>
                    </tr>
                </table>
            </div>
    </div>

    <div id="card-wrapper">
        <form class="layui-form" onsubmit="return false">
            <table class="layui-table">
                <colgroup>
                        <col width="100">
                        <col width="">
                    </colgroup>
                    <tr>
                        <td>账户</td>
                        <td>
                            <select id="account" v-model="edit_strategy.account_id" lay-filter="select-account">
                                <option v-for="item in accounts" :key="item.id" :value="item.id">{{item.name}}</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>交易区</td>
                        <td>
                            <input type="text" v-model="edit_strategy.zone_name" lay-verify="required" placeholder="zone" autocomplete="off" class="layui-input">                      
                        </td>
                    </tr>
                    <tr>
                        <td>币种</td>
                        <td>
                            <input type="text" v-model="edit_strategy.coin_name" lay-verify="required" placeholder="coin" autocomplete="off" class="layui-input">                      
                        </td>
                    </tr>
                    <tr>
                        <td>百分比</td>
                        <td>
                            <input type="number" v-model="edit_strategy.percent" lay-verify="required" placeholder="percent" autocomplete="off" class="layui-input">                      
                        </td>
                    </tr>
                    <tr>
                        <td>小数点</td>
                        <td>
                            <input type="number" v-model="edit_strategy.point" lay-verify="required" placeholder="point" autocomplete="off" class="layui-input">                      
                        </td>
                    </tr>
                    <tr>
                        <td>最大金额</td>
                        <td>
                            <input type="text" v-model="edit_strategy.max_price" name="xxx" class="layui-input">
                        </td>
                    </tr>
                    <tr>
                        <td>最小金额</td>
                        <td>
                            <input type="text" v-model="edit_strategy.min_price" name="xxx" class="layui-input">
                        </td>
                    </tr>
                    <tr>
                        <td>开始时间</td>
                        <td>
                            <input type="text" id="start_time" v-model="edit_strategy.start_time" name="xxx" lay-filter="start_time" class="layui-input">
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <button class="layui-btn" v-on:click="sumbit_wrapper">提交</button>
                            <button class="layui-btn layui-btn-primary" v-on:click="closeAll">取消</button>
                        </td>
                    </tr>
            </table>
        </form>
    </div>
</div>    
</template>

<script>
import { 
    strategys_url,
    add_strategy_url,
    del_strategy_url,
    update_strategy_url,
    accounts_url,
} from '@/config.js'
import fetch from '@/fetch.js'

var _ = require('lodash')

export default {
    data: function(){
        return {
            strategys: [],
            accounts: [],        
            account: {},        
            edit_strategy: {},
        }
    },
    methods: {
        init_data: function(){
            fetch({
                url: strategys_url,                
            }).then(res => {
                this.strategys = res.data
            })

        },
        fetch_accounts:function(){                          
            fetch.get(accounts_url).then(res=>{
                this.accounts = res.data
            })
        },
        open_wrapper: function(id){
            this.fetch_accounts()
            if(id>0){
                this.edit_strategy = _.find(this.strategys, function(item){return item.id == id})
            }else{
                this.edit_strategy = {}
                this.edit_strategy.is_api = true
            }
            layer.open({
                title: '循环策略参数',
                type: 1, 
                content: $('#card-wrapper'),
                area: ['500px','700px']
            })
        },
        sumbit_wrapper: function(){
            layer.load()
            if(this.edit_strategy.id){
                var url = update_strategy_url + '/' + this.edit_strategy.id
                fetch.post(url, this.edit_strategy).then(res => {
                    this.init_data()
                    this.closeAll()
                    layer.msg(res.data)
                })
            }else{
                fetch({
                    method: 'post', 
                    url: add_strategy_url,
                    data: this.edit_strategy
                }).then(res => {
                    this.init_data()
                    this.closeAll()
                    layer.msg(res.data)
                })
            }
            
        },
        del: function(id){
            layer.load()
            var url = del_strategy_url + '/' + id
            fetch({
                url: url
            }).then(res=>{
                if(res.data == 'succ'){
                    this.init_data()
                    this.closeAll()
                    layer.msg(res.data)
                }
            })

        },
        closeAll: function(){
            layer.closeAll()
        },
        refresh_form: function(){            
            layui.use('form', function(){
                var form = layui.form
                form.render('select')
            })
        }
    },
    watch: {
        accounts: function(){
            this.$nextTick(function() {
                this.refresh_form()
            });
        }
    },
    mounted: function(){
        var _this = this
        _this.init_data()
        this.$nextTick(function(){
            layui.use('layer', function(){
                var layer = layui.layer
            })
            layui.use('form', function(){
                var form = layui.form     
                form.on("select(select-account)", function(data) {
                    _this.edit_strategy.account_id = data.value
                });  
            })
            layui.use('laydate', function(){
                var laydate = layui.laydate;
                //执行一个laydate实例
                laydate.render({
                    elem: '#start_time', 
                    type: 'datetime',
                    done: function(value){
                        _this.edit_strategy.start_time = value
                    }
                });
            });
        })
    }
}
</script>

<style scoped>
.layui-card{margin: 20px 0 20px 0}
#card-wrapper{display: none}
#gg_code_wrapper{display: none}
.layui-layer-wrap{padding: 20px;}
</style>

