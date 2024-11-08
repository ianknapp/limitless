import { queryOptions } from '@tanstack/vue-query'
import { ProjectApi } from './api'

export const projectQueries = {
  all: () => ['projects'],
  myProjects: () =>
    queryOptions({
      queryKey: [...projectQueries.all(), 'my-projects'],
      queryFn: ProjectApi.csc.myProjects,
      select: (data) => {
        const devServer = import.meta.env.VITE_DEV_BACKEND_URL
        return data.map((projectServer) => {
          return devServer
            ? {
                ...projectServer,
                image: `${devServer}${projectServer.image}`,
              }
            : projectServer
        })
      },
    }),
}
