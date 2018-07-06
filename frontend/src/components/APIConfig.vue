<template>
    <div>
        <blockquote class="layui-elem-quote"><h2>API网址修改</h2></blockquote>

        <button class="layui-btn" @click="open_wrapper">新增</button>
        <table class="layui-table">
            <tr v-for="item in configs" :key="item.id" :class="{is_default: item.is_default}">
                <td>{{item.id}}</td>
                <td>{{item.url}}</td>
                <td>
                    <button v-if="!item.is_default" class="layui-btn layui-btn-primary" @click="set_default(item.id)">设为默认</button>
                    <button class="layui-btn layui-btn-primary" @click="del(item.id)">删除</button>
                </td>
            </tr>
            
        </table>

        <div id="wrapper">
            <table class="layui-table">
                <tr>
                    <td>
                        <input type="text" placeholder="url" class="layui-input" v-model="url">
                    </td>
                </tr>
                <tr>
                    <td>
                        <button class="layui-btn" @click="add()" style="width:270px">提交</button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import {
    api_configs_url,
    add_api_config_url,
    del_api_config_url,
    set_default_api_config_url,
} from '@/config.js'
import fetch from '@/fetch.js'

export default {
    data: function(){
        return {
            configs: [],

            url: ''
        }
    },
    methods: {
        init_data: function(){
            fetch.get(api_configs_url).then(res => {
                this.configs = res.data
            })
        },
        open_wrapper: function(){
            layer.open({
                title: 'API网址',
                type: 1,
                content: $('#wrapper'),
                area: ['300px', '']
            })

        },
        add: function(){
            layer.load()
            if(this.url != ''){
                fetch.post(
                    add_api_config_url,
                    { 'url': this.url },
                ).then(res => {
                    layer.closeAll()
                    layer.msg(res.data)
                    this.init_data()
                    this.init_data()
                })
            }

        },
        del: function(id){
            layer.load()
            var url = del_api_config_url + '/' + id
            fetch.get(url).then(res => {
                layer.closeAll()
                layer.msg(res.data)
                this.init_data()
            })
        },
        set_default: function(id){
            layer.load()
            var url = set_default_api_config_url + '/' + id
            fetch.get(url).then(res => {
                layer.closeAll()
                layer.msg(res.data)
                this.init_data()
            })
        }
    },
    mounted() {
        this.init_data()
        layui.use('layer', function(){
            var layer = layui.layer
        })
    },
}
</script>

<style scoped>
.is_default{background-color: #5FB878}
#wrapper{display: none}
</style>


