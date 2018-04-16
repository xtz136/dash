<style>
html, body {
    height: 100%;
}

.gap-top {
  margin-top: 1em;
}

.gap-buttom {
  margin-buttom: 1em;
}
</style>

<style scoped>
.ivu-layout {
    height: 100%;
}
.layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    height: 100%;
}
.layout-logo{
    width: 60px;
    height: 60px;
    border-radius: 3px;
    float: left;
    position: relative;
    left: 20px;
}
.layout-company-name{
    height: 60px;
    background: #5b6270;
    border-radius: 3px;
    float: left;
    position: relative;
    left: 20px;
    color: white;
    padding: 0 .5em;
}
.layout-nav{
    width: 420px;
    margin: 0 auto;
    margin-right: 20px;
}
.layout-footer-center{
    text-align: center;
}
.layout .content {
    padding: 0 50px;
}
.ivu-menu-item a {
    color: rgba(255,255,255,.7);
}
.ivu-menu-item.ivu-menu-item-active a {
    color: #fff;
}
</style>

<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1">
                    <img class="layout-logo" :src="$store.state.config.logoImg" />
                    <div class="layout-company-name">{{ $store.state.config.companyName }}</div>
                    <div class="layout-nav">
                        <MenuItem name="1"> <Icon type="ios-navigate"></Icon> <router-link to="/company">资料录入</router-link> </MenuItem>
                        <MenuItem name="2"> <Icon type="ios-navigate"></Icon> <router-link to="/revertentitys">资料归还单</router-link> </MenuItem>
                        <MenuItem name="3"> <Icon type="ios-keypad"></Icon> <a target="_blank" :href="$store.state.config.adminUrl">管理后台</a> </MenuItem>
                    </div>
                </Menu>
            </Header>
            <router-view></router-view>
            <Footer class="layout-footer-center">2018 &copy; {{ $store.state.config.companyName }}</Footer>
        </Layout>
    </div>
</template>

<script>
export default {
  computed: {
  }
}
</script>
