<template>
  <div class="pt-8 text-left xl:max-w-2xl h-full">
    <h1 class="pt-2 pl-6 text-4xl font-bold">My Projects</h1>
    <div class="flex gap-x-2 justify-between" v-for="project in myProjects" :key="project.id">
      <div class="my-2 py-2 px-4 border rounded-lg flex w-full">
        <div class="grid grid-cols-5 gap-4 w-full">
          <section class="col-span-1">
            <img :src="project.image" class="h-20 w-20 rounded-lg" />
          </section>
          <div
            class="pl-2 mt-4 col-span-3 font-normal text-lg font-sans flex flex-wrap justify-left"
          >
            {{ project.title }}
          </div>
          <div class="border my-2 py-2 flex flex-none rounded-lg w-16 col-span-1 justify-self-end">
            <button
              class="self-center pl-6"
              @click.prevent="deleteProject({ pk: project.id })"
              :disabled="isDeleting"
            >
              <img src="@/assets/icons/trash_can.png" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ProjectApi, projectQueries } from '@/services/projects'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

export default {
  name: 'MyProjects',
  components: {},
  setup() {
    const { data: myProjects } = useQuery(projectQueries.myProjects())
    const queryClient = useQueryClient()
    const { mutate: deleteProject, isPending: isDeleting } = useMutation({
      mutationFn: ProjectApi.csc.deleteProject,
      onSuccess: () => {
        queryClient.invalidateQueries(projectQueries.all())
      },
    })

    return {
      deleteProject,
      myProjects,
      isDeleting,
    }
  },
}
</script>

<style></style>
