import BaseApi from './base.js'
import {createFakeData, fitData} from '../tools.js'

const datas = [
  {id: 1, first_name: '雇员1', last_name: ''},
  {id: 2, first_name: '雇员2', last_name: ''},
  {id: 3, first_name: '张三', last_name: ''},
  {id: 4, first_name: 'fake user', last_name: ''}
]

class PeopleApi extends BaseApi {
  fakeApiData (args) {
    switch (args.type) {
      case 'api_filter':
        return createFakeData(datas.filter(x => x.first_name.includes(args.name)))
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  genCustomField (data) {
    return Object.assign({name: `${data.last_name}${data.first_name}`}, data)
  }

  filter (args) {
    return this.fetch({type: 'api_filter', ...args})
      .then(fitData.bind(null, 'msg', this.genCustomField))
  }
}

const peopleApi = new PeopleApi('/borrow/api/people')

export default peopleApi
