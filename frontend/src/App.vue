<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import './assets/styles/fonts.css'

export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Tahoma, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  direction: rtl;
}
</style>
