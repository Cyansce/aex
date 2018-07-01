<template>
<div class="layui-form">
    <blockquote class="layui-elem-quote"><h2>API交易</h2></blockquote>

    <div class="layui-row layui-col-space10">
        <div class="layui-card">
        <div class="layui-card-header">當前賬戶</div>
            <div class="layui-card-body">
                <select id="api_account" v-model="current_account_id" lay-filter="select-current-account">
                    <option v-for="item in accounts" :key="item.id" :value="item.id">{{item.name}}</option>
                </select>
                <button class="layui-btn b100 mg-top10" :class="btn_danger" @click="lock_account()">{{lock_account_text}}</button>
            </div>
        </div>
    </div>

    <div class="layui-row layui-col-space10">
        <div class="layui-col-xs2">
            <select v-model="zone_id" name="zone" lay-filter="zone">
                <option v-for="item in zones" :key="item.id" :value="item.id">{{item.name}}</option>
            </select>
        </div>
        <div class="layui-col-xs2">
            <input type="text" class="layui-input" placeholder="数量" v-model="amount">
        </div>
        <div class="layui-col-xs2">
            <select v-model="current_coin.id" name="coin" lay-filter="coin">
                <option v-for="item in coins" :key="item.id" :value="item.id">{{item.name}}</option>
            </select>
        </div>
    </div>
    <div class="layui-row layui-col-space10">
        <div class="layui-col-xs2">
            <input type="text" class="layui-input" v-model="ticker.buy" readonly @click="get_price(ticker.buy)">
        </div>
        <div class="layui-col-xs2">
            <button class="layui-btn layui-btn-primary w40" @click="desc1()">⬇</button>
            <input type="text" class="layui-input w100" v-model="price">
            <button class="layui-btn layui-btn-primary w40" @click="add1()">⬆</button>
        </div>
        <div class="layui-col-xs2">
            <input type="text" class="layui-input" v-model="ticker.sell" readonly @click="get_price(ticker.sell)">
        </div>
    </div>
    <div class="layui-row layui-col-space10">
        <div class="layui-col-xs2">
            <button class="layui-btn b100" @click="mk_order(1)">买入</button>
        </div>
        <div class="layui-col-xs2">
            <button class="layui-btn layui-btn-primary w40" @click="sum11()">11</button>
            <input type="text" class="layui-input w100" v-model="sum_price" disabled>
            <button class="layui-btn layui-btn-primary w40" @click="sum_22()">22</button>
        </div>
        <div class="layui-col-xs2">
            <button class="layui-btn b100" @click="mk_order(2)">卖出</button>
        </div>
    </div>
    <balance :account-id="current_account_id" :coin-name="current_coin.name"></balance>
    <operation-log :refresh="log_refresh"></operation-log>
</div>
</template>

<script>
import fetch from "@/fetch.js";
import {
  accounts_url,
  zones_url,
  coins_url,
  ticker_url,
  coin_url,
  order_url
} from "@/config.js";

import OperationLog from "@/components/OperationLog"
import Balance from "@/components/Balance"

var _ = require("lodash")

export default {
  components: {
    "operation-log": OperationLog,
    balance: Balance
  },
  data: function() {
    return {
      accounts: [],
      current_account_id: 0,
      zones: [],
      zone_id: 0,
      coins: [],

      btn_danger: "",
      lock_account_text: "锁定",

      ticker: {
        buy: 0,
        sell: 0
      },
      price: 0,
      sum_price: 0,
      amount: 0,

      current_coin: {},
      balance: {},

      log_refresh: 0
    };
  },
  methods: {
    init_data: function() {
      fetch.get(accounts_url).then(res => {
        this.accounts = res.data;
      });
      fetch.get(zones_url).then(res => {
        this.zones = res.data;
      });
      //   this.get_ticker()
    },
    fetch_coin: function(zone_id) {
      fetch.get(coins_url).then(res => {
        this.coins = _.filter(res.data, function(item) {
          return item.zone_id == zone_id;
        });
      });
    },
    refresh_form: function() {
      layui.use("form", function() {
        var form = layui.form;
        form.render();
      });
    },
    lock_account: function() {
      if ($("#api_account").attr("disabled") == null) {
        this.btn_danger = "layui-btn-danger";
        $("#api_account").attr("disabled", "disabled");
        this.lock_account_text = "解锁";
      } else {
        $("#api_account").removeAttr("disabled");
        this.btn_danger = "";
        this.lock_account_text = "锁定";
      }
      this.refresh_form();
    },
    get_ticker: function(coin_id) {
      if (coin_id == 0) return;
      fetch.post(ticker_url, { coin_id: coin_id }).then(res => {
        this.ticker = res.data.ticker;
      });
    },
    get_coin: function(id){
      var url = coin_url + '/' + id
      fetch.get(url).then(res => {
        this.current_coin = res.data
        window.localStorage.setItem('coin', JSON.stringify(this.current_coin))
      })
    },
    get_price: function(price) {
      this.price = price;
    },
    sum11: function() {
      this.sum_price = 11;
      this.amount = (this.sum_price / this.price).toFixed(4);
    },
    sum_22: function() {
      this.sum_price = 22;
      this.amount = (this.sum_price / this.price).toFixed(4);
    },
    add1: function(){
        var last = parseFloat(this.price) + parseFloat(this.getUnit(this.current_coin.point))
        this.price = last.toFixed(this.current_coin.point)
    },
    desc1: function(){
        var last = this.price - this.getUnit(this.current_coin.point)
        this.price = last.toFixed(this.current_coin.point)
    },

    mk_order: function(trade_type){
        var index = layer.load(0)
        var data = {
          account_id: this.current_account_id,
          coin_id: this.current_coin.id,
          trade_type: trade_type,
          price: this.price,
          amount: this.amount
        }
        fetch.post(order_url, data).then(res=>{
          layer.close(index)
          layer.msg(res.data)
          this.log_refresh = _.random(1.11,100.22)
        })
    },

    // 获取一个递减或递增单位
    getUnit: function(y) {
      var z = 1;
      for (var i = y; i > 0; i--) {
        z = z / 10;
      }
      return z;
    }
  },
  watch: {
    coins: function() {
      this.$nextTick(function() {
        this.refresh_form();
      });
    },
    accounts: function() {
      this.$nextTick(function() {
        this.refresh_form();
      });
    },
    zones: function() {
      this.$nextTick(function() {
        this.refresh_form();
      });
    },
    amount: function() {
      this.sum_price = (this.price * this.amount).toFixed(4);
    },
    price: function() {    
      if(String(this.price).indexOf('e')>=0 && !$.isEmptyObject(this.current_coin)){
        this.price = this.price.toFixed(this.current_coin.point)
      }
      this.amount = (this.sum_price / this.price).toFixed(4);
    }
  },
  mounted: function() {
    this.$nextTick(function() {
      var _this = this;
      this.init_data();
      layui.use("form", function() {
        var form = layui.form;
        form.on("select(select-current-account)", function(data) {
          _this.current_account_id = data.value;
          window.localStorage.setItem('account_id', data.value)
        });
        form.on("select(zone)", function(data) {
          _this.zone_id = data.value;
          _this.coin_id = 0;
          window.localStorage.setItem('zone_id', data.value)
          _this.fetch_coin(data.value);
        });
        form.on("select(coin)", function(data) {
          _this.get_coin(data.value)
          _this.get_ticker(data.value)
        });
      });
      var account_id = window.localStorage.getItem('account_id') 
      var coin = JSON.parse(window.localStorage.getItem('coin'))
      var zone_id = window.localStorage.getItem('zone_id') 
      if(account_id){
        this.current_account_id = account_id
      }
      if(coin && !$.isEmptyObject(coin)){
        this.zone_id = zone_id
        this.current_coin = coin
        _this.fetch_coin(zone_id);
        _this.get_ticker(coin.id)
      }
    });
  }
};
</script>

<style scoped>
.layui-col-xs2 {
  width: 200px;
}
.layui-btn {
  padding: 0;
}
.layui-input {
  display: inline-block;
}
.w100 {
  width: 100px;
}
.w40 {
  width: 40px;
}
.b100 {
  width: 100%;
}
.mg-top10 {
  margin-top: 10px;
}
.layui-card {
  margin: 10px 0 10px 0;
  width: 400px;
}
</style>


