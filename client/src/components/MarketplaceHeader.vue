<template>
  <div class="flex justify-between items-center mb-6 px-4">
    <!-- Search Section -->
    <div class="w-1/3">
      <div class="relative">
        <input
          type="text"
          placeholder="Search models..."
          class="w-full px-4 py-2 bg-zinc-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-white"
          v-model="searchQuery"
          @input="handleSearch"
        />
        <img
          src="@/assets/icons/search.svg"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4"
        />
      </div>
    </div>

    <!-- Filter Options -->
    <div class="flex items-center space-x-4">
      <!-- Sort By Label -->
      <span class="text-white font-medium">Sort By:</span>

      <!-- Filter Buttons -->
      <button
        v-for="filter in filters"
        :key="filter.id"
        @click="selectFilter(filter.id)"
        class="px-4 py-2 rounded-lg transition-colors"
        :class="[
          activeFilter === filter.id
            ? 'bg-primary text-black font-medium'
            : 'bg-zinc-800/30 hover:bg-zinc-700/30 text-gray-300 hover:text-white'
        ]"
      >
        {{ filter.name }}
      </button>

      <!-- Time Period Button -->
      <div class="relative" ref="dropdownRef">
        <button
          @click="toggleTimeDropdown"
          class="px-4 py-2 rounded-lg bg-zinc-700/50 text-white font-medium flex items-center space-x-2"
        >
          <span>{{ selectedTimePeriod.label }}</span>
          <img
            src="@/assets/icons/chevron_down.svg"
            class="w-4 h-4"
            :class="{ 'transform rotate-180': isTimeDropdownOpen }"
          />
        </button>

        <!-- Dropdown Menu -->
        <div
          v-if="isTimeDropdownOpen"
          class="absolute right-0 top-full mt-2 w-48 bg-zinc-800 rounded-lg shadow-lg py-2 z-10"
        >
          <button
            v-for="period in timePeriods"
            :key="period.value"
            @click="selectTimePeriod(period)"
            class="w-full px-4 py-2 text-left hover:bg-zinc-700/50 text-gray-300 hover:text-white"
            :class="{ 'text-primary': selectedTimePeriod.value === period.value }"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, defineEmits, onMounted, onUnmounted } from 'vue'

export default {
  name: 'MarketplaceHeader',
  setup() {
    const emit = defineEmits(['search', 'filter-change'])
    
    const searchQuery = ref('')
    const activeFilter = ref('trending')
    const isTimeDropdownOpen = ref(false)
    const dropdownRef = ref(null)

    const filters = [
      { id: 'trending', name: 'Trending' },
      { id: 'downloads', name: 'Downloads' },
      { id: 'saves', name: 'Saves' },
      { id: 'recent', name: 'Recent' },
    ]

    const timePeriods = [
      { value: '7d', label: '7 Days' },
      { value: '30d', label: '30 Days' },
      { value: '180d', label: '180 Days' },
      { value: '1y', label: '1 Year' },
      { value: 'all', label: 'All Time' },
    ]

    const selectedTimePeriod = ref(timePeriods[0])

    function handleClickOutside(event) {
      if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        isTimeDropdownOpen.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    function handleSearch() {
      // Emit search event to parent
      emit('search', searchQuery.value)
    }

    function selectFilter(filterId) {
      activeFilter.value = filterId
      // Emit filter change event to parent
      emit('filter-change', { filter: filterId, time: selectedTimePeriod.value.value })
    }

    function toggleTimeDropdown() {
      isTimeDropdownOpen.value = !isTimeDropdownOpen.value
    }

    function selectTimePeriod(period) {
      selectedTimePeriod.value = period
      isTimeDropdownOpen.value = false
      // Emit time period change event to parent
      emit('filter-change', { filter: activeFilter.value, time: period.value })
    }

    return {
      searchQuery,
      activeFilter,
      isTimeDropdownOpen,
      dropdownRef,
      filters,
      timePeriods,
      selectedTimePeriod,
      handleSearch,
      selectFilter,
      toggleTimeDropdown,
      selectTimePeriod,
    }
  },
}
</script> 