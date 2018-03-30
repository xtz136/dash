import BaseApi from './base.js'
import {createFakePageData} from '../tools.js'

const datas = [
  {id: 1, first_name: '雇员1', last_name: ''},
  {id: 2, first_name: '雇员2', last_name: ''},
  {id: 3, first_name: '张三', last_name: ''},
  {id: 4, first_name: 'fake user', last_name: ''}
]

class PeopleApi extends BaseApi {
  fakeApiData (data) {
    switch (data.type) {
      case 'api_filter':
        return createFakePageData(datas.filter(x => x.first_name.includes(data.data.name)))
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  genCustomField (data) {
    return Object.assign({name: `${data.first_name} ${data.last_name}`}, data)
  }

  filter (data) {
    return this.fetch({type: 'api_filter', data})
      .then(x => x.msg)
      .then(x => Object({datas: x.datas.map(this.genCustomField)}, x))
  }
}

const peopleApi = new PeopleApi('/borrow/api/people')

export default peopleApi
