import axiosInstance from '../AxiosClient'
import { createApi, createCollectionManager } from '@thinknimble/tn-models'
import { printerShape } from './models'

export const printerApi = createApi({
  client: axiosInstance,
  baseUri: '/printers/',
  models: {
    entity: printerShape,
  },
})
export const printerCollection = createCollectionManager({
  fetchList: printerApi.list,
})
