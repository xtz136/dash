import BaseApi from './base.js'
import {createFakePageData} from '../tools.js'

let datas = [
  {id: 1, company: '部落胜利有限公司', company_id: 1, order_id: 'YH201804010010', revert_borrow_date: '2018-04-12'},
  {id: 2, company: '部落胜利有限公司', company_id: 1, order_id: 'YH201804010011', revert_borrow_date: '2018-04-13'},
  {id: 3, company: '亡灵大叫有限公司', company_id: 2, order_id: 'YH201804010012', revert_borrow_date: '2018-04-14'}
]

class RevertListApi extends BaseApi {
  fakeApiData (args) {
    switch (args.type) {
      case 'api_filter':
        return createFakePageData(datas)
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  filter (args) {
    return this.fetch({type: 'api_filter', ...args})
  }
}

const entityListApi = new RevertListApi('/borrow/api/revert_list')
export default entityListApi
