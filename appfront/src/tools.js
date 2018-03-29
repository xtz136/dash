const toReqHeader = function (data, extra = {}) {
  let params = new URLSearchParams()
  for (let key of Object.keys(data)) {
    params.append(key, data[key] instanceof Object ? JSON.stringify(data[key]) : data[key])
  }
  extra['Accept'] = 'application/json'
  extra['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'

  return {
    method: 'POST',
    body: params,
    headers: extra
  }
}

/**
 * 自定义fetch函数，支持csrf
 */
const myfetch = function (url, data = {}, options = {}) {
  let defaultOpt = {
    method: 'POST',
    cache: 'no-cache',
    credentials: 'include'
  }
  let headers = {}
  let tokenInput = document.querySelector('input[name=csrfmiddlewaretoken]')

  options = toReqHeader(data, options)

  if (tokenInput) {
    headers['X-CSRFToken'] = tokenInput.value
  }

  if (options.headers) {
    headers = Object.assign({}, headers, options.headers || {})
  }

  return fetch(url, Object.assign(defaultOpt, options, {headers}))
}

/**
 * 方便构造测试数据
 */
const createFakePageData = function (datas) {
  return {
    status: true,
    code: 0,
    msg: {
      count: 1,
      page_count: 1,
      page: 1,
      has_prev: false,
      has_next: false,
      datas: datas
    }
  }
}

export {myfetch, createFakePageData}
