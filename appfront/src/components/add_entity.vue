<template>
<div>
<Form :model="formItem" :label-width="80">
  <FormItem label="物品">
    <Select v-model="formItem.entity_id">
      <Option v-for="entity in entitys" :key="entity.id" :value="entity.id">{{ entity.name }}</Option>
    </Select>
  </FormItem>
  <FormItem label="数量">
    <InputNumber :min="0" v-model="formItem.amount"></InputNumber>
  </FormItem>
  <FormItem label="签收人">
    <Select v-model="formItem.signer_id" filterable remote :remote-method="handlePeopleSearch" :loading="searchPeopleLoading">
      <Option v-for="people in peoples" :key="people.id" :value="people.id">{{ people.name }}</Option>
    </Select>
  </FormItem>
  <FormItem label="签收时间">
    <DatePicker type="date" :options="dateOptions" v-model="formItem.sign_date"></DatePicker>
  </FormItem>
  <FormItem label="借用人">
    <Select v-model="formItem.borrower_id" filterable remote :remote-method="handlePeopleSearch" :loading="searchPeopleLoading">
      <Option v-for="people in peoples" :key="people.id" :value="people.id">{{ people.name }}</Option>
    </Select>
  </FormItem>
  <FormItem label="借用日期">
    <DatePicker type="date" :options="dateOptions" v-model="formItem.borrow_date"></DatePicker>
  </FormItem>
  <FormItem label="还回日期">
    <DatePicker type="date" :options="dateOptions" v-model="formItem.revert_borrow_date"></DatePicker>
  </FormItem>
  <FormItem label="归还日期">
    <DatePicker type="date" :options="dateOptions" v-model="formItem.revert_date"></DatePicker>
  </FormItem>
  <FormItem label="状态">
    <Select v-model="formItem.status">
        <Option value="寄存">寄存</Option>
        <Option value="借出">借出</Option>
        <Option value="归还">归还</Option>
    </Select>
  </FormItem>
  <FormItem label="备注">
    <Input v-model="formItem.descript" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
  </FormItem>
  <FormItem>
    <Button type="primary" @click="addEntity">提交</Button>
    <Button type="ghost" style="margin-left: 8px" @click="$router.back()">取消</Button>
  </FormItem>
</Form>
<Spin size="large" fix v-if="spinShow"></Spin>
<Modal
  v-model="addEntityListModal"
  title="提交成功"
  @on-cancel="$router.back()"
  @on-ok="$router.back()">
  <p>资料录入成功</p>
</Modal>
</div>
</template>

<script>
const date2str = function(date) {
  return date
    ? `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    : date
}

export default {
  props: ['companyId'],
  data() {
    return {
      formItem: {
        entity_id: '',
        amount: 0,
        signer_id: '',
        sign_date: '',
        borrower_id: '',
        borrow_date: '',
        revert_borrow_date: '',
        revert_date: '',
        status: '寄存',
        descript: ''
      },
      dateOptions: {
        shortcuts: [
          {
            text: '今天',
            value () { return new Date() }
          }
        ]
      },
      spinShow: true,
      searchPeopleLoading: false,
      addEntityListModal: false
    }
  },
  computed: {
    entitys () {
      return this.$store.getters.entitys
    },
    peoples () {
      return this.$store.getters.peoples
    }
  },
  methods: {
    handlePeopleSearch: (function () {
      let syncId
      return function (value) {
        if (value !== '') {
          if (syncId) clearTimeout(syncId)
          syncId = setTimeout(() => {
            syncId = undefined
            this.searchPeopleLoading = true
            this.$store.dispatch('filterPeoples', {name: value})
              .then(() => { this.searchPeopleLoading = false })
          }, 200)
        }
      }
    }()),
    addEntity () {
      const entityList = Object.assign({}, this.formItem, {
        sign_date: date2str(this.formItem.sign_date),
        borrow_date: date2str(this.formItem.borrow_date),
        revert_borrow_date: date2str(this.formItem.revert_borrow_date),
        revert_date: date2str(this.formItem.revert_date),
        company_id: this.companyId
      })
      this.spinShow = true
      console.log('addEntityList', entityList)
      this.$store.dispatch('addEntityList', {entityList})
        .then(() => {
          this.spinShow = false
          this.addEntityListModal = true
        })
    }
  },
  created () {
    this.$store.dispatch('fetchEntitys').then(() => { this.spinShow = false })
  }
}
</script>
