<template>
  <div>
    <Input v-model="searchValue" placeholder="搜索公司" icon="ios-search" @on-keypress="search"></Input>
    <Table :loading="loading" :columns="columns" :data="data"></Table>
    <Page v-if="pagination.count > 0" :current="pagination.page" :total="pagination.count" class-name="gap-top" @on-change="pageChange" show-elevator></Page>
  </div>
</template>

<script>
import {FETCH_COMPANY_LIST, SET_PAGINATION_PAGE, SET_PAGINATION_COUNT} from '../store/types'

export default {
  name: 'ListCompany',
  data () {
    return {
      searchValue: '',
      loading: true,
      columns: [
        {type: 'index', align: 'center', width: 60},
        {title: '标题', key: 'title', width: 200},
        {title: '所属行业', key: 'industry'},
        {title: '业务员', key: 'saleman'},
        {title: '记账会计', key: 'bookkeeper'},
        {title: '纳税人类型', key: 'taxpayer_type'},
        {title: '执照过期日期', key: 'license_status'},
        {title: '代理状态', key: 'status'},
        {title: '联系人信息', key: 'contactor_info', width: 200},
        {
          title: '操作',
          key: 'action',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {type: 'primary', size: 'small'},
                style: 'margin-bottom: 5px',
                on: {
                  click: () => {
                    this.toListEntity(params.row.id)
                  }
                }
              }, '资料管理')
              /*
              h('Button', {
                props: {type: 'info', size: 'small'},
                on: {
                  click: () => {
                    this.toListRevertEntity(params.row.id)
                  }
                }
              }, '归还记录')
              */
            ])
          }
        }
      ]
    }
  },
  methods: {
    toListEntity (companyId) {
      this.$router.push({name: 'ListEntity', params: {companyId}})
    },
    toListRevertEntity (companyId) {
      this.$router.push({name: 'ListRevertEntity', params: {companyId}})
    },
    pageChange (pageNum, args = {}) {
      this.$store.dispatch(FETCH_COMPANY_LIST, {page: pageNum, ...args})
        .then(result => {
          this.$store.commit(SET_PAGINATION_PAGE, pageNum)
          this.$store.commit(SET_PAGINATION_COUNT, result.msg.count)
          this.loading = false
        })
    },
    search (event) {
      if (event.which === 13) {
        this.loading = true
        this.pageChange(1, {title: this.searchValue})
      }
    }
  },
  computed: {
    pagination () {
      return this.$store.state.pagination.data
    },
    data () {
      return this.$store.getters.companyList
    }
  },
  created () {
    window.title = this.$store.state.config.companyName
    this.pageChange(this.pagination.page)
  }
}
</script>
