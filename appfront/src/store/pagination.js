import {SET_PAGINATION_COUNT, SET_PAGINATION_PAGE} from './types'
import Vue from 'vue'

export default {
  state: {
    data: {
      count: 100,
      page: 1,
      size: 10
    }
  },
  mutations: {
    [SET_PAGINATION_COUNT] (state, count) {
      Vue.set(state.data, 'count', count)
    },
    [SET_PAGINATION_PAGE] (state, page) {
      Vue.set(state.data, 'page', page)
    }
  }
}
