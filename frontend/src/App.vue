<template>
  <div id="app">
    <nav-top></nav-top>
    <router-view/>
  </div>
</template>

<script>
import NavTop from '@/components/NavTop'

export default {
  name: 'App',
  components: {
    'nav-top': NavTop
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
