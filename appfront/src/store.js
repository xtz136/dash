import Vue from 'vue'
import Vuex from 'vuex'
import CompanyApi from './api/company'

// 现在需要配置的东西比较简单，以后复杂了就单独放一个文件
const config = {
  state: {
    'adminUrl': '/admin'
  }
}

const FETCH_COMPANY_LIST = 'FETCH_COMPANY_LIST'

const company = {
  state: {
    companyList: []
  },
  getters: {
    companyList (state) {
      return state.companyList
    }
  },
  mutations: {
    [FETCH_COMPANY_LIST] (state, datas) {
      Vue.set(state, 'companyList', datas)
    }
  },
  actions: {
    fetchCompanyList ({commit}) {
      CompanyApi.list().then(result => {
        commit(FETCH_COMPANY_LIST, result.datas)
      })
    }
  }
}

const getStore = function () {
  return new Vuex.Store({
    modules: {config, company},
    strict: true
  })
}

export default getStore
