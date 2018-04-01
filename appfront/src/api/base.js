import {myfetch} from '../tools.js'

const toJSON = x => x.json()

class BaseApi {
  constructor (url) {
    this._url = url
  }

  /**
   * 返回后端接口的测试数据，为了测试
   */
  fakeApiData (/* data, header */) {
    return {status: true, msg: '', code: 0}
  }

  _fakeApiData (...args) {
    console.log('fetch api: ', this.constructor.name, args)
    return this.fakeApiData(...args)
  }

  /**
   * 向后端请求接口的方法
   *
   * 可以通过变量 _devMode 切换开发模式，开发模式返回假数据，不去后端请求
   */
  fetch(data = {}, header = {}) {
    return this._devMode
      ? Promise.resolve(this._fakeApiData(data, header))
      : myfetch(this._url, data, header).then(toJSON)
  }
}

BaseApi.prototype._devMode = false

export default BaseApi
