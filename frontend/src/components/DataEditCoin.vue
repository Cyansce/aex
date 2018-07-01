<template>
    <div>
        <blockquote class="layui-elem-quote"><h2>币种区</h2></blockquote>

        <button class="layui-btn" v-on:click="open_wrapper('add')">新增</button>
        <hr>
        <table class="layui-table">
            <colgroup>
                <col width="100">
                <col width="100">
                <col width="100">
                <col width="200">
                <col>
            </colgroup>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>交易区</th>
                    <th>小数点</th>
                    <th>创建时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in coins" :key="item.id">
                    <td>{{item.name}}</td>
                    <td>{{item.zone_name}}</td>
                    <td>{{item.point}}</td>
                    <td>{{item.create_at}}</td>
                    <td>
                        <button disabled class="layui-btn" @click="open_wrapper('edit',item.id)">修改</button>
                        <button class="layui-btn" @click="del_coin(item.id)">删除</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div id="open-data-wrapper">
            <form class="layui-form" onsubmit="return false">
                <div class="layui-form-item">
                    <select v-model="zone_id" lay-filter="select">
                        <option v-for="item in zones" :key="item.id" :value="item.id">{{item.name}}</option>
                    </select>            
                </div>
                <div class="layui-form-item">
                    <input type="text" v-model="edit_coin.name" lay-verify="required" placeholder="币种名称" autocomplete="off" class="layui-input">                    
                </div>
                <div class="layui-form-item">
                    <input type="number" v-model="edit_coin.point" lay-verify="required" placeholder="小数点" autocomplete="off" class="layui-input">                    
                </div>
                <div class="layui-form-item">
                    <div class="layui-input-block">
                    <button class="layui-btn" v-on:click="wrapper_submit">提交</button>
                    <button class="layui-btn layui-btn-primary" v-on:click="closeAll">取消</button>
                    </div>
                </div>
            </form>
        </div>
    </div>    
</template>

<script>
import fetch from '@/fetch.js'
import {coins_url, add_coin_url, del_coin_url, zones_url} from '@/config.js'

var _ = require('lodash')

export default {
    data: function(){
        return {
            coins: [],
            edit_coin: {
                id:0,
                name: '',
                point: ''
            },
            zone_id: 0,
            zones: []
        }
    },
    watch:{
        zones: function(){
            this.$nextTick(function(){
                this.refresh_form()
            })
        }
    },
    methods: {
        init_data: function(){
            fetch({
                url: coins_url
            }).then(res => {
                this.coins = res.data
            })
            fetch({
                url: zones_url
            }).then(res => {
                this.zones = res.data
            })
        },
        open_wrapper: function(option, id=0){
            if(option == 'add'){
                this.edit_coin.name = ''
                this.edit_coin.id = 0
            }
            layer.open({
                type: 1, 
                content: $('#open-data-wrapper'),
                area: ['400px','300px']
            })
        },
        wrapper_submit: function(){
            fetch({
                method: 'post', 
                url: add_coin_url, 
                data: {'coin_name': this.edit_coin.name, 'zone_id': this.zone_id, 'point': this.edit_coin.point },
            }).then(res => {
                this.coins.push(res.data)
                this.coins = _.sortBy(this.coins, function(item){return -item.id})
                this.closeAll()
            })
        },
        del_coin: function(id){
            var url = del_coin_url + '/' + id
            fetch({
                url: url,                            
            }).then(res => {
                this.coins =_.difference(this.coins, _.remove(this.coins, (item)=>{return item.id == id}))
            })
        },
        closeAll: function(){
            layer.closeAll()
        },
        refresh_form: function(){
            layui.use("form", function() {
            var form = layui.form;
            form.render('select');
        });
        }

    },
    mounted: function(){
        var _this = this
        layui.use('layer', function(){
            var layer = layui.layer
        })
        layui.use("form", function() {
            var form = layui.form;
            form.render();

            form.on('select(select)', function(data){
                _this.zone_id = data.value
            }); 
        });
        this.init_data()
    }
}
</script>

<style scoped>
#open-data-wrapper {display: none}
.layui-layer-wrap{padding: 20px;}
</style>
