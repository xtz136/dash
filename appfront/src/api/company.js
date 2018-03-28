import BaseApi from './base.js'
import {createFakePageData} from '../tools.js'

class CompanyApi extends BaseApi {
  fakeApiData (data) {
    switch (data.type) {
      case 'api_list':
        return createFakePageData([
          {id: 1, title: '部落胜利有限公司', address: '地球某地', salesman: '', bookkeeper: '', industry: '', taxpayer_type: '', license_status: '有效', status: '有效', contactor: '', contactor_phone: ''},
          {id: 2, title: '亡灵大叫有限公司', address: '地球某地', salesman: '', bookkeeper: '', industry: '', taxpayer_type: '', license_status: '有效', status: '有效', contactor: '', contactor_phone: ''}
        ])
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  genCustomField (data) {
    return Object.assign({contactor_info: `${data.contactor} ${data.contactor_phone}`}, data)
  }

  list () {
    return this.fetch({type: 'api_list'})
      .then(x => x.msg)
      .then(x => Object({datas: x.datas.map(this.genCustomField)}, x))
  }
}

const companyApi = new CompanyApi('/borrow/api/company')

export default companyApi
