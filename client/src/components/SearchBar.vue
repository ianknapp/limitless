<template>
  <form class="pl-12 grid font-sans cursor-pointer" @submit.prevent="handleSearch">
    <InputField
      class="col-start-1 row-start-1 z-20"
      inputClass="pl-6 h-12 w-72 bg-zinc-900/50 rounded-full cursor-pointer"
      v-model:value="searchQuery"
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
        query: { search: searchQuery.value }
      })
    }

    return {
      searchQuery,
      handleSearch
    }
  }
}
</script>
