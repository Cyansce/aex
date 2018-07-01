<template>
<div>
    <blockquote class="layui-elem-quote"><h2>KEY</h2></blockquote>

    <button class="layui-btn" v-on:click="open_wrapper('add')">新增</button>

    <div class="layui-card" v-for="item in api_accounts" :key="item.id">
        <div class="layui-card-header">{{item.name}}</div>
            <div class="layui-card-body">
                <table class="layui-table">
                    <colgroup>
                        <col width="100">
                        <col width="">
                    </colgroup>
                    <tr>
                        <td>key</td>
                        <td>{{item.key}}</td>
                    </tr>
                    <tr>
                        <td>skey</td>
                        <td>{{item.skey}}</td>
                    </tr>
                    <tr>
                        <td>userid</td>
                        <td>{{item.user_id}}</td>
                    </tr>
                    <tr>
                        <td colspan="2">
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
                        <td>Name</td>
                        <td>
                            <input type="text" v-model="edit_api_account.name" lay-verify="required" placeholder="name" autocomplete="off" class="layui-input">                      
                        </td>
                    </tr>
                    <tr>
                        <td>Key</td>
                        <td>
                            <input type="text" v-model="edit_api_account.key" lay-verify="required" placeholder="key" autocomplete="off" class="layui-input">                      
                        </td>
                    </tr>
                    <tr>
                        <td>SKey</td>
                        <td>
                            <input type="text" v-model="edit_api_account.skey" lay-verify="required" placeholder="skey" autocomplete="off" class="layui-input">                            
                        </td>
                    </tr>
                    <tr>
                        <td>UserID</td>
                        <td>
                            <input type="text" v-model="edit_api_account.user_id" lay-verify="required" placeholder="userid" autocomplete="off" class="layui-input">                          
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
import { api_accounts_url, add_api_account_url, del_api_account_url } from '@/config.js'
import fetch from '@/fetch.js'

var _ = require('lodash')

export default {
    data: function(){
        return {
            api_accounts: [],
            edit_api_account: {
                name: '',
                key: '',
                skey: '',
                user_id: '',
            }
            
        }
    },
    methods: {
        init_data: function(){
            fetch({
                url: api_accounts_url,                
            }).then(res => {
                this.api_accounts = res.data
            })

        },
        open_wrapper: function(){
            layer.open({
                title: 'api密鑰',
                type: 1, 
                content: $('#card-wrapper'),
                area: ['500px','400px']
            })
        },
        sumbit_wrapper: function(){
            fetch({
                method: 'post', 
                url: add_api_account_url,
                data: this.edit_api_account
            }).then(res => {
                this.api_accounts.push(res.data)
                this.api_accounts = _.sortBy(this.api_accounts, function(item){return -item.id})
                this.closeAll()
            })
        },
        del: function(id){
            var url = del_api_account_url + '/' + id
            fetch({
                url: url
            }).then(res=>{
                if(res.data == 'succ'){
                    this.api_accounts = _.difference(this.api_accounts, _.remove(this.api_accounts, function(item){return item.id == id}))
                }
            })

        },
        closeAll: function(){
            layer.closeAll()
        }
    },
    mounted: function(){
        layui.use('layer', function(){
            var layer = layui.layer
        })
        this.init_data()
    }
}
</script>

<style scoped>
.layui-card{margin: 20px 0 20px 0}
#card-wrapper{display: none}
.layui-layer-wrap{padding: 20px;}
</style>

