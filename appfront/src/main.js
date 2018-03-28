// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BaseApi from './api/base'
import getStore from './store'
import Vuex from 'vuex'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

// 可以切换api的开发模式
BaseApi.prototype._devMode = window._devMode || false

Vue.config.productionTip = false
Vue.use(iView)
Vue.use(Vuex)

console.log(router)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store: getStore(),
  router,
  components: { App },
  template: '<App />'
})
