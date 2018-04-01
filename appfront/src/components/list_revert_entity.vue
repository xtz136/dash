<template>
    <div>
        <Card>
            <Form :model="formItem">
            <Row>
                <Col span="6">
                    <Input v-model="formItem.order_id">
                        <span slot="prepend"> 归还编号：</span>
                    </Input>
                </Col>
                <Col span="6">
                    <Select clearable v-model="formItem.entity_id" placeholder="选择物品">
                      <Option v-for="entity in entityList" :key="entity.id" :value="entity.id">{{ entity.name }}</Option>
                    </Select>
                </Col>
                <Col span="6">
                    <Select
                          v-model="formItem.signer_id"
                          filterable remote clearable
                          :remote-method="handlePeopleSearch"
                          :loading="searchPeopleLoading"
                          placeholder="选择签收人">
                      <Option v-for="people in peoples" :key="people.id" :value="people.id">{{ people.name }}</Option>
                    </Select>
                </Col>
                <Col span="6">
                    <Select
                         v-model="formItem.borrower_id"
                         filterable remote clearable
                         :remote-method="handlePeopleSearch"
                         :loading="searchPeopleLoading"
                         placeholder="选择借用人">
                      <Option v-for="people in peoples" :key="people.id" :value="people.id">{{ people.name }}</Option>
                    </Select>
                </Col>
            </Row>

            <Row class-name="gap-top">
                <Col span="6">
                    <DatePicker
                        type="daterange"
                        v-model="formItem.sign_date"
                        placeholder="选择签收日期"
                        style="width: 100%">
                    </DatePicker>
                </Col>
                <Col span="6">
                    <DatePicker
                        type="daterange"
                        v-model="formItem.borrow_date"
                        placeholder="选择借用日期"
                        style="width: 100%">
                    </DatePicker>
                </Col>
                <Col span="6">
                    <DatePicker
                        type="daterange"
                        v-model="formItem.revert_date"
                        placeholder="选择归还日期"
                        style="width: 100%">
                    </DatePicker>
                </Col>
                <Col span="6">
                    <Input v-model="formItem.descript">
                        <span slot="prepend"> 备注：</span>
                    </Input>
                </Col>
            </Row>

            <Row class-name="gap-top">
                <Button type="info" @click="handleSearch()">搜索</Button>
                <Button type="default" @click="$router.back()">后退</Button>
            </Row>
            </Form>
        </Card>

        <div class="gap-top"> </div>

        <Table :loading="loading" :columns="columns" :data="data"></Table>
        <Page v-if="pagination.count > 0" :current="pagination.page" :total="pagination.count" class-name="gap-top" @on-change="handleSearch" show-elevator></Page>
    </div>
</template>

<script>
import {
  FILTER_ENTITYS_LIST,
  SHOW_NOTIFY,
  FILTER_ENTITY_LIST,
  FILTER_PEOPLES_LIST,
  SET_PAGINATION_PAGE,
  SET_PAGINATION_COUNT
} from '../store/types'

import {mapGetters} from 'vuex'
import {date2str} from '../tools'

export default {
  name: 'ListRevertEntity',
  props: ['companyId'],
  data () {
    return {
      loading: false,
      columns: [
        {type: 'index', align: 'center', width: 60},
        {title: '归还编号', key: 'order_id'},
        {title: '物品', key: 'entity'},
        {title: '数量', key: 'amount', width: 60},
        {title: '签收人', key: 'signer'},
        {title: '签收日期', key: 'sign_date'},
        {title: '借用人', key: 'borrower'},
        {title: '借用日期', key: 'borrow_date'},
        {title: '归还日期', key: 'revert_borrow_date'},
        {title: '状态', key: 'status', width: 60},
        {title: '备注', key: 'descript'}
      ],
      formItem: {
        order_id: undefined,
        entity_id: undefined,
        signer_id: undefined,
        sign_date: ['', ''],
        borrower_id: undefined,
        borrow_date: ['', ''],
        revert_date: ['', ''],
        descript: undefined
      },
      searchPeopleLoading: false
    }
  },
  computed: {
    pagination () {
      return this.$store.state.pagination.data
    },
    data () {
      return this.$store.getters.entitys
    },
    ...mapGetters(['entityList', 'peoples'])
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
            this.$store.dispatch(FILTER_PEOPLES_LIST, {name: value})
              .then(() => { this.searchPeopleLoading = false })
          }, 200)
        }
      }
    }()),
    handleSearch(pageNum = 1) {
      const signDate = this.formItem.sign_date.map(date2str).filter(x => x)
      const borrowDate = this.formItem.borrow_date.map(date2str).filter(x => x)
      const revertDate = this.formItem.revert_date.map(date2str).filter(x => x)

      const search = Object.assign({}, this.formItem, {
        sign_date: signDate.length ? signDate : undefined,
        borrow_date: borrowDate.length ? borrowDate : undefined,
        revert_date: revertDate.length ? revertDate : undefined,
        status: '归还',
        page: pageNum,
        company_id: this.companyId
      })

      this.loading = true
      this.$store.dispatch(FILTER_ENTITYS_LIST, search)
        .then(result => {
          this.$store.commit(SET_PAGINATION_PAGE, pageNum)
          this.$store.commit(SET_PAGINATION_COUNT, result.msg.count)
          this.loading = false
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
      this.handleSearch()
      this.$store.dispatch(FILTER_ENTITY_LIST)
    }
  }
}
</script>
