import BaseApi from './base.js'
import {createFakeData} from '../tools.js'

class EntityApi extends BaseApi {
  fakeApiData (args) {
    switch (args.type) {
      case 'api_filter':
        return createFakeData([
          {id: 1, name: '身份证'},
          {id: 2, name: '护照'},
          {id: 3, name: '证明'}
        ])
      default:
        return {status: false, code: -100, msg: ''}
    }
  }

  filter () {
    return this.fetch({type: 'api_filter'})
  }
}

const entityApi = new EntityApi('/borrow/api/entity')

export default entityApi
