<template>
  <div class="min-h-screen bg-black bg-[url('@/assets/icons/hex.png')] w-full flex flex-col">
    <!-- Fixed top navbar -->
    <NavBar v-if="!skipNav" />
    
    <div class="flex flex-grow">
      <!-- Right side categories panel -->
      <LeftNav v-if="!skipNav" />
      
      <!-- Main content area -->
      <div class="flex-grow">
        <div v-if="skipNav">
          <router-view />
        </div>
        <div v-else class="px-6 overflow-auto">
          <router-view />
        </div>
      </div>
    </div>
    
    <AlertAlert />
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
