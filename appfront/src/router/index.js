import Vue from 'vue'
import Router from 'vue-router'
import ListCompany from '@/components/list_company'
import ListEntity from '@/components/list_entity'
import BatchAddEntitys from '@/components/batch_add_entitys'
import Print from '@/components/print'
import ListRevertEntity from '@/components/list_revert_entity'
/*
import AddEntity from '@/components/add_entity'
*/
import Main from '@/components/main'
import Container from '@/components/container'
import Entitys from '@/components/entitys'

Vue.use(Router)

Vue.component('entitys', Entitys)

export default new Router({
  routes: [
    {
      path: '/company/:companyId?',
      name: 'Main',
      component: Main,
      meta: {
        title: '资料借用'
      },
      children: [
        {
          path: '',
          name: 'ListCompany',
          component: ListCompany,
          meta: {
            title: '公司列表'
          }
        },
        {
          path: 'entity',
          name: 'EntityContainer',
          component: Container,
          meta: {
            bcName: 'ListEntity',
            title: '资料列表'
          },
          children: [
            {
              path: '',
              name: 'ListEntity',
              component: ListEntity,
              props: true,
              meta: {
                bcSkip: true,
                title: ''
              }
            },
            {
              path: 'add',
              name: 'BatchAddEntitys',
              component: BatchAddEntitys,
              props: true,
              meta: {
                title: '资料录入'
              }
            },
            {
              path: 'revert/print',
              name: 'Print',
              component: Print,
              props: true,
              meta: {
                title: '资料归还'
              }
            }
          ]
        }
      ]
    },
    {
      path: '/revertentitys',
      name: 'Main',
      component: Main,
      meta: {
        title: '已归还资料列表'
      },
      children: [
        {
          path: '',
          name: 'ListRevertEntity',
          component: ListRevertEntity,
          meta: {
            title: '归还单'
          }
        },
        {
          path: 'revert/print',
          name: 'Print2',
          component: Print,
          props: true,
          meta: {
            title: '资料归还'
          }
        }
      ]
    },
    {
      path: '',
      redirect: '/company'
    }
  ]
})
