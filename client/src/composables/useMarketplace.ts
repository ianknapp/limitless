import { ref, computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { projectApi } from '@/services/projects'

export function useMarketplace() {
  const filters = ref({
    search: '',
    sort: 'newest',
    category: ''
  })

  const currentPage = ref(1)
  const itemsPerPage = ref(20)

  const { 
    data: projects,
    isLoading,
    refetch 
  } = useQuery({
    queryKey: ['projects', filters, currentPage],
    queryFn: () => projectApi.getProjects({ 
      page: currentPage.value,
      limit: itemsPerPage.value,
      ...filters.value 
    })
  })

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    currentPage.value = 1
    refetch()
  }

  const loadMore = () => {
    currentPage.value++
    refetch()
  }

  return {
    projects,
    filters,
    isLoading,
    updateFilters,
    loadMore
  }
} 