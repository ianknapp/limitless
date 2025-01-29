<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Search and Filters -->
    <div class="mb-8 flex flex-col md:flex-row gap-4">
      <input
        v-model="filters.search"
        type="text"
        placeholder="Search projects..."
        class="flex-1 px-4 py-2 bg-zinc-800 rounded-lg"
        @input="handleSearch"
      />
      
      <select
        v-model="filters.sort"
        class="px-4 py-2 bg-zinc-800 rounded-lg"
        @change="handleFiltersChange"
      >
        <option value="newest">Newest</option>
        <option value="downloads">Most Downloaded</option>
        <option value="saves">Most Saved</option>
      </select>

      <select
        v-model="filters.category"
        class="px-4 py-2 bg-zinc-800 rounded-lg"
        @change="handleFiltersChange"
      >
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
    </div>

    <!-- Projects Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
      />
    </div>

    <!-- Load More -->
    <div v-if="hasMore" class="text-center mt-8">
      <button
        @click="loadMore"
        class="px-6 py-2 bg-primary rounded-lg hover:bg-primary/80"
        :disabled="isLoading"
      >
        {{ isLoading ? 'Loading...' : 'Load More' }}
      </button>
    </div>
  </div>
</template>

<script>
import { useMarketplace } from '@/composables/useMarketplace'
import ProjectCard from '@/components/ProjectCard.vue'
import { debounce } from '@/utils/helpers'

export default {
  name: 'Marketplace',
  components: {
    ProjectCard
  },
  setup() {
    const {
      projects,
      filters,
      isLoading,
      updateFilters,
      loadMore
    } = useMarketplace()

    const handleSearch = debounce(() => {
      updateFilters(filters.value)
    }, 300)

    const handleFiltersChange = () => {
      updateFilters(filters.value)
    }

    return {
      projects,
      filters,
      isLoading,
      loadMore,
      handleSearch,
      handleFiltersChange
    }
  }
}
</script> 