<template>
  <header class="relative w-full px-6 flex h-32 justify-between sm:h-48"></header>
  <LoadingSpinner v-if="loading" />
  <div v-if="!loading" class="flex">
    <div class="mb-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 content-start px-6">
      <ProjectCard v-for="project in projects.list" :project="project" :key="project.id" />
      <button
        class="col-start-1 col-span-2 md:col-span-4 justify-self-center btn--primary mt-12 w-40 text-center"
        v-if="projects.pagination.next"
        @click="addNextPage()"
      >
        See More
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onBeforeMount, triggerRef } from 'vue'
import { useStore } from 'vuex'
import ProjectCard from '@/components/ProjectCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { projectFunctions } from '@/services/projects'

export default {
  name: 'Projects',
  components: {
    ProjectCard,
    LoadingSpinner,
  },
  setup() {
    const store = useStore()
    const { projectCollection, projectFilters } = projectFunctions()
    const projects = ref(projectCollection)
    const loading = computed(() => {
      return projects.value?.refreshing
    })
    const addNextPage = async () => {
      await projects.value.addNextPage()
      triggerRef(projects)
    }
    onBeforeMount(async () => {
      await getProjects()
    })

    const getProjects = async () => {
      await projects.value.refresh().catch((error) => {
        alert(error)
      })
      triggerRef(projects)
      store.dispatch('setProjects', projects.value.list)
    }
    return {
      addNextPage,
      loading,
      projects,
      projectFilters,
    }
  },
}
</script>
