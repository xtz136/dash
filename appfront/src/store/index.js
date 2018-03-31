import Vue from 'vue'
import Vuex from 'vuex'

import CompanyApi from '../api/company'
import EntityListApi from '../api/entity_list'
import EntityApi from '../api/entity'
import PeopleApi from '../api/people'

import notify from './notify'
import pagination from './pagination'
import config from './config'

import {
  PUSH_BREADCRUMB,
  POP_BREADCRUMB,
  FETCH_COMPANY_LIST,
  FILTER_ENTITY_LIST,
  FILTER_ENTITYS_LIST,
  FILTER_ENTITYS_ALL_LIST,
  REVERT_ENTITYS,
  FILTER_PEOPLES_LIST,
  UPDATE_ENTITYS,
  SHOW_NOTIFY
} from './types'

Vue.use(Vuex)

/**
 * 自动判断接口出错或者网络错误，并进行提示
 * 如果是网络错误，会中断 promise 的后续操作
 */
const withErrorP = (p) => {
  return new Promise((resolve, reject) => {
    p.then(x => {
      if (x.status) {
        resolve(x)
      } else {
        store.dispatch(SHOW_NOTIFY, {title: x.msg || '未知错误', type: 'error', duration: 0})
        reject(x)
      }
    }).catch(x => {
      console.error(x)
      store.dispatch(SHOW_NOTIFY, {title: '网络出错！', type: 'error', duration: 0})
    })
  })
}

const company = {
  state: {
    companyList: []
  },
  getters: {
    companyList (state) {
      return state.companyList
    },
    companyById: (state) => (id) => {
      return state.companyList.find(x => x.id === id)
    }
  },
  mutations: {
    [FETCH_COMPANY_LIST] (state, datas) {
      Vue.set(state, 'companyList', datas)
    }
  },
  actions: {
    [FETCH_COMPANY_LIST] ({commit, state}, payload) {
      return withErrorP(CompanyApi.filter(payload))
        .then(result => {
          commit(FETCH_COMPANY_LIST, result.msg.datas)
          return result
        })
    }
  }
}

const entity = {
  state: {
    entityList: []
  },
  getters: {
    entityList (state) {
      return state.entityList
    }
  },
  mutations: {
    [FILTER_ENTITY_LIST] (state, datas) {
      Vue.set(state, 'entityList', datas)
    }
  },
  actions: {
    [FILTER_ENTITY_LIST] ({commit, state}) {
      // 物品比较固定，所以只请求一次
      if (state.entityList.length > 0) {
        return Promise.resolve(state.entityList)
      }

      return EntityApi.filter().then(result => {
        commit(FILTER_ENTITY_LIST, result.msg)
      })
    }
  }
}

const entitys = {
  state: {
    entitys: []
  },
  getters: {
    entitys (state) {
      return state.entitys
    }
  },
  mutations: {
    [FILTER_ENTITYS_LIST] (state, datas) {
      Vue.set(state, 'entitys', datas)
    },
    [REVERT_ENTITYS] (state, data) {
      const found = state.entitys.filter(x => data.selected.includes(x.id))
      if (found.length > 0) {
        found.forEach(x => {
          Vue.set(x, 'status', '归还')
        })
      }
    }
  },
  actions: {
    [FILTER_ENTITYS_LIST] ({commit}, payload) {
      return withErrorP(EntityListApi.filter(payload))
        .then(result => {
          commit(FILTER_ENTITYS_LIST, result.msg.datas)
          return result
        })
    },
    [FILTER_ENTITYS_ALL_LIST] ({commit}, payload) {
      return withErrorP(EntityListApi.filterAll(payload))
        .then(result => {
          commit(FILTER_ENTITYS_LIST, result.msg)
          return result
        })
    },
    [UPDATE_ENTITYS] ({commit}, payload) {
      return withErrorP(EntityListApi.update(payload))
    },
    [REVERT_ENTITYS] ({commit}, payload) {
      return withErrorP(EntityListApi.revert(payload))
        .then(result => {
          commit(REVERT_ENTITYS, payload)
          return result
        })
    }
  }
}

const people = {
  state: {
    peoples: []
  },
  getters: {
    peoples (state) {
      return state.peoples
    }
  },
  mutations: {
    [FILTER_PEOPLES_LIST] (state, datas) {
      Vue.set(state, 'peoples', datas)
    }
  },
  actions: {
    [FILTER_PEOPLES_LIST] ({commit}, payload) {
      return PeopleApi.filter(payload).then(result => {
        commit(FILTER_PEOPLES_LIST, result.msg)
        return result
      })
    }
  }
}

const breadcrumb = {
  state: {
    breadcrumb: []
  },
  getters: {
    breadcrumb (state) {
      return state.breadcrumb
    }
  },
  mutations: {
    [PUSH_BREADCRUMB] (state, data) {
      Vue.set(state, 'breadcrumb', [].concat(state.breadcrumb, [data]))
    },
    [POP_BREADCRUMB] (state, num = 1) {
      Vue.set(state, 'breadcrumb', state.breadcrumb.slice(0, -num))
    }
  }
}

const store = new Vuex.Store({
  modules: {config, company, entity, entitys, people, breadcrumb, notify, pagination},
  strict: true
})

export default store
