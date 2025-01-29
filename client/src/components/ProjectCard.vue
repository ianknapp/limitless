<template>
  <div class="bg-zinc-900/30 rounded-lg overflow-hidden hover:bg-zinc-800/30 transition-all">
    <!-- Project Image -->
    <router-link :to="{ name: 'Project', params: { id: project.id }}">
      <div class="relative aspect-video">
        <img 
          :src="project.image" 
          :alt="project.title"
          class="w-full h-full object-cover"
        />
        <!-- Hover overlay -->
        <div class="absolute inset-0 bg-black/40 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
          <span class="text-white font-medium">View Project</span>
        </div>
      </div>
    </router-link>

    <!-- Project Info -->
    <div class="p-4">
      <h3 class="font-semibold text-lg mb-2">{{ project.title }}</h3>
      
      <!-- Creator Info -->
      <div class="flex items-center space-x-2 mb-3">
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
            <i class="icon-download" />
            {{ formatNumber(project.downloads) }}
          </span>
          <span class="flex items-center space-x-1">
            <i class="icon-eye" />
            {{ formatNumber(project.views) }}
          </span>
        </div>
        
        <button 
          @click="toggleSave"
          class="flex items-center space-x-1"
          :class="{ 'text-primary': isSaved }"
        >
          <i :class="isSaved ? 'icon-bookmark-filled' : 'icon-bookmark'" />
          {{ formatNumber(project.saves) }}
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
      required: true
    }
  },
  setup(props) {
    const store = useStore()
    const isSaved = ref(props.project.is_saved || false)

    const formatNumber = (num) => {
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
