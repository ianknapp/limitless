<template>
  <div class="flex-1 flex justify-center">
    <v-select
      v-model="selected"
      :options="options"
      :filterable="false"
      :loading="isLoading"
      @search="onSearch"
      placeholder="Search Models"
      class="w-72"
    >
      <template #no-options>
        Type to search projects...
      </template>
      <template #option="{ title, image }">
        <div class="flex items-center">
          <img v-if="image" :src="image" class="h-8 w-8 rounded mr-2" />
          <span>{{ title }}</span>
        </div>
      </template>
    </v-select>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import VSelect from 'vue-select'
import 'vue-select/dist/vue-select.css'

export default {
  name: 'SearchBar',
  components: {
    VSelect,
  },
  setup() {
    const router = useRouter()
    const selected = ref(null)
    const options = ref([])
    const isLoading = ref(false)

    const onSearch = async (search) => {
      if (search.length < 1) return
      
      isLoading.value = true
      try {
        // Use your existing API endpoint
        const response = await fetch(`/api/projects/?search=${search}`)
        const data = await response.json()
        options.value = data
      } catch (error) {
        console.error('Search error:', error)
      } finally {
        isLoading.value = false
      }
    }

    // Watch for changes in selection
    watch(selected, (newValue) => {
      if (newValue) {
        router.push({ name: 'Project', params: { id: newValue.id } })
      }
    })

    return {
      selected,
      options,
      isLoading,
      onSearch,
    }
  }
}
</script>

<style>
/* Custom styles to match your dark theme */
.v-select {
  background-color: rgba(24, 24, 27, 0.5);
  border-radius: 9999px;
  width: 18rem; /* w-72 equivalent */
}

.v-select .vs__dropdown-toggle {
  border: none;
  height: 3rem;
  padding-left: 1.5rem;
  background-color: transparent;
}

.v-select .vs__selected {
  color: white;
}

.v-select .vs__search {
  color: white;
}

.v-select .vs__dropdown-menu {
  background-color: rgb(24, 24, 27);
  color: white;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.v-select .vs__dropdown-option {
  color: white;
  padding: 0.5rem 1rem;
}

.v-select .vs__dropdown-option--highlight {
  background: rgba(139, 92, 246, 0.5);
}

.v-select .vs__search::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.v-select .vs__actions {
  padding-right: 1rem;
}

.v-select .vs__clear {
  fill: white;
}
</style>