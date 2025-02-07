<template>
  <div class="min-h-screen bg-black bg-[url('@/assets/icons/hex.png')] w-full">
    <!-- Fixed top navbar -->
    <NavBar v-if="!skipNav" />
    
    <!-- Main layout container -->
    <div class="flex min-h-screen">
      <!-- Left side navigation -->
      <LeftNav v-if="!skipNav" />
      
      <!-- Main content area -->
      <div class="flex-1">
        <router-view />
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

    // onBeforeMount(async () => {
    //   settingsApi.csc.getSettings().then(handleSuccess).catch(handleFailure)
    // })
    // function handleSuccess(response) {
    //   store.dispatch('setFilaments', response.filaments)
    //   store.dispatch('setSupportStructures', response.supportStructures)
    //   store.dispatch('setSupportTypes', response.supportTypes)
    //   store.dispatch('setAdhesionTypes', response.adhesionTypes)
    //   store.dispatch('setPrinters', response.printers)
    // }
    // function handleFailure(error) {
    //   if (error.response && error.response.status === 401) {
    //     // User session expired
    //     store.dispatch('logoutUser')
    //     router.push({ name: 'Login' })
    //   }
    //   console.log(error)
    // }

    return {
      skipNav: computed(() =>
        ['Login', 'Signup', 'RequestPasswordReset'].some(
          (item) => item === router.currentRoute.value.name,
        ),
      ),
    }
  },
}
</script>

<style>
.body {
  color: white;
}
</style>


