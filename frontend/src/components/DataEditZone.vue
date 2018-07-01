<template>
    <div>
        <blockquote class="layui-elem-quote"><h2>交易区</h2></blockquote>

        <button class="layui-btn" v-on:click="open_wrapper('add')">新增</button>
        <hr>
        <table class="layui-table">
            <colgroup>
                <col width="200">
                <col width="200">
                <col>
            </colgroup>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>创建时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in zones" :key="item.id">
                    <td>{{item.name}}</td>
                    <td>{{item.create_at}}</td>
                    <td>
                        <button class="layui-btn" disabled @click="open_wrapper('edit',item.id)">修改</button>
                        <button class="layui-btn" @click="del(item.id)">删除</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div id="open-data-wrap">
            <form class="layui-form" onsubmit="return false">
                <div class="layui-form-item">
                    <input type="text" name="title" v-model="zone_edit_name" lay-verify="required" placeholder="交易区名称" autocomplete="off" class="layui-input">
                </div>
                <div class="layui-form-item">
                    <div class="layui-input-block">
                    <button class="layui-btn" v-on:click="add_sumbit">提交</button>
                    <button class="layui-btn layui-btn-primary" v-on:click="closeAll">取消</button>
                    </div>
                </div>
            </form>
        </div>
    </div>    
</template>

<script>
import fetch from '@/fetch.js'
import {zones_url, add_zone_url, del_zone_url} from '@/config.js'

var _ = require('lodash')

export default {
    data: function() {
        return {            
            zones: [],
            zone_edit_name: '',
            zone_edit_id: 0,
        }
    },
    mounted: function(){
        layui.use('layer', function(){
            var layer = layui.layer
        })
        this.init_data()
    },
    methods: {
        open_wrapper: function(option, id=0){
            if(option == 'add'){
                this.zone_edit_name = ''
                this.zone_edit_id = 0
            }
            if(option == 'edit'){
                var this_zone = _.find(this.zones, ['id', id])
                this.zone_edit_name = this_zone.name
                this.zone_edit_id = this_zone.id
            }
            layer.open({
                type: 1, 
                content: $('#open-data-wrap'),
                area: ['400px','200px']
            })
        },
        add_sumbit: function(){
            fetch({
                method: 'post', 
                url: add_zone_url,
                data: {'zone': this.zone_edit_name}
            }).then(res => {
                this.zones = res.data
                layer.closeAll()
            })
            return false
        },
        del: function(id){
            console.log(id)
            fetch({
                url: del_zone_url,
                method: 'post',
                data: { 'id': id }
            }).then(res => {
                this.zones = res.data
            })
        },
        update: function(id){
        },
        closeAll: function(){
            layer.closeAll()
            return false
        },
        init_data: function() {
            fetch({
                url: zones_url,
            }).then(res => {
                this.zones = res.data
            })
        }
    },
    
}
</script>

<style scoped>
#open-data-wrap{display: none}
.layui-form {margin-top: 10px}
.layui-layer-wrap{padding: 20px;}
</style>

