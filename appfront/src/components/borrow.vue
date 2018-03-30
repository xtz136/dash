<template>
  <div>
  <Content class="content">
      <Breadcrumb class="breadcrumb">
          <BreadcrumbItem v-for="bc in bcs" :key="bc.id">{{ bc.title }}</BreadcrumbItem>
      </Breadcrumb>
      <Card>
          <div style="min-height: 200px;">
          <router-view></router-view>
          </div>
      </Card>
  </Content>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
</style>
