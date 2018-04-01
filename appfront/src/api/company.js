import BaseApi from './base.js'
import {createFakePageData, fitData} from '../tools.js'

const fakeDatas = [
  {id: 1, title: '部落胜利有限公司', address: '地球某地', saleman: '小皮球', bookkeeper: '', industry: '', taxpayer_type: '', license_status: '有效', status: '有效', contactor: '洛瑟玛·塞隆', contactor_phone: '12345678901'},
  {id: 2, title: '亡灵大叫有限公司', address: '地球某地', saleman: '不穿衣', bookkeeper: '', industry: '', taxpayer_type: '', license_status: '有效', status: '有效', contactor: '希尔瓦娜斯·风行者', contactor_phone: '12345678901'},
  {id: 3, title: '联盟太衰有限公司', address: '地球某地', saleman: '性感猫咪', bookkeeper: '', industry: '', taxpayer_type: '', license_status: '有效', status: '有效', contactor: '瓦里安·乌瑞恩国王', contactor_phone: '12345678901'}
]

class CompanyApi extends BaseApi {
  fakeApiData (args) {
    switch (args.type) {
      case 'api_filter':
        const pageSize = 2
        let datas = fakeDatas
        if (args.title) {
          datas = datas.filter(x => x.title.includes(args.title))
        }
        const count = datas.length
        const start = pageSize * (args.page - 1)
        const result = datas.slice(start, start + pageSize)
        return createFakePageData(result, count)
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  genCustomField (data) {
    return Object.assign({contactor_info: `${data.contactor} ${data.contactor_phone}`}, data)
  }

  filter (args) {
    return this.fetch({type: 'api_filter', ...args})
      .then(fitData.bind(null, 'msg.datas', this.genCustomField))
  }
}

const companyApi = new CompanyApi('/borrow/api/company')

export default companyApi
