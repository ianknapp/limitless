import {
  createApi,
  createCollectionManager,
  createCustomServiceCall,
  Pagination,
} from '@thinknimble/tn-models'
import axiosInstance from '../AxiosClient'
import { projectFiltersShape, projectShape, printShape } from './models'
import { z } from 'zod'

const print = createCustomServiceCall({
  inputShape: printShape,
  cb: async ({ client, input, utils }) => {
    const res = await client.post('/projects/print/', utils.toApi(input))
    return res.data
  },
})

const myProjects = createCustomServiceCall({
  inputShape: projectShape,
  cb: async ({ client }) => {
    const res = await client.get('/my_projects/')
    return res.data
  },
})

const deleteProject = createCustomServiceCall({
  inputShape: { pk: z.string().uuid() },
  cb: async ({ client, input, utils }) => {
    const res = await client.delete(`/projects/${input.pk}/`)
    return res.data
  },
})

const createProject = createCustomServiceCall({
  inputShape: projectShape,
  outputShape: projectShape,
  cb: async ({ client, input, utils }) => {
    const formData = new FormData()
    formData.append('title', input.title)
    formData.append('description', input.description)
    formData.append('recommendedFilament', input.recommendedFilament)
    formData.append('model', input.model)
    formData.append('primaryImage', input.primaryImage)
    formData.append('secondaryImage', input.secondaryImage)

    const res = await client.post('/projects/create/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return utils.fromApi(res.data)
  },
})

export const ProjectApi = createApi({
  client: axiosInstance,
  baseUri: '/projects/',
  models: {
    entity: projectShape,
    extraFilters: projectFiltersShape,
  },
  customCalls: { print, createProject, myProjects, deleteProject },
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
