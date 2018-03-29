import BaseApi from './base.js'
import {createFakePageData} from '../tools.js'

class EntityApi extends BaseApi {
  fakeApiData (data) {
    switch (data.type) {
      case 'api_list':
        return createFakePageData([
          {id: 1, name: '身份证'},
          {id: 2, name: '护照'},
          {id: 3, name: '证明'}
        ])
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  list () {
    return this.fetch({type: 'api_list'})
      .then(x => x.msg)
  }
}

const entityApi = new EntityApi('/borrow/api/entity')

export default entityApi
