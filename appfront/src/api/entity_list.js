import BaseApi from './base.js'
import {createFakePageData} from '../tools.js'

const datas = [
  {id: 1, entity: '证明', amount: 1, signer: 'admin', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '寄存', descript: 'test', company_id: '1'},
  {id: 2, entity: '护照', amount: 2, signer: '雇员2', sign_date: '2018-03-08', borrower: '雇员1', borrow_date: '2018-03-11', revert_borrow_date: '2018-04-11', revert_date: '2018-04-23', status: '归还', descript: 'test', company_id: '2'}
]

class EntityListApi extends BaseApi {
  fakeApiData (data) {
    switch (data.type) {
      case 'api_list':
        return createFakePageData(datas)
      case 'api_filter':
        return createFakePageData(datas.filter(x => x.company_id === data.data.companyId))
      case 'api_add':
        return createFakePageData(true)
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  list () {
    return this.fetch({type: 'api_list'})
      .then(x => x.msg)
  }

  filter (data) {
    return this.fetch({type: 'api_filter', data})
      .then(x => x.msg)
  }

  add (data) {
    return this.fetch({type: 'api_add', data})
      .then(x => x.msg)
  }
}

const entityListApi = new EntityListApi('/borrow/api/entity_list')

export default entityListApi
