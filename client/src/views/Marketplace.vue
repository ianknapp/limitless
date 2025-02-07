<template>
  <div class="p-6"> <!-- Added padding to match content area -->
    <MarketplaceHeader
      @search="attemptSearch"
      @filter-change="handleFilterChange"
    />

    <LoadingSpinner v-if="loading" />
    <div v-if="!loading" class="flex">
      <div
        class="mb-8 grid gap-4 content-start w-full"
        style="grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));"
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
  </div>
</template>

<script>
import { ref, computed, onBeforeMount, triggerRef } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import InputField from '@/components/inputs/InputField.vue'
import ProjectCard from '@/components/ProjectCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import MarketplaceHeader from '@/components/MarketplaceHeader.vue'
import { projectFunctions, SearchForm } from '@/services/projects'

export default {
  name: 'Projects',
  components: {
    InputField,
    ProjectCard,
    LoadingSpinner,
    MarketplaceHeader,
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
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
    // Added this section to handle URL search params
    onBeforeMount(async () => {
      if (route.query.search) {
        form.value.query.value = route.query.search
        projectFilters.search = route.query.search
      }
      await getProjects()
    })

    const getProjects = async () => {
      await projects.value.refresh().catch((error) => {
        console.log('getProjects: ', error)
        if (error.response && error.response.status === 401) {
          // User session expired
          store.dispatch('logoutUser')
          router.push({ name: 'Login' })
        }
      })
      triggerRef(projects)
      store.dispatch('setProjects', projects.value.list)
    }
    // Updated attemptSearch to modify URL
    function attemptSearch() {
      const unwrappedForm = form.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return
      projectFilters.search = unwrappedForm.query.value
      router.push({
        query: { search: unwrappedForm.query.value },
      })
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
