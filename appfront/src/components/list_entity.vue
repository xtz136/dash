<style scope>
.list-entitys-container {
  position: relative;
}
.edit-entitys-wrap {
  position: absolute;
  top: 0;
  left: 0;
  background-color: hsla(0,0%,100%,.9);
  width: 100%;
  height: 100%;
  z-index: 9999;
}
.edit-entitys-wrap .fields {
  background-color: white;
}

.edit-entitys-position {
  width: 100%;
  position: absolute;
}
</style>

<template>
  <div class="list-entitys-container">
    <Table :loading="loading" :columns="columns" :data="result" @on-selection-change="selectChange"></Table>
    <Form class="edit-entitys-wrap" v-if="Object.keys(editEntitys).length">
      <div class="edit-entitys-position" v-bind:style="{top: editEntitysTop + 'px'}">
        <entitys :item="editEntitys" successBtnText="确认" cancelBtnText="取消" @handleCancel="cancelEdit()" @handleSuccess="commitEdit()" />
      </div>
    </Form>
    <div class="gap-top">
      <Button type="warning" @click="addEntity">资料录入</Button>
      <Button type="info" @click="revertEntity">归还</Button>
      <Button type="default" @click="$router.back()">后退</Button>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import {
  FILTER_ENTITYS_ALL_LIST,
  REVERT_ENTITYS,
  UPDATE_ENTITYS,
  FETCH_COMPANY_LIST,
  SHOW_NOTIFY,
  SET_BREADCRUMB
} from '../store/types'

import Vue from 'vue'
import {object2entitys} from '../tools'

let selected = []

export default {
  name: 'ListEntity',
  props: ['companyId'],
  data () {
    return {
      loading: false,
      editEntitys: {},
      // 控制entitys组件的位置
      editEntitysTop: 0,
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
                  click: (event) => {
                    this.updateEntity(params.row, event)
                  }
                }
              }, '修改')
            ])
          }
        }
      ]
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
      return this.data.length ? this.data : []
    }
  },
  methods: {
    addEntity() {
      this.$router.push({name: 'BatchAddEntitys', params: {companyId: this.companyId}})
    },
    updateEntity(old, event) {
      this.editEntitysTop = this.getOffsetByTable(event)
      Vue.set(this, 'editEntitys', Object.assign({removed: false}, old))
    },
    cancelEdit() {
      Vue.set(this, 'editEntitys', {})
    },
    commitEdit() {
      const entitys = object2entitys(
        Object.assign({companyId: this.companyId}, this.editEntitys)
      )
      return this.$store.dispatch(UPDATE_ENTITYS, {datas: [entitys]})
        .then(this.getRevertedEntitys)
        .then(this.cancelEdit)
    },
    getOffsetByTable (event) {
      // 如果html结构改变，这里也需要做更改
      const tableElm = event.path[8]
      const bounding = tableElm.getBoundingClientRect()
      return event.clientY - bounding.top
    },
    // 将表格左边勾选好的记录下来，以便后续使用
    selectChange (change) {
      selected = change
    },
    getRevertedEntitys () {
      this.loading = true
      return this.$store.dispatch(
        FILTER_ENTITYS_ALL_LIST,
        {company_id: parseInt(this.companyId), status: '归还'}
      ).then(() => {
        this.loading = false
      })
    },
    revertEntity () {
      if (selected.length === 0) {
        this.$store.dispatch(SHOW_NOTIFY, {title: '还没选择归还物品', type: 'warning'})
        return
      }
      this.$store.dispatch(REVERT_ENTITYS, {selected: selected.map(x => x.id), company_id: parseInt(this.companyId)})
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
    this.getRevertedEntitys()
    this.$store.dispatch(FETCH_COMPANY_LIST, {id: parseInt(this.companyId)})
      .then(() => {
        const found = this.$store.getters.companyById(parseInt(this.companyId))
        this.$store.commit(SET_BREADCRUMB, {name: this.$options.name, title: found.title})
      })
  }
}
</script>
