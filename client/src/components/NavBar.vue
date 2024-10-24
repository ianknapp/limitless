<template>
  <div class="top-0 z-10 shadow sm:pt-10">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-row justify-end sm:justify-between h-16">
        <div class="content-center hidden sm:inline-block">
          <img
            class="block h-6 w-6 cursor-pointer"
            v-if="leftNavOpen"
            src="@/assets/icons/chevron_left.png"
            alt="Hide Navigation"
            @click="toggleLeftNav"
          />
          <img
            class="block h-6 w-6 cursor-pointer"
            v-if="!leftNavOpen"
            src="@/assets/icons/chevron_right.png"
            alt="Open Navigation"
            @click="toggleLeftNav"
          />
        </div>
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <template v-if="!isLoggedIn">
            <router-link :to="{ name: 'Login' }" class="btn--primary bg-zinc-900" data-cy="login"
              >Login</router-link
            >
            <router-link :to="{ name: 'Signup' }" class="btn--secondary ml-6">Signup</router-link>
          </template>
          <!-- Profile dropdown -->
          <div class="relative ml-3 focus:ring-2" v-if="isLoggedIn">
            <div
              @click="profileMenuOpen = !profileMenuOpen"
              class="cursor-pointer h-13 p-4 bg-neutral-700 rounded-full justify-start items-center gap-2.5 inline-flex"
            >
              <div class="w-5 h-5 relative">
                <img
                  class="h-5 w-4 left-[1.97px] top-[0.87px] absolute"
                  src="@/assets/icons/gear.svg"
                  alt="Profile"
                />
              </div>
            </div>
            <div
              v-if="profileMenuOpen"
              class="absolute font-sans right-0 z-10 mt-2 w-48 rounded-md bg-zinc-900 py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
            >
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
        <div class="flex items-center sm:hidden">
          <!-- Mobile menu button -->
          <div
            class="rounded-md p-2 bg-zinc-700 hover:bg-gray-100 hover:text-gray-500 focus:outline-none"
          >
            <img
              class="block h-6 w-6 cursor-pointer"
              v-if="!mobileMenuOpen"
              src="@/assets/icons/bars.svg"
              alt="Bars"
              @click="mobileMenuOpen = true"
            />
            <img
              v-if="mobileMenuOpen"
              src="@/assets/icons/x-mark.svg"
              alt="Close"
              class="block h-6 w-6 cursor-pointer text-primary"
              @click="mobileMenuOpen = false"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="sm:hidden font-sans bg-gray-500/10" v-if="mobileMenuOpen">
      <div class="space-y-1 pb-3 pt-2">
        <router-link
          :to="{ name: 'Home' }"
          @click="mobileMenuOpen = false"
          active-class="active--mobile"
          class="mobile-link--main"
        >
          Home
        </router-link>
      </div>
      <div class="border-t border-gray-200 pb-3 pt-4">
        <div class="flex justify-center px-4" v-if="isLoggedIn">
          <div class="h-13 p-4 bg-neutral-700 rounded-full gap-2.5 inline-flex">
            <div class="w-5 h-5 relative">
              <img
                class="h-6 w-6 rounded-full"
                src="@/assets/icons/profile-circle.svg"
                alt="Profile"
              />
            </div>
          </div>
          <div class="ml-3">
            <div class="text-base font-medium">{{ user.firstName }} {{ user.lastName }}</div>
            <div class="text-sm font-medium">{{ user.email }}</div>
          </div>
        </div>
        <div class="mt-3 space-y-1" v-if="isLoggedIn">
          <router-link
            :to="{ name: 'Settings' }"
            @click="mobileMenuOpen = false"
            active-class="active--mobile"
            class="mobile-link"
          >
            Settings
          </router-link>
          <template v-if="!isLoggedIn">
            <router-link
              @click="mobileMenuOpen = false"
              :to="{ name: 'Signup' }"
              active-class="active--mobile"
              class="mobile-link"
            >
              Signup
            </router-link>
            <router-link
              @click="mobileMenuOpen = false"
              :to="{ name: 'Login' }"
              data-cy="login"
              active-class="active--mobile"
              class="mobile-link"
            >
              Login
            </router-link>
          </template>
          <div v-if="isLoggedIn" @click="logout()" class="mobile-link">Log Out</div>
        </div>
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
  emits: ['toggleLeftNav'],
  setup(props, context) {
    const store = useStore()
    const router = useRouter()
    let leftNavOpen = ref(true)
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
        store.dispatch('logoutUser')
        router.push({ name: 'Login' })
      }
    }

    function toggleLeftNav() {
      context.emit('toggleLeftNav')
      leftNavOpen.value = !leftNavOpen.value
    }

    return {
      toggleLeftNav,
      leftNavOpen,
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
