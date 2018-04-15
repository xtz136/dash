<template>
<div>

<Form ref="formItems" :model="formItems">
    <FormItem
            v-for="(formItem, index) in formItems.items"
            v-if="!formItem.removed"
            :key="index">
        <entitys :item="formItem" cancelBtnText="删除" @handleCancel="handleRemove(index)" />
    </FormItem>
    <FormItem>
        <Button type="dashed" long @click="handleAdd" icon="plus-round" style="width: 100px;">添加</Button>
    </FormItem>
    <FormItem>
        <Button type="primary" @click="handleSubmit('formItems')">提交</Button>
        <Button type="ghost" @click="$router.back()" style="margin-left: 8px">取消</Button>
    </FormItem>
</Form>

<Spin size="large" fix v-if="spinShow"></Spin>
</div>
</template>

<script>
import {
  UPDATE_ENTITYS,
  SHOW_NOTIFY
} from '../store/types'

import {object2entitys} from '../tools'

export default {
  props: ['companyId'],
  data() {
    return {
      defaultFormItem: {
        entity_id: '',
        amount: 0,
        signer_id: '',
        sign_date: undefined,
        borrower_id: undefined,
        borrow_date: undefined,
        revert_borrow_date: undefined,
        revert_date: undefined,
        status: '寄存',
        descript: '',
        removed: false
      },
      formItems: {
        items: []
      },
      spinShow: false
    }
  },
  methods: {
    addEntitys () {
      const datas = this.formItems.items
        .filter(x => !x.removed && x.entity_id)
        .map(x => object2entitys(Object.assign({companyId: this.companyId}, x)))

      if (!datas.length) {
        return Promise.reject(new Error('请至少添加一条资料'))
      } else {
        return this.$store.dispatch(UPDATE_ENTITYS, {datas})
      }
    },
    handleSubmit (name) {
      this.spinShow = true
      this.addEntitys().then(() => {
        this.spinShow = false
        this.$store.dispatch(SHOW_NOTIFY, {title: '提交成功', type: 'info'})
        this.$router.back()
      }).catch(error => {
        this.spinShow = false
        this.$store.dispatch(SHOW_NOTIFY, {title: '提交错误', desc: error, type: 'error'})
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    handleAdd () {
      this.formItems.items.push(Object.assign({}, this.defaultFormItem))
    },
    handleRemove (index) {
      this.formItems.items[index].removed = true
    }
  },
  created () {
    this.handleAdd()
  }
}
</script>
