<template>
<fieldset class="layui-elem-field layui-field-title">
  <legend>操作记录</legend>
  <div class="layui-field-box">
    <table class="layui-table">
      <colgroup>
        <col width="20">
        <col width="100">
        <col width="100">
        <col width="80">
        <col width="80">
        <col width="60">
        <col width="80">
        <col width="80">
        <col width="80">
        <col width="">
      </colgroup>
      <thead>
        <tr>
          <th>ID</th>
          <th>账户</th>
          <th>Number</th>
          <th>交易区</th>
          <th>币种</th>
          <th>类型</th>
          <th>价格</th>
          <th>数量</th>
          <th>总价</th>
          <th>时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in logs" :key="item.id">
          <td>{{item.id}}</td>
          <td>{{item.account_name}}</td>
          <td>{{item.number}}</td>
          <td>{{item.zone_name}}</td>
          <td>{{item.coin_name}}</td>
          <td>{{item.trade_type | buy-sell}}</td>
          <td>{{item.price}}</td>
          <td>{{item.amount}}</td>
          <td>{{(item.amount * item.price).toFixed(4)}}</td>
          <td>{{item.create_at}}</td>
        </tr>
      </tbody>
    </table>
    <div>
      <button class="layui-btn" @click="init_data()">刷新</button>
    </div>
  </div>
</fieldset>    
</template>

<script>
import fetch from '@/fetch.js'

import { init_order_logs_url } from '@/config.js'

export default {
  props: ['refresh'],
  data: function(){
    return {
      logs: []
    }
  },
  methods: {
    init_data: function(){
      fetch.get(init_order_logs_url).then(res=>{
        this.logs = res.data
      })
    }
  },
  watch: {
    refresh: function(){
      this.init_data()
    }
  },
  mounted: function(){
    this.init_data()
  }
    
}
</script>

<style scoped>

</style>


