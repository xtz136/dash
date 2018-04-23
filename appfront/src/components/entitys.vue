<style scoped>
.fields {
    display: flex;
    padding: .5em;
    border: 1px solid #a5b0bb;
    border-radius: .5em;
}
.fields > .field-opt {
    width: 6em;
    margin-left: 1em;
    padding-left: 1em;
    border-left: 1px solid #b5ada8;
}
.fields > .field-opt > button {
    margin-top: 1em;
}

.ivu-select {
    width: auto;
}
.field {
    flex-grow: 1;
    display: flex;
    flex-wrap: wrap;
}
.field > .item {
    flex-grow: 1;
}
.ivu-select {
    width: auto;
}
</style>

<template>

<div class="fields">
    <div class="field">
        <div class="item">
            <FormItem label="物品：">
                <Select v-model="item.entity_id" filterable style="width: 10em">
                    <Option v-for="entity in entityList" :key="entity.id" :value="entity.id">{{ entity.name }}</Option>
                </Select>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="数量：">
                <InputNumber :min="0" v-model="item.amount" style="width: 5em"></InputNumber>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="签收人：">
                <Select v-model="item.signer_id" filterable remote :label="defaultFormSigner" :remote-method="handlePeopleSearch" :loading="searchPeopleLoading" style="width: 10em">
                    <Option v-for="people in peoples" :key="people.id" :value="people.id">{{ people.name }}</Option>
                </Select>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="签收日期：">
                <DatePicker type="date" :options="dateOptions" v-model="item.sign_date" style="width: 10em"></DatePicker>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="借用人：">
                <Select v-model="item.borrower_id" filterable remote :label="defaultFormBorrower" :remote-method="handlePeopleSearch" :loading="searchPeopleLoading" style="width: 10em">
                    <Option v-for="people in peoples" :key="people.id" :value="people.id">{{ people.name }}</Option>
                </Select>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="借用日期：">
                <DatePicker type="date" :options="dateOptions" v-model="item.borrow_date" style="width: 10em"></DatePicker>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="还回日期：">
                <DatePicker type="date" :options="dateOptions" v-model="item.revert_borrow_date" style="width: 10em"></DatePicker>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="归还日期：">
                <DatePicker type="date" :options="dateOptions" v-model="item.revert_date" style="width: 10em"></DatePicker>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="状态：">
                <Select v-model="item.status">
                    <Option value="寄存">寄存</Option>
                    <Option value="借出">借出</Option>
                    <Option value="归还">归还</Option>
                </Select>
            </FormItem>
        </div>
        <div class="item">
            <FormItem label="备注：">
                <Input v-model="item.descript" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
            </FormItem>
        </div>
    </div>
    <div class="field-opt">
        <Button type="ghost" @click="handleCancel">{{ cancelBtnText }}</Button>
        <Button type="ghost" @click="handleSuccess" v-if="successBtnText">{{ successBtnText }}</Button>
    </div>
</div>
</template>

<script>
import {
  FILTER_ENTITY_LIST,
  FILTER_PEOPLES_LIST
} from '../store/types'

import {mapGetters} from 'vuex'

export default {
  props: ['item', 'cancelBtnText', 'successBtnText'],
  data () {
    return {
      dateOptions: {
        shortcuts: [
          {
            text: '今天',
            value () { return new Date() }
          }
        ]
      },
      searchPeopleLoading: false,
      defaultFormSigner: this.item.signer || '',
      defaultFormBorrower: this.item.borrower || ''
    }
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
    handleCancel () {
      this.$emit('handleCancel')
    },
    handleSuccess () {
      this.$emit('handleSuccess')
    }
  },
  computed: mapGetters(['entityList', 'peoples']),
  created () {
    this.$store.dispatch(FILTER_ENTITY_LIST)
  }
}
</script>
