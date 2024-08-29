<template>
  <div v-if="expandLeftNav" id="leftNav" class="flex-initial shadow">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col h-16 justify-between">
        <div class="flex flex-row gap-4 w-fit mr-12 py-4 px-4">
          <img class="mx-auto h-16 w-auto" src="@/assets/icons/glyph.png" alt="Limitless" />
          <div
            class="mt-4 text-center text-4xl w-fit font-bold leading-9 tracking-tight text-primary"
          >
            Limitless
          </div>
        </div>
        <router-link :to="{ name: 'Home' }" class="router" active-class="active">
          Home
        </router-link>
        <router-link
          active-class="active"
          v-if="isLoggedIn"
          :to="{ name: 'Projects' }"
          class="router"
          >Projects</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import { userApi } from '@/services/users'
import { computed, ref } from 'vue'

import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  props: {
    expandLeftNav: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    let mobileMenuOpen = ref(false)
    let profileMenuOpen = ref(false)

    async function logout() {
      try {
        await userApi.csc.logout()
      } catch (error) {
        if (error.response && error.response.status === 401) {
          console.error('User is not logged in')
        }
        console.log(error)
      } finally {
        profileMenuOpen.value = false
        mobileMenuOpen.value = false
        store.dispatch('setUser', null)
        router.push({ name: 'Home' })
      }
    }

    return {
      logout,
      isLoggedIn: computed(() => store.getters.isLoggedIn),
      user: computed(() => store.getters.user),
      mobileMenuOpen,
      profileMenuOpen,
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
