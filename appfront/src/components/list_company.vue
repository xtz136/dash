<template>
  <Table :columns="columns" :data="data"></Table>
</template>

<script>
export default {
  name: 'ListCompany',
  data () {
    return {
      columns: [
        {title: '标题', key: 'title'},
        {title: '所属行业', key: 'industry'},
        {title: '业务员', key: 'saleman'},
        {title: '记账会计', key: 'bookkeeper'},
        {title: '纳税人类型', key: 'taxpayer_type'},
        {title: '执照过期日期', key: 'license_status'},
        {title: '代理状态', key: 'status'},
        {title: '联系人信息', key: 'contactor_info'},
        {
          title: '操作',
          key: 'action',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {props: {type: 'primary', size: 'small'}}, '资料管理')
            ])
          }
        }
      ]
    }
  },
  computed: {
    data () {
      return this.$store.getters.companyList
    }
  },
  created () {
    this.$store.dispatch('fetchCompanyList')
  }
}
</script>
