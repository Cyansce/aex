<template>
    <div>
        <fieldset class="layui-elem-field layui-field-title">
        <legend>余额</legend>
        <div class="layui-field-box">
            <table class="layui-table">
                <colgroup>
                    <col width="100">
                    <col width="200">
                    <col>
                </colgroup>
                <thead>
                    <tr>
                    <th>币种</th>
                    <th>可用余额</th>
                    <th>锁定余额</th>
                    </tr> 
                </thead>
                <tbody>
                    <tr v-for="item in balance" :key="item.id">
                        <td>{{item.name}}</td>
                        <td>{{item.value}}</td>
                        <td>{{item.value_lock}}</td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <button class="layui-btn" @click="init_data()">刷新</button>
                        </td>
                        <td></td>
                    </tr>
                </tbody>
                </table>
        </div>
        </fieldset>  
    </div>

</template>

<script>
import fetch from "@/fetch.js";
import {
    balance_url
} from "@/config.js";


export default {
    props: [ 'accountId', 'coinName'],
    data: function(){
        return {
            balance: []
        }
    },
    methods: {
        init_data: function(){
            if(this.accountId <= 0){
                return 
            }
            var url = balance_url + '/' + this.accountId            
            fetch.get(url).then(res => {
                if(typeof(res.data) == "string"){
                    alert(res.data)
                    return
                }
                if(typeof(res.data) == "object"){
                    this.balance = []
                    this.balance.push({name: 'CNC', value: res.data.cnc_balance, value_lock:res.data.cnc_balance_lock})
                    this.balance.push({name: 'USDT', value: res.data.usdt_balance, value_lock:res.data.usdt_balance_lock})
                    this.balance.push({name: 'BTC', value: res.data.btc_balance, value_lock:res.data.btc_balance_lock})
                    this.balance.push({name: 'BITCNY', value: res.data.bitcny_balance, value_lock:res.data.bitcny_balance_lock})
                    if(this.coinName)
                        this.balance.push({name: this.coinName.toUpperCase() , value: res.data[this.coinName.toLowerCase()+'_balance'], value_lock:res.data[this.coinName+'_balance_lock']})
                }
            })
        }
    },
    watch: {
        accountId: function(){
            this.init_data()
        },
        coinName: function(){
            this.init_data()
        }
    }

};
</script>

<style scoped>
</style>


