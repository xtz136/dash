import {SHOW_NOTIFY} from './types'
import {Notice} from 'iview'

const notifys = {
  info: Notice.info,
  success: Notice.success,
  warning: Notice.warning,
  error: Notice.error,
  default: Notice.open
}

const displayNotify = function ({type = 'default', title, desc = '', duration = 4.5}) {
  return new Promise((resolve) => {
    notifys[type].call(Notice, {title, desc, duration, onClose: resolve})
  })
}

export default {
  state: {
  },
  actions: {
    [SHOW_NOTIFY] (state, data) {
      return displayNotify.call(this, data)
    }
  }
}
