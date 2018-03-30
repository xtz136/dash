import Vue from 'vue'
import Vuex from 'vuex'
import CompanyApi from './api/company'
import EntityListApi from './api/entity_list'
import EntityApi from './api/entity'
import PeopleApi from './api/people'

// 现在需要配置的东西比较简单，以后复杂了就单独放一个文件
const config = {
  state: {
    'adminUrl': '/admin'
  }
}

export const PUSH_BREADCRUMB = 'PUSH_BREADCRUMB'
export const POP_BREADCRUMB = 'POP_BREADCRUMB'
export const FETCH_COMPANY_LIST = 'FETCH_COMPANY_LIST'
export const FILTER_ENTITY_LIST = 'FILTER_ENTITY_LIST'
export const FETCH_ENTITYS = 'FETCH_ENTITYS'
export const FILTER_PEOPLES = 'FILTER_PEOPLES'

const company = {
  state: {
    companyList: [],
    entityList: [],
    breadcrumb: [],
    entitys: [],
    peoples: []
  },
  getters: {
    companyList (state) {
      return state.companyList
    },
    entityList (state) {
      return state.entityList
    },
    breadcrumb (state) {
      return state.breadcrumb
    },
    entitys (state) {
      return state.entitys
    },
    peoples (state) {
      return state.peoples
    }
  },
  mutations: {
    [FETCH_COMPANY_LIST] (state, datas) {
      Vue.set(state, 'companyList', datas)
    },
    [FILTER_ENTITY_LIST] (state, datas) {
      Vue.set(state, 'entityList', datas)
    },
    [PUSH_BREADCRUMB] (state, data) {
      Vue.set(state, 'breadcrumb', [].concat(state.breadcrumb, [data]))
    },
    [POP_BREADCRUMB] (state, num = 1) {
      Vue.set(state, 'breadcrumb', state.breadcrumb.slice(0, -num))
    },
    [FETCH_ENTITYS] (state, datas) {
      Vue.set(state, 'entitys', datas)
    },
    [FILTER_PEOPLES] (state, datas) {
      Vue.set(state, 'peoples', datas)
    }
  },
  actions: {
    fetchCompanyList ({commit}) {
      return CompanyApi.list().then(result => {
        commit(FETCH_COMPANY_LIST, result.datas)
      })
    },
    filterEntityList ({commit}, payload) {
      return EntityListApi.filter(payload).then(result => {
        commit(FILTER_ENTITY_LIST, result.datas)
      })
    },
    fetchEntitys ({commit}) {
      return EntityApi.list().then(result => {
        commit(FETCH_ENTITYS, result.datas)
      })
    },
    filterPeoples ({commit}, payload) {
      return PeopleApi.filter(payload).then(result => {
        commit(FILTER_PEOPLES, result.datas)
      })
    },
    addEntityList ({commit}, payload) {
      return EntityListApi.add(payload)
    }
  }
}

export default function getStore() {
  return new Vuex.Store({
    modules: {config, company},
    strict: true
  })
}
