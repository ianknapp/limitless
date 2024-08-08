import axiosInstance from '../AxiosClient'
import { createApi, createCustomServiceCall } from '@thinknimble/tn-models'
import { settingsShape } from './models'

const getSettings = createCustomServiceCall({
  outputShape: settingsShape,
  cb: async ({ client, utils }) => {
    const res = await client.get('/settings/')
    return utils.fromApi(res.data)
  },
})

export const settingsApi = createApi({
  client: axiosInstance,
  baseUri: '/settings/',
  customCalls: {
    getSettings,
  },
})
