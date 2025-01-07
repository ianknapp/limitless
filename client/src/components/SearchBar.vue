<template>
  <form class="flex" @submit.prevent="handleSearch">
    <InputField
      class="pl-6 h-12 w-72 bg-zinc-900/50 rounded-full cursor-pointer"
      v-model="searchQuery"
      placeholder="Search Models"
    />
  </form>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import InputField from '@/components/inputs/InputField.vue'

export default {
  name: 'SearchBar',
  components: {
    InputField,
  },
  setup() {
    const router = useRouter()
    const searchQuery = ref('')

    const handleSearch = () => {
      if (!searchQuery.value) return

      router.push({
        name: 'Home',
        query: { search: searchQuery.value },
      })
    }

    return {
      searchQuery,
      handleSearch,
    }
  },
}
</script>
