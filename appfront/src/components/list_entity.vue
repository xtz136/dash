<template>
  <div>
    <Table :loading="loading" :columns="columns" :data="result" @on-selection-change="selectChange"></Table>
    <div class="gap-top">
      <Button type="warning" @click="addEntity">资料录入</Button>
      <Button type="info" @click="revertEntity">归还</Button>
      <Button type="default" @click="$router.back()">后退</Button>
    </div>
  </div>
</template>

<script>
import {FILTER_ENTITYS_ALL_LIST, REVERT_ENTITYS, SHOW_NOTIFY} from '../store/types'

let selected = []

export default {
  name: 'ListEntity',
  props: ['companyId'],
  data () {
    return {
      loading: false,
      columns: [
        {type: 'selection', align: 'center', width: 60},
        {type: 'index', align: 'center', width: 60},
        {title: '物品', key: 'entity'},
        {title: '数量', key: 'amount', width: 60},
        {title: '签收人', key: 'signer'},
        {title: '签收日期', key: 'sign_date'},
        {title: '借用人', key: 'borrower'},
        {title: '借用日期', key: 'borrow_date'},
        {title: '归还日期', key: 'revert_borrow_date'},
        {title: '状态', key: 'status', width: 60},
        {title: '备注', key: 'descript'},
        {
          title: '操作',
          key: 'action',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {type: 'primary', size: 'small', disabled: params.row._disabled},
                on: {
                  click: () => {
                    this.updateEntity(params.row.id)
                  }
                }
              }, '修改')
            ])
          }
        }
      ],
      addEntityModal: false
    }
  },
  computed: {
    pagination () {
      return this.$store.state.pagination.data
    },
    data () {
      return this.$store.getters.entitys
    },
    result () {
      return this.data.length
        ? this.data.map(x => Object.assign({_disabled: x.status === '归还'}, x))
        : []
    }
  },
  methods: {
    addEntity() {
      this.$router.push({name: 'AddEntity', params: {companyId: this.companyId}})
    },
    updateEntity(id) {
      this.$router.push({
        name: 'UpdateEntity',
        params: {
          companyId: this.companyId,
          entityListId: id,
          old: this.getDataById(id)
        }
      })
    },
    getDataById(id) {
      return this.data.find(x => x.id === id)
    },
    selectChange (change) {
      selected = change
    },
    revertEntity () {
      if (selected.length === 0) {
        this.$store.dispatch(SHOW_NOTIFY, {title: '还没选择归还物品', type: 'warning'})
        return
      }
      this.$store.dispatch(REVERT_ENTITYS, {selected: selected.map(x => x.id)})
        .then(({msg}) => {
          const simpleEntitys = selected.map(x => ({entity: x.entity, amount: x.amount}))
          selected = []
          this.$router.push({
            name: 'Print',
            params: {
              companyId: this.companyId,
              entitys: simpleEntitys,
              orderId: msg
            }
          })
        })
    }
  },
  created () {
    const found = this.$store.getters.companyById(parseInt(this.companyId))
    if (!found) {
      this.$store.dispatch(
        SHOW_NOTIFY,
        {title: '没有找到对应的公司', desc: '请重新选择公司进入资料管理', type: 'error', duration: 0}
      )
    } else {
      this.loading = true
      this.$store.dispatch(
        FILTER_ENTITYS_ALL_LIST,
        {company_id: parseInt(this.companyId), status: '归还'}
      ).then(() => {
        this.loading = false
      })
    }
  }
}
</script>
