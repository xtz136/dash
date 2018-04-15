<template>
    <div>
        <Card>
            <Form :model="search">
              <Row>
                  <Col span="8">
                      <Input v-model="search.order_id">
                          <span slot="prepend"> 归还编号：</span>
                      </Input>
                  </Col>
                  <Col span="8">
                      <Input v-model="search.company">
                          <span slot="prepend"> 公司：</span>
                      </Input>
                  </Col>
                  <Col span="8">
                    <Button type="info" @click="handleSearch()">搜索</Button>
                    <Button type="default" @click="$router.back()">后退</Button>
                  </Col>
              </Row>
            </Form>
        </Card>

        <div class="gap-top"> </div>

        <Table :loading="loading" :columns="columns" :data="revertList"></Table>
        <Page v-if="pagination.count > 0" :current="pagination.page" :total="pagination.count" class-name="gap-top" @on-change="handleSearch" show-elevator></Page>
    </div>
</template>

<script>
import {
  FILTER_REVERTLIST,
  GET_ENTITYS_REVERT,
  SET_PAGINATION_PAGE,
  SET_PAGINATION_COUNT
} from '../store/types'

import {mapGetters} from 'vuex'

export default {
  name: 'ListRevertEntity',
  data () {
    return {
      loading: false,
      columns: [
        {type: 'index', align: 'center', width: 60},
        {title: '公司', key: 'company'},
        {title: '归还编号', key: 'order_id', width: 150},
        {title: '归还日期', key: 'revert_borrow_date', width: 120},
        {
          title: '操作',
          key: 'action',
          align: 'center',
          width: 80,
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {type: 'primary', size: 'small'},
                on: {
                  click: () => {
                    this.handleShowDetails(params.row)
                  }
                }
              }, '详情')
            ])
          }
        }
      ],
      search: {
        order_id: undefined,
        company: ''
      }
    }
  },
  computed: {
    pagination () {
      return this.$store.state.pagination.data
    },
    ...mapGetters(['revertList', 'entitys'])
  },
  methods: {
    handleSearch(pageNum = 1) {
      const search = Object.assign({}, this.search, {
        page: pageNum
      })

      this.loading = true
      this.$store.dispatch(FILTER_REVERTLIST, search)
        .then(result => {
          this.$store.commit(SET_PAGINATION_PAGE, pageNum)
          this.$store.commit(SET_PAGINATION_COUNT, result.msg.count)
          this.loading = false
        })
    },
    handleShowDetails (data) {
      this.$store.dispatch(GET_ENTITYS_REVERT, {'order_id': data.order_id, 'id': data.id})
        .then(() => {
          this.$router.push({name: 'Print2',
            params: {
              entitys: this.entitys,
              companyId: data.company_id,
              orderId: data.order_id
            }
          })
        })
    }
  },
  created () {
    this.handleSearch()
  }
}
</script>
