<style scoped>
.header {
    height: 90px;
    display: flex;
    flex-direction: row;
}

.logo {
    width: 90px;
    height: 100%;
    flex-grow: 0;
}

.other {
    margin-left: 2em;
    width: auto;
    height: 100%;
    flex-grow: 1;
}

.other .ivu-row {
    height: 45px;
}

.table {
    padding: 2em 0em;
}

.row {
    margin-top: .5em;
}

.print {
    width: 700px;
    margin: 0 auto;
}

@media print {
    .wrapp-print {
        position: fixed;
        top: 0px;
        left: 0px;
        width: 100vw;
        height: 100vh;
        background-color: white;
        z-index: 1000;
    }
    .print > button {
        display: none;
    }
}
</style>

<template>
  <div class="wrapp-print">
    <div class="print">
      <div class="header">
          <img class="logo" :src="$store.state.config.logoImg" />
          <div class="other">
              <Row>
                  <Col span="16"> <h2>{{ $store.state.config.companyName }}</h2> </Col>
                  <Col span="8"> 编号：{{ orderId }} </Col>
              </Row>
              <Row>
                  <Col span="16"> <h2>客户证件（资料）交接表</h2> </Col>
                  <Col span="8"> {{ now.getFullYear() }} 年 {{ now.getMonth() + 1 }} 月 {{ now.getDate() }} 日 </Col>
              </Row>
          </div>
      </div>

      <h2>今收到（交还）<span>{{ client.title }}</span> 证件（资料）如下：</h2>

      <div class="table">
        <Table :columns="columns" :data="entitys" ></Table>
      </div>

      <div class="gap-top">
          <Row>
            <Col span="12">以上证件（资料）共计：<span>{{ entitys.length}}</span> 项</Col>
            <Col span="6">接收人：</Col>
            <Col span="6">移交人：</Col>
          </Row>
          <Row class-name="row">
            <Col span="12">负责人：{{ client.contactor }}</Col>
            <Col span="12">网址：www.gzyhcs.com</Col>
          </Row>
          <Row class-name="row">
            <Col span="12">负责人电话：{{ client.contactor_phone }}</Col>
            <Col span="12">咨询电话：020-87313109</Col>
          </Row>
          <Row class-name="row">
            <Col span="12">客户地址：{{ client.address }}</Col>
            <Col span="12">地址：广州越秀区永福路8号永怡新都808室</Col>
          </Row>
      </div>

      <Button type="info" @click="startPrint">开始打印</Button>

    </div>
  </div>
</template>

<script>
import {SHOW_NOTIFY} from '../store/types'

export default {
  name: 'Print',
  props: ['entitys', 'companyId', 'orderId'],
  data () {
    return {
      columns: [
        {type: 'index', align: 'center', width: 60},
        {title: '物品', key: 'entity'},
        {title: '数量', key: 'amount', width: 60}
      ],
      now: new Date()
    }
  },
  computed: {
    client () {
      return this.$store.getters.companyById(parseInt(this.companyId))
    }
  },
  methods: {
    startPrint () {
      window.print()
    }
  },
  created () {
    if (!this.companyId || !this.orderId) {
      this.$store.dispatch(SHOW_NOTIFY, {title: '参数错误', type: 'error', duration: 0})
    }
  }
}
</script>
