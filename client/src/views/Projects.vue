<template>
  <form class="pl-12 lg:-mt-14 grid font-sans cursor-pointer" @submit.prevent="attemptSearch()">
    <InputField
      class="col-start-1 row-start-1 z-20"
      inputClass="pl-6 h-12 w-72 bg-zinc-900/50 rounded-full cursor-pointer"
      v-model:value="form.query.value"
      :errors="form.query.errors"
      @blur="form.query.validate()"
      placeholder="Search Models"
    />
  </form>
  <header class="relative w-full px-6 flex h-32 justify-between sm:h-48"></header>
  <LoadingSpinner v-if="loading" />
  <div v-if="!loading" class="flex">
    <div
      class="mb-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 content-start px-6"
    >
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
import InputField from '@/components/inputs/InputField.vue'
import ProjectCard from '@/components/ProjectCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { projectFunctions, SearchForm } from '@/services/projects'

export default {
  name: 'Projects',
  components: {
    InputField,
    ProjectCard,
    LoadingSpinner,
  },
  setup() {
    const store = useStore()
    const { projectCollection, projectFilters } = projectFunctions()
    const projects = ref(projectCollection)
    const form = ref(new SearchForm())
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
    function attemptSearch() {
      const unwrappedForm = form.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return
      projectFilters.search = unwrappedForm.query.value
      getProjects()
    }
    return {
      attemptSearch,
      addNextPage,
      form,
      loading,
      projects,
      projectFilters,
    }
  },
}
</script>
