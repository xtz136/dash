import Vue from 'vue'
import Router from 'vue-router'
import ListCompany from '@/components/list_company'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/list-company',
      name: 'ListCompany',
      component: ListCompany
    },
    {
      path: '/*',
      redirect: '/list-company'
    }
  ]
})
