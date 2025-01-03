<template>
  <div class="min-h-screen bg-black bg-[url('@/assets/icons/hex.png')] w-full flex">
    <div class="flex justify-center flex-grow">
      <div
        class="w-1/2 h-full opacity-20 bg-violet-900 rounded-full blur-3xl absolute z-0 -top-full mt-40"
      ></div>
      <div v-if="skipNav">
        <router-view />
      </div>
      <div
        v-else
        class="flex flex-row w-full text-center font-serif text-primary antialiased md:max-w-[80%] 3xl:max-w-[70%] flex-grow"
      >
        <AlertAlert />

        <LeftNav :expandLeftNav="leftNav" />
        <div class="flex justify-center flex-grow flex-col w-full">
          <NavBar @toggle-left-nav="toggleLeftNav" />
          <div class="px-6 overflow-auto flex flex-grow">
            <router-view />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { AlertAlert } from '@thinknimble/vue3-alert-alert'
import LeftNav from '@/components/LeftNav.vue'
import NavBar from '@/components/NavBar.vue'
import { settingsApi } from '@/services/settings'

export default {
  name: 'App',
  components: {
    LeftNav,
    NavBar,
    AlertAlert,
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const leftNav = ref(true)

    onBeforeMount(async () => {
      settingsApi.csc.getSettings().then(handleSuccess).catch(handleFailure)
    })
    function handleSuccess(response) {
      store.dispatch('setFilaments', response.filaments)
      store.dispatch('setSupportStructures', response.supportStructures)
      store.dispatch('setSupportTypes', response.supportTypes)
      store.dispatch('setAdhesionTypes', response.adhesionTypes)
      store.dispatch('setPrinters', response.printers)
    }
    function handleFailure(error) {
      if (error.response && error.response.status === 401) {
        // User session expired
        store.dispatch('logoutUser')
        router.push({ name: 'Login' })
      }
      console.log(error)
    }

    function toggleLeftNav() {
      leftNav.value = !leftNav.value
    }

    return {
      leftNav,
      toggleLeftNav,
      skipNav: computed(() =>
        ['Login', 'Signup', 'RequestPasswordReset'].some(
          (item) => item === router.currentRoute.value.name,
        ),
      ),
    }
  },
}
</script>
