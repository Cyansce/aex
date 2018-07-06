<template>
  <ul class="layui-nav" lay-filter="">
    <li class="layui-nav-item layui-this">
      <router-link to="/">Dashboard</router-link>
    </li>
    <li class="layui-nav-item">
      <router-link to="/apitrade">API交易</router-link>
    </li>
    <li class="layui-nav-item">
      <a href="javascript:;">策略挂单</a>
      <dl class="layui-nav-child"> <!-- 二级菜单 -->
        <dd><router-link to="/loopapitrade">API挂单</router-link></dd>
        <dd><router-link to="/trade">直接挂单</router-link></dd>   
        <dd><router-link to="/reservationorder">预约挂单</router-link></dd>   
      </dl>
    </li>
    <li class="layui-nav-item">
      <a href="javascript:;">挂单管理</a>
      <dl class="layui-nav-child"> <!-- 二级菜单 -->
        <dd><router-link to="/ordermanagestrategy">策略挂单</router-link></dd>
        <dd><router-link to="/ordermanageaex">aex挂单</router-link></dd>   
      </dl>
    </li>
    <li class="layui-nav-item">
      <a href="javascript:;">数据修改</a>
      <dl class="layui-nav-child"> <!-- 二级菜单 -->
        <dd><router-link to="/dataeditzone">交易区</router-link></dd>
        <dd><router-link to="/dataeditcoin">币种</router-link></dd>
        <!-- <dd><router-link to="/dataeidtkey">Key</router-link></dd>       -->
        <dd><router-link to="/dataeidtaccount">账户</router-link></dd>      
        <dd><router-link to="/dataeditstrategyorderloop">循环挂单策略</router-link></dd>      
      </dl>
    </li>
    <li class="layui-nav-item"><a href="">社区</a></li>
  </ul>
 

</template>

<script>
export default {
  created: function() {
    layui.use('element', function(){
      var element = layui.element
    })  
  }
};
</script>

<style scoped>
.layui-nav{margin-bottom: 10px}
</style>


