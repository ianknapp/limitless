<template>
  <div class="w-64 bg-zinc-900/50 border-r border-zinc-800 flex flex-col">
    <!-- Categories Section -->
    <div class="p-4">
      <div class="flex items-center space-x-2 p-2 hover:bg-zinc-700/50 rounded cursor-pointer">
        <span class="text-primary font-medium">Categories</span>
        <img src="@/assets/icons/chevron_right.png" class="h-4 w-4" />
      </div>
      <!-- Add your category items here -->
    </div>
    <!-- Recently Viewed Section -->
    <div class="p-4 border-t border-zinc-800">
      <h3 class="text-primary font-medium mb-4">Recently Viewed</h3>
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <ProjectMiniCard 
          v-for="project in projects.list" 
          :project="project" 
          :key="project.id" 
        />
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount, triggerRef } from 'vue'
import { useStore } from 'vuex'
import ProjectMiniCard from '@/components/ProjectMiniCard.vue'
import { projectFunctions } from '@/services/projects'

export default {
  name: 'LeftNav',
  components: {
    ProjectMiniCard,
  },
  setup() {
    const store = useStore()
    const { projectCollection, projectFilters } = projectFunctions()
    const projects = ref(projectCollection)

    const getProjects = async () => {
      projectFilters.recentlyViewed = 'true'
      await projects.value.refresh()
      triggerRef(projects)
      store.dispatch('setProjects', projects.value.list)
    }

    onBeforeMount(async () => {
      await getProjects()
    })

    return {
      projects,
    }
  },
}
</script>

<style scoped>
.mobile-link {
  @apply block cursor-pointer border-l-4 px-4 py-2 text-base font-medium hover:bg-gray-100 hover:text-gray-800;
}

.mobile-link--main {
  @apply block border-l-4 py-2 pl-3 pr-4 text-base font-medium hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700;
}
</style>
