<template>
<div>
    <blockquote class="layui-elem-quote"><h2>交易账户</h2></blockquote>

    <button class="layui-btn" v-on:click="open_wrapper(0)">新增</button>

    <div class="layui-card" v-for="item in accounts" :key="item.id">
        <div class="layui-card-header">
            {{item.is_api? 'API账户': '非API账户'}} - {{item.name}}
        </div>
            <div class="layui-card-body">
                <table class="layui-table" v-if="item.is_api">
                    <colgroup>
                        <col width="120">
                        <col width="">
                    </colgroup>
                    <tr>
                        <td>Key</td>
                        <td>{{item.key}}</td>
                    </tr>         
                    <tr>
                        <td>SKey</td>
                        <td>{{item.skey}}</td>
                    </tr>         
                    <tr>
                        <td>UserID</td>
                        <td>{{item.user_id}}</td>
                    </tr> 
                    <tr>
                        <td colspan="2">
                            <button class="layui-btn layui-btn-primary" v-on:click="open_wrapper(item.id)">修改</button>
                            <button class="layui-btn layui-btn-primary" v-on:click="del(item.id)">刪除</button>
                        </td>
                    </tr>        
                </table>
                <table class="layui-table" v-if="!item.is_api">
                    <colgroup>
                        <col width="120">
                        <col width="">
                    </colgroup>
                    <tr>
                        <td>Email</td>
                        <td>{{item.email}}</td>
                    </tr>                    
                    <tr>
                        <td>Password</td>
                        <td>{{item.password}}</td>
                    </tr>
                    <tr>
                        <td>Md5</td>
                        <td>{{item.md5}}</td>
                    </tr>
                    <tr>
                        <td>Md5更新时间</td>
                        <td>{{item.update_md5_at}}</td>
                    </tr>
                    <tr>
                        <td>UserId</td>
                        <td>{{item.user_id}}</td>
                    </tr>
                    <tr>
                        <td>Url</td>
                        <td>{{item.url}}</td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <button class="layui-btn layui-btn-primary" v-on:click="open_wrapper(item.id)">修改</button>
                            <button class="layui-btn layui-btn-primary" v-on:click="del(item.id)">刪除</button>
                            <button class="layui-btn" v-on:click="login(item.id)">重新登录</button>
                            <button class="layui-btn layui-btn-warm" v-on:click="test_make_order(item.id, 'open')">测试交易</button>
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
                    <td>API ? </td>
                    <td v-show="!edit_account.id">
                        <input type="radio" name="is_api" value="1" title="是" v-model="is_api_show" lay-filter="is_api">
                        <input type="radio" name="is_api" value="0" title="否" v-model="is_api_show"  lay-filter="is_api">
                    </td>
                    <td v-show="edit_account.id">
                        {{edit_account.is_api? "API账户": "非API账户"}}
                    </td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td>
                        <input type="text" v-model="edit_account.name" lay-verify="required" placeholder="name" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
            </table>
            <table class="layui-table" v-show="is_api_show">
                <colgroup>
                    <col width="100">
                    <col width="">
                </colgroup>
                <tr>
                    <td>Key</td>
                    <td>
                        <input type="text" v-model="edit_account.key" lay-verify="required" placeholder="key" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
                <tr v-if="!edit_account.id">
                    <td>SKey</td>
                    <td>
                        <input type="text" v-model="edit_account.skey" lay-verify="required" placeholder="skey" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
                <tr>
                    <td>UserID</td>
                    <td>
                        <input type="text" v-model="edit_account.user_id" lay-verify="required" placeholder="user_id" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
            </table>
            <table class="layui-table" v-show="!is_api_show">
                <colgroup>
                    <col width="100">
                    <col width="">
                </colgroup>                
                <tr>
                    <td>Email</td>
                    <td>
                        <input type="text" v-model="edit_account.email" lay-verify="required" placeholder="email" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
                <tr v-if="!edit_account.id">
                    <td>Password</td>
                    <td>
                        <input type="password" v-model="edit_account.password" lay-verify="required" placeholder="password" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
                <tr>
                    <td>Md5</td>
                    <td>
                        <input type="text" v-model="edit_account.md5" lay-verify="required" placeholder="md5" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
                <tr>
                    <td>UserID</td>
                    <td>
                        <input type="text" v-model="edit_account.user_id" lay-verify="required" placeholder="user_id" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>
                <tr>
                    <td>url</td>
                    <td>
                        <input type="text" v-model="edit_account.url" lay-verify="required" placeholder="url" autocomplete="off" class="layui-input">                      
                    </td>
                </tr>                
            </table>
            <table class="layui-table">
                <tr>
                    <td colspan="2">
                        <button class="layui-btn" v-on:click="sumbit_wrapper">提交</button>
                        <button class="layui-btn layui-btn-primary" v-on:click="closeAll">取消</button>
                    </td>
                </tr>
            </table>
        </form>
    </div>
    <div id="gg_code_wrapper">
        <input type="text" v-model="gg_code" placeholder="" autocomplete="off" class="layui-input">   
        <hr>
        <button class="layui-btn" v-on:click="test_make_order(test_account_id)">提交</button>
        <button class="layui-btn layui-btn-primary" v-on:click="closeAll">取消</button>
    </div>
</div>    
</template>

<script>
import { 
    accounts_url,
    add_account_url,
    del_account_url,
    update_account_url,
    login_url,
    test_make_order_url
} from '@/config.js'
import fetch from '@/fetch.js'

var _ = require('lodash')

export default {
    data: function(){
        return {
            accounts: [],            
            edit_account: {},

            test_account_id: '',
            gg_code: '',
            is_api_show: true
        }
    },
    methods: {
        init_data: function(){
            fetch({
                url: accounts_url,                
            }).then(res => {
                this.accounts = res.data
            })

        },
        open_wrapper: function(id){
            if(id>0){
                this.edit_account = _.find(this.accounts, function(item){return item.id == id})
                this.is_api_show = this.edit_account.is_api
            }else{
                this.edit_account = {}
            }
            layer.open({
                title: '账户',
                type: 1, 
                content: $('#card-wrapper'),
                area: ['500px','530px']
            })
        },
        sumbit_wrapper: function(){
            this.edit_account.is_api = this.is_api_show
            layer.load(0,{time:10*1000})
            if(this.edit_account.id){
                var url = update_account_url + '/' + this.edit_account.id                
                fetch.post(url, this.edit_account).then(res => {
                    this.init_data()
                    this.closeAll()
                })
            }else{
                fetch({
                    method: 'post', 
                    url: add_account_url,
                    data: this.edit_account
                }).then(res => {
                    this.init_data()
                    this.closeAll()
                })
            }
            
        },
        del: function(id){
            var url = del_account_url + '/' + id
            fetch({
                url: url
            }).then(res=>{
                if(res.data == 'succ'){
                    this.accounts = _.difference(this.accounts, _.remove(this.accounts, function(item){return item.id == id}))
                }
            })

        },
        login: function(account_id){
            var url = login_url + '/' + account_id
            layer.load()
            fetch.get(url).then(res=>{    
                layer.closeAll()            
                layer.msg(res.data)
                this.init_data()
            })

        },
        test_make_order: function(account_id, open){
            this.test_account_id = account_id
            if(open){
                layer.open({
                    title: '谷歌验证码',
                    type: 1, 
                    content: $('#gg_code_wrapper'),
                    area: ['200px','200px']
                })
            }else{
                layer.load()
                var url = test_make_order_url + '/' + this.test_account_id
                fetch.post(url, {'gg_code': this.gg_code}).then(res => {   
                    this.closeAll()             
                    layer.msg(res.data)
                })
            }            
        },
        closeAll: function(){
            layer.closeAll()
        }
    },
    mounted: function(){
        var _this = this
        layui.use('form', function(){
            var form = layui.form
            form.on('radio(is_api)', function(data){
                _this.edit_account.is_api = data.value == "1"? true : false
                _this.is_api_show = data.value == "1"? true : false
            });  
            form.render()
        })

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
#gg_code_wrapper{display: none}
.layui-layer-wrap{padding: 20px;}
</style>

