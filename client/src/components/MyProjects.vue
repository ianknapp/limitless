<template>
  <div class="pt-8 text-left xl:max-w-2xl h-full">
    <h1 class="pt-2 pl-6 pt-12 text-4xl font-bold">My Projects</h1>
    <div class="flex gap-x-2 justify-between" v-for="project in projects" :key="project.id">
      <div class="my-2 py-2 pl-4 border rounded-lg flex w-full">
        <div class="pr-12 flex flex-row gap-4">
          <div class="pl-2 mt-4 font-normal text-lg font-sans flex flex-wrap justify-left">
            {{ project.title }}
          </div>
          <div class="border my-2 py-2 flex flex-none rounded-lg w-16">
            <button class="self-center pl-6" @click.prevent="deleteProject(project)">
              <img src="@/assets/icons/trash_can.png" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { ProjectApi } from '@/services/projects'

export default {
  name: 'MyProjects',
  components: {},
  setup() {
    const store = useStore()
    const projects = ref()

    onBeforeMount(async () => {
      await getMyProjects()
    })

    const getMyProjects = async () => {
      await ProjectApi.csc.myProjects().then(handleGetProjectsSuccess).catch(handleFailure)
    }
    function handleGetProjectsSuccess(response) {
      projects.value = response
    }

    function deleteProject(project) {
      ProjectApi.csc
        .deleteProject({ pk: project.id })
        .then(handleRemovalSuccess)
        .catch(handleFailure)
    }
    function handleRemovalSuccess() {
      getMyProjects()
    }

    function handleFailure(error) {
      console.log(error)
    }

    return {
      deleteProject,
      projects,
    }
  },
}
</script>

<style></style>
