import {SET_BREADCRUMB} from './types'
import Vue from 'vue'

export default {
  state: {
    data: {}
  },
  mutations: {
    [SET_BREADCRUMB] (state, {name, title}) {
      Vue.set(state.data, name, title)
    }
  }
}
