<template>
  <Content class="content">
      <Breadcrumb class="breadcrumb">
          <BreadcrumbItem
            v-for="(route, index) in $route.matched"
            v-if="!route.meta.bcSkip"
            :key="index">
          {{$store.state.breadcrumb.data[
              route.meta.bcName || route.name
            ] || route.meta.title
          }}
          </BreadcrumbItem>
      </Breadcrumb>
      <Card>
            <router-view></router-view>
      </Card>
  </Content>
</template>

<script>
export default {
}
</script>

<style scoped>
.breadcrumb {
  margin: 20px 0;
}
.content {
  display: flex;
  flex-direction: column;
}
.content .ivu-card {
  flex: auto;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
