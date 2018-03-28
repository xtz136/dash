<style>
html, body {
    height: 100%;
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
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
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
.layout .breadcrumb {
    margin: 20px 0;
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
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <MenuItem name="1"> <Icon type="ios-navigate"></Icon> <router-link to="/list-company">借阅</router-link> </MenuItem>
                        <MenuItem name="2"> <Icon type="ios-keypad"></Icon> <a target="_blank" :href="$store.state.config.adminUrl">管理后台</a> </MenuItem>
                    </div>
                </Menu>
            </Header>
            <Content class="content">
                <Breadcrumb class="breadcrumb">
                    <BreadcrumbItem>借阅</BreadcrumbItem>
                </Breadcrumb>
                <Card>
                    <div style="min-height: 200px;">
                        <router-view></router-view>
                    </div>
                </Card>
            </Content>
            <Footer class="layout-footer-center">2017-2018 &copy; nobody</Footer>
        </Layout>
    </div>
</template>

<script>
export default {
}
</script>
