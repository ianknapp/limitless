import {
  createApi,
  createCollectionManager,
  createCustomServiceCall,
  Pagination,
} from '@thinknimble/tn-models'
import axiosInstance from '../AxiosClient'
import { projectFiltersShape, projectShape, printShape } from './models'

const print = createCustomServiceCall({
  inputShape: printShape,
  cb: async ({ client, input, utils }) => {
    const res = await client.post('/projects/print/', utils.toApi(input))
    return res.data
  },
})

export const ProjectApi = createApi({
  client: axiosInstance,
  baseUri: '/projects/',
  models: {
    entity: projectShape,
    extraFilters: projectFiltersShape,
  },
  customCalls: { print },
})

export const projectFunctions = () => {
  const projectFilters = {
    ordering: '-title',
    search: '',
    recentlyViewed: '',
  }

  const projectCollection = createCollectionManager({
    fetchList: ProjectApi.list,
    filters: projectFilters,
    pagination: new Pagination({ size: 24 }),
  })
  return {
    projectCollection,
    projectFilters,
  }
}
