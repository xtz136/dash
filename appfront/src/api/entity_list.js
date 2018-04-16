import BaseApi from './base.js'
import {createFakePageData, createFakeData} from '../tools.js'

const orderId = 'YH201804010010'

let datas = [
  {id: 1, entity: '证明', amount: 1, signer: 'admin', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '寄存', descript: 'test', entity_id: 3, signer_id: 1, borrower_id: 2, company_id: 1},
  {id: 4, entity: '身份证', amount: 1, signer: 'admin', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '寄存', descript: 'test', entity_id: 3, signer_id: 1, borrower_id: 2, company_id: 1},
  {id: 5, entity: '证明', amount: 1, signer: 'admin', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '寄存', descript: 'test', entity_id: 3, signer_id: 1, borrower_id: 2, company_id: 1},
  {id: 6, entity: '证明', amount: 1, signer: 'admin', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '寄存', descript: 'test', entity_id: 3, signer_id: 1, borrower_id: 2, company_id: 1},
  {id: 7, entity: '身份证', amount: 1, signer: 'admin', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '寄存', descript: 'test', entity_id: 3, signer_id: 1, borrower_id: 2, company_id: 1, order_id: orderId},
  {id: 2, entity: '护照', amount: 2, signer: '雇员2', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '归还', descript: 'test', entity_id: 2, signer_id: 3, borrower_id: 2, company_id: 1, order_id: orderId},
  {id: 3, entity: '证明', amount: 2, signer: '雇员2', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '归还', descript: 'test', entity_id: 2, signer_id: 3, borrower_id: 2, company_id: 2, order_id: orderId}
]

class EntityListApi extends BaseApi {
  fakeApiData (args) {
    switch (args.type) {
      case 'api_get_revert':
        return createFakeData(datas.filter(x => x.order_id === args.order_id))
      case 'api_filter':
        return createFakePageData(datas.filter(x => x.company_id === args.company_id && x.status === args.status))
      case 'api_filter_all':
        return createFakeData(datas.filter(x => x.company_id === args.company_id && x.status !== args.status))
      case 'api_update':
        datas = Array.prototype.concat.call([], datas, args.datas)
        return createFakeData(true)
      case 'api_revert':
        const found = datas.filter(x => args.selected.includes(x.id))
        if (found) {
          found.forEach(x => {
            x['status'] = '归还'
            x['order_id'] = orderId
          })
          return createFakeData(orderId)
        } else {
          return this.fakeApiData({type: 'default'})
        }
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  filter (args) {
    return this.fetch({type: 'api_filter', ...args})
  }

  filterAll (args) {
    return this.fetch({type: 'api_filter_all', ...args})
  }

  update (args) {
    return this.fetch({type: 'api_update', ...args})
  }

  revert (args) {
    return this.fetch({type: 'api_revert', ...args})
  }

  getRevert (args) {
    return this.fetch({type: 'api_get_revert', ...args})
  }
}

const entityListApi = new EntityListApi('/borrow/api/entity_list')

export default entityListApi
