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
const myfetch = function (url, {type, ...data}, options = {}) {
  let defaultOpt = {
    method: 'POST',
    cache: 'no-cache',
    credentials: 'include'
  }
  let headers = {}
  let tokenInput = document.querySelector('input[name=csrfmiddlewaretoken]')

  options = toReqHeader({type, data}, options)

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
const createFakePageData = function (datas, count) {
  return {
    status: true,
    code: 0,
    msg: {
      count: count || datas.length,
      page_count: 1,
      page: 1,
      has_prev: false,
      has_next: false,
      datas: copy(datas)
    }
  }
}

/**
 * 方便构造测试数据
 */
const createFakeData = function (datas) {
  return {
    status: true,
    code: 0,
    msg: copy(datas)
  }
}

/**
 * 方便修改接口的返回的列表
 */
const fitData = function(path, cb, data) {
  if (data.code === -1) {
    return data
  }

  const paths = path.split('.')
  const [last] = paths.slice(-1)
  const maybe = paths.slice(0, -1).reduce((a, b) => a ? a[b] : null, data)
  if (maybe) {
    maybe[last] = maybe[last].map(cb)
  }
  return data
}

/**
 * 复制 object 类型
 */
const copy = function(source) {
  if (typeof source === 'object') {
    if (source.length) {
      return source.map(copy)
    } else {
      return {...source}
    }
  }

  return source
}

/**
 * 将日期格式转为后端可以识别的格式
 */
const date2str = function(date) {
  return date
    ? `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    : date
}

/**
 * 清洗归还单的数据结构
 */
const object2entitys = function(obj) {
  return {
    id: obj.id,
    company_id: parseInt(obj.companyId),
    amount: obj.amount,
    borrower_id: obj.borrower_id,
    entity_id: obj.entity_id,
    signer_id: obj.signer_id,
    sign_date: date2str(obj.sign_date || undefined),
    borrow_date: date2str(obj.borrow_date || undefined),
    revert_borrow_date: date2str(obj.revert_borrow_date || undefined),
    revert_date: date2str(obj.revert_date || undefined),
    descript: obj.descript,
    status: obj.status
  }
}

export {myfetch, createFakePageData, createFakeData, fitData, date2str, object2entitys}
