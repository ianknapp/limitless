import {
  createApi,
  createCollectionManager,
  createCustomServiceCall,
  Pagination,
} from '@thinknimble/tn-models'
import axiosInstance from '../AxiosClient'
import { projectShape, printShape } from './models'

const print = createCustomServiceCall({
  inputShape: printShape,
  cb: async ({ client, input, utils }) => {
    console.log('about to print')
    const res = await client.post('/projects/print/', utils.toApi(input))
    return res.data
  },
})

export const projectApi = createApi({
  client: axiosInstance,
  baseUri: '/projects/',
  models: {
    entity: projectShape,
  },
  customCalls: { print },
})

export const projectFunctions = () => {
  const projectFilters = {
    ordering: '-title',
  }

  const projectCollection = createCollectionManager({
    fetchList: projectApi.list,
    filters: projectFilters,
    pagination: new Pagination({ size: 24 }),
  })
  return {
    projectCollection,
    projectFilters,
  }
}
