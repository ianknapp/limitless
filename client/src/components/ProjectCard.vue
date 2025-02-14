<template>
  <div class="border border-gray-700 rounded-lg overflow-hidden bg-zinc-900/30">
    <router-link
      :to="{ name: 'Project', params: { id: project.id } }"
      class="block"
    >
      <div class="flex justify-center items-center h-48 bg-black">
        <img 
          v-if="project.image"
          class="max-h-full max-w-full object-contain" 
          :src="project.image" 
          :alt="project.title"
        />
      </div>
    </router-link>

    <!-- Project Info -->
    <div class="p-4">
      <h3 class="font-semibold text-lg mb-2 text-white">{{ project.title }}</h3>
      
      <!-- Creator Info -->
      <div v-if="project.creator" class="flex items-center space-x-2 mb-3">
        <img 
          :src="project.creator.avatar" 
          :alt="project.creator.username"
          class="w-6 h-6 rounded-full"
        />
        <span class="text-sm text-gray-300">{{ project.creator.username }}</span>
      </div>

      <!-- Stats -->
      <div class="flex items-center justify-between text-sm text-gray-400">
        <div class="flex items-center space-x-4">
          <span class="flex items-center space-x-1">
            <img src="@/assets/icons/download-svgrepo-com.svg" class="w-4 h-4 filter-white mr-1" />
            {{ formatNumber(project.downloads || 0) }}
          </span>
          <span class="flex items-center space-x-1">
            <img src="@/assets/icons/eye-svgrepo-com.svg" class="w-4 h-4 filter-white mr-1" />
            {{ formatNumber(project.views || 0) }}
          </span>
        </div>
        
        <button 
          @click="toggleSave"
          class="flex items-center space-x-1"
          :class="{ 'text-primary': isSaved }"
        >
          <img v-if="isSaved" src="@/assets/icons/bookmark-fill-svgrepo-com.svg" class="w-4 h-4 filter-white " />
          <img v-else src="@/assets/icons/bookmark-svgrepo-com.svg" class="w-4 h-4 filter-white" />
          {{ formatNumber(project.saves || 0) }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'ProjectCard',
  props: {
    project: {
      type: Object,
      required: true,
      validator: (prop) => {
        return prop && prop.id && prop.title // Add basic validation
      }
    }
  },
  setup(props) {
    const store = useStore()
    const isSaved = ref(props.project.is_saved || false)

    const formatNumber = (num) => {
      if (!num) return '0'
      if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
      if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
      return num.toString()
    }

    const toggleSave = async () => {
      if (!store.getters.isLoggedIn) {
        store.dispatch('showLoginPrompt')
        return
      }

      try {
        const response = await store.dispatch('toggleProjectSave', props.project.id)
        isSaved.value = response.is_saved
      } catch (error) {
        console.error('Error toggling save:', error)
      }
    }

    return {
      isSaved,
      formatNumber,
      toggleSave
    }
  }
}
</script>

<style scoped>
.filter-white {
  filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%);
}
</style>


