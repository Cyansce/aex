import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard'
import APITrade from '@/components/APITrade'
import StrategyLoopTrade from '@/components/StrategyLoopTrade'
import DataEditZone from '@/components/DataEditZone'
import DataEditCoin from '@/components/DataEditCoin'
import DataEditKey from '@/components/DataEditKey'
import DataEditAccount from '@/components/DataEditAccount'
import OrderManageAEX from '@/components/OrderManageAEX'
import StrategyLoopAPITrade from '@/components/StrategyLoopAPITrade'  
import DataEditStrategyOrderLoop from '@/components/DataEditStrategyOrderLoop'  
import OrderManageStrategy from '@/components/OrderManageStrategy'  
import ReservationOrder from '@/components/ReservationOrder'
import APIConfig from '@/components/APIConfig'
import GatFlush from '@/components/GatFlush'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/apitrade',
      name: 'APITrade',
      component: APITrade
    },
    {
      path: '/trade',
      name: 'StrategyLoopTrade',
      component: StrategyLoopTrade
    },
    {
      path: '/dataeditzone',
      name: 'DataEditZone',
      component: DataEditZone
    },
    {
      path: '/dataeditcoin',
      name: 'DataEditCoin',
      component: DataEditCoin
    },
    {
      path: '/dataeidtkey',
      name: 'DataEditKey',
      component: DataEditKey
    },
    {
      path: '/dataeidtaccount',
      name: 'DataEditAccount',
      component: DataEditAccount
    },
    {
      path: '/ordermanageaex',
      name: 'OrderManageaex',
      component: OrderManageAEX
    },
    {
      path: '/loopapitrade',
      name: 'StrategyLoopAPITrade',
      component: StrategyLoopAPITrade
    },
    {
      path: '/dataeditstrategyorderloop',
      name: 'DataEditStrategyOrderLoop',
      component: DataEditStrategyOrderLoop
    },
    {
      path: '/ordermanagestrategy',
      name: 'OrderManageStrategy',
      component: OrderManageStrategy
    },
    {
      path: '/reservationorder',
      name: 'ReservationOrder',
      component: ReservationOrder
    },
    {
      path: '/apiconfig',
      name: 'APIConfig',
      component: APIConfig
    },
    {
      path: '/gatflush',
      name: 'GatFlush',
      component: GatFlush
    },
  ]
})
