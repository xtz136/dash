<style scoped>
.header {
    height: 90px;
}

.nav {
    display: flex;
    flex-direction: row;
}

.nav .nav-item {
    flex-grow: 0;
}

.width20 {
    width: 20%;
}

.width25 {
    width: 25%;
}

.width50 {
    width: 50%;
}

.width55 {
    width: 55%;
}

.height-half {
    height: 50%;
}

.doub-h2-lh {
    line-height: 2.8em;
}

.logo {
    width: 80px;
    height: 80px;
    float: left;
    margin-right: 1em;
}

.table {
    padding: 2em 0em;
    display: flex;
    flex-direction: row;

}

table {
    width: 100%;
}

table td {
    text-align:center;
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
      <div class="header nav">
          <div class="nav-item width20">
          </div>
          <div class="nav-item width55">
              <img class="logo" :src="$store.state.config.logoImg" />
              <h2 class="height-half"> {{ $store.state.config.companyName }} </h2>
              <h2 class="height-half"> 客户证件（资料）交接表 </h2>
          </div>
          <div class="nav-item width25">
              <div class="height-half doub-h2-lh"> 编号：{{ orderId }} </div>
              <div class="height-half doub-h2-lh"> {{ now.getFullYear() }} 年 {{ now.getMonth() + 1 }} 月 {{ now.getDate() }} 日 </div>
          </div>
      </div>

      <h2>今收到（交还）<u>{{ client.title }}</u> 证件（资料）如下：</h2>

      <div class="table">
          <div class="width50">
              <table border="1" cellspacing="0">
                  <thead>
                      <tr>
                          <th>序号</th>
                          <th>物品</th>
                          <th>数量</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(item, i) in entitysLeft" :key="i">
                          <td>{{ i + 1 }}</td>
                          <td>{{ item.entity }}</td>
                          <td>{{ item.amount }}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
          <div class="width50">
              <table border="1" cellspacing="0" style="border-left: 0">
                  <thead>
                      <tr>
                          <th>序号</th>
                          <th>物品</th>
                          <th>数量</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(item, i) in entitysRight" :key="i">
                          <td>{{ i + 1 + entitysLeft.length }}</td>
                          <td>{{ item.entity }}</td>
                          <td>{{ item.amount }}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>

      <div class="gap-top">
          <div class="nav">
            <span class="nav-item width50">以上证件（资料）共计：<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>&nbsp;项</span>
            <span class="nav-item width25">接收人：</span>
            <span class="nav-item width25">移交人：</span>
          </div>
          <div class="nav">
            <span class="nav-item width50">负责人：{{ client.contactor }}</span>
            <span class="nav-item width50">网址：www.gzyhcs.com</span>
          </div>
          <div class="nav">
            <span class="nav-item width50">负责人电话：{{ client.contactor_phone }}</span>
            <span class="nav-item width50">咨询电话：020-87313109</span>
          </div>
          <div class="nav">
            <span class="nav-item width50">客户地址：{{ client.address }}</span>
            <span class="nav-item width50">地址：广州越秀区永福路8号永怡新都808室</span>
          </div>
      </div>

      <Button type="info" @click="startPrint">开始打印</Button>

    </div>
  </div>
</template>

<script>
import {
  FETCH_COMPANY_LIST
} from '../store/types'

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
      return this.$store.getters.companyById(parseInt(this.companyId)) || {}
    }
  },
  methods: {
    startPrint () {
      window.print()
    }
  },
  created () {
    // 最低需要有20个entitys，如果不够，添加空的entity
    // 如果多于20个，就加4个空的entity，预留位置给手动添加项目
    const entityLength = Math.max(this.entitys.length + (this.entitys.length % 2 ? 5 : 4), 10)
    const all = Array.from(
      {length: entityLength},
      (v, i) => this.entitys[i] || {entity: '', amount: ''})
    this.entitysLeft = all.slice(0, entityLength / 2)
    this.entitysRight = all.slice(entityLength / 2)
    this.$store.dispatch(FETCH_COMPANY_LIST, {id: this.companyId})
  }
}
</script>
