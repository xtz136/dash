<template>
  <div>
    <Table :columns="columns" :data="data"></Table>
    <Button type="warning" @click="addEntity">资料录入</Button>
    <Button type="default" @click="$router.back()">后退</Button>
  </div>
</template>

<script>
export default {
  name: 'ListEntity',
  props: ['companyId'],
  data () {
    return {
      columns: [
        {type: 'index', align: 'center'},
        {title: '物品', key: 'entity'},
        {title: '数量', key: 'amount'},
        {title: '签收人', key: 'signer'},
        {title: '签收日期', key: 'sign_date'},
        {title: '借用人', key: 'borrower'},
        {title: '借用日期', key: 'borrow_date'},
        {title: '归还日期', key: 'revert_borrow_date'},
        {title: '状态', key: 'status'},
        {title: '备注', key: 'descript'}
      ],
      addEntityModal: false
    }
  },
  methods: {
    addEntity() {
      this.$router.push({name: 'AddEntity', params: {companyId: this.companyId}})
    }
  },
  computed: {
    data () {
      return this.$store.getters.entityList
    }
  },
  created () {
    this.$store.dispatch('filterEntityList', {companyId: this.companyId})
  }
}
</script>
