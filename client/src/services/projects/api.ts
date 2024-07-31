import { createApi, createCollectionManager, Pagination } from '@thinknimble/tn-models'
import axiosInstance from '../AxiosClient'
import { projectShape } from './models'

export const projectApi = createApi({
  client: axiosInstance,
  baseUri: '/projects/',
  models: {
    entity: projectShape,
  },
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
