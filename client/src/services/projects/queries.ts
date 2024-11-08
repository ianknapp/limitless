import { queryOptions } from '@tanstack/vue-query'
import { ProjectApi } from './api'

export const projectQueries = {
  all: () => ['projects'],
  myProjects: () =>
    queryOptions({
      queryKey: [...projectQueries.all(), 'my-projects'],
      queryFn: ProjectApi.csc.myProjects,
    }),
}
