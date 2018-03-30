import Vue from 'vue'
import Router from 'vue-router'
import ListCompany from '@/components/list_company'
import ListEntity from '@/components/list_entity'
import AddEntity from '@/components/add_entity'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/company',
      name: 'ListCompany',
      component: ListCompany,
      meta: {
        title: '公司列表'
      }
    },
    {
      path: '/company/:companyId/entity',
      name: 'ListEntity',
      component: ListEntity,
      props: true,
      meta: {
        title: '资料列表'
      }
    },
    {
      path: '/company/:companyId/entity/add',
      name: 'AddEntity',
      component: AddEntity,
      props: true,
      meta: {
        title: '资料录入'
      }
    },
    {
      path: '/*',
      redirect: '/company'
    }
  ]
})
