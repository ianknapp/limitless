<template>
  <div class="fixed top-0 left-0 right-0 h-16 bg-zinc-900 shadow z-50">
    <div class="h-full px-4 flex items-center justify-between">
      <!-- Left section with logo and main nav -->
      <div class="flex items-center space-x-8">
        <router-link to="/" class="flex items-center space-x-3" >
          <img class="h-8" src="@/assets/icons/glyph.png" alt="Limitless" />
          <span class="text-xl font-bold text-primary">Limitless</span>
        </router-link>
        
        <div class="flex space-x-4">
          <router-link 
            to="/" 
            class="text-primary hover:text-primary/80 font-medium"
          >
            3D Models
          </router-link>
        </div>
      </div>

      <!-- Right section with auth -->
      <div class="flex items-center space-x-4" >
        <template v-if="!isLoggedIn">
          <router-link :to="{ name: 'Login' }" class="btn--primary">Login</router-link>
          <router-link :to="{ name: 'Signup' }" class="btn--secondary">Signup</router-link>
        </template>
        
        <div v-else class="relative">
          <button 
            @click="profileMenuOpen = !profileMenuOpen"
            class="p-2 rounded-full bg-neutral-700 hover:bg-neutral-600"
          >
            <img class="h-5 w-5" src="@/assets/icons/gear.svg" alt="Settings" />
          </button>
          
          <!-- Profile dropdown menu -->
          <div v-if="profileMenuOpen" class="absolute right-0 mt-2 w-48 bg-zinc-900 rounded-md shadow-lg">
            <router-link :to="{ name: 'Settings' }">
              <div class="py-2 hover:bg-zinc-600/30">My Profile</div>
            </router-link>
            <hr class="w-1/2 bg-purple dark:bg-purple my-2 h-1 mt-1 rounded border-0 mx-auto" />
            <div
              class="block cursor-pointer px-4 py-2 text-sm textprimary hover:bg-zinc-600/30"
              @click="logout()"
            >
              Log Out
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { userApi } from '@/services/users'

export default {
  name: 'NavBar',
  setup() {
    const store = useStore()
    const router = useRouter()
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
        store.dispatch('logoutUser')
        router.push({ name: 'Login' })
      }
    }

    return {
      logout,
      isLoggedIn: computed(() => store.getters.isLoggedIn),
      profileMenuOpen,
    }
  },
}
</script>
