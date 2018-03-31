import Vue from 'vue'
import Router from 'vue-router'
import ListCompany from '@/components/list_company'
import ListEntity from '@/components/list_entity'
import ListRevertEntity from '@/components/list_revert_entity'
import AddEntity from '@/components/add_entity'
import Print from '@/components/print'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/company',
      name: 'ListCompany',
      component: ListCompany,
      props: (route) => ({page: route.query.page || 1}),
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
      path: '/company/:companyId/revertentity',
      name: 'ListRevertEntity',
      component: ListRevertEntity,
      props: true,
      meta: {
        title: '已归还资料列表'
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
      path: '/company/:companyId/entity/:entityListId/update',
      name: 'UpdateEntity',
      component: AddEntity,
      props: true,
      meta: {
        title: '资料修改'
      }
    },
    {
      path: '/company/:companyId/entity/revert/print',
      name: 'Print',
      component: Print,
      props: true
    },
    {
      path: '/*',
      redirect: '/company'
    }
  ]
})
