<template>
  <div class="p-6">
    <MarketplaceHeader
      @search="attemptSearch"
      @filter-change="handleFilterChange"
    />

    <LoadingSpinner v-if="loading" />
    
    <!-- Debug info -->
    <div v-if="!loading && (!projects?.list || projects.list.length === 0)" class="text-white">
      No projects found
    </div>

    <!-- Project Grid -->
    <div v-if="!loading && projects?.list && projects.list.length > 0">
      <div
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <ProjectCard 
          v-for="project in projects.list" 
          :project="project" 
          :key="project.id" 
          class="w-full"
        />
      </div>
      
      <button
        v-if="projects.pagination?.next"
        @click="addNextPage"
        class="mx-auto block btn--primary mt-12 w-40 text-center"
      >
        See More
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, triggerRef } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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
    const loading = ref(true)

    const getProjects = async () => {
      loading.value = true
      try {
        console.log('Fetching projects...')
        await projects.value.refresh()
        triggerRef(projects)
        store.dispatch('setProjects', projects.value.list)
        console.log('Projects loaded:', projects.value.list)
      } catch (error) {
        console.error('Error loading projects:', error)
        if (error.response?.status === 401) {
          store.dispatch('logoutUser')
          router.push({ name: 'Login' })
        }
      } finally {
        loading.value = false
      }
    }

    const addNextPage = async () => {
      if (loading.value) return
      loading.value = true
      try {
        await projects.value.addNextPage()
        triggerRef(projects)
      } catch (error) {
        console.error('Error loading more projects:', error)
      } finally {
        loading.value = false
      }
    }

    function attemptSearch(query) {
      projectFilters.search = query
      router.push({ query: { search: query } })
      getProjects()
    }

    function handleFilterChange({ filter, time }) {
      projectFilters.filter = filter
      projectFilters.timeRange = time
      router.push({ query: { ...route.query, filter, time } })
      getProjects()
    }

    // Initialize projects on component mount
    onMounted(async () => {
      if (route.query.search) {
        projectFilters.search = route.query.search
      }
      await getProjects()
    })

    return {
      projects,
      loading,
      attemptSearch,
      handleFilterChange,
      addNextPage,
      form,
    }
  },
}
</script>
