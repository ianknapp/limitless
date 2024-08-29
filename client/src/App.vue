<template>
  <div class="min-h-screen bg-black" style="background-image: url('/src/assets/icons/hex.png')">
    <div class="flex justify-center">
      <div v-if="skipNav">
        <router-view />
      </div>
      <div
        v-else
        class="flex max-w-7xl min-h-screen flex-row text-center font-serif text-primary antialiased"
      >
        <AlertAlert />

        <LeftNav :expandLeftNav="leftNav" />
        <div class="w-full mx-auto flex min-h-full flex-2 flex-col">
          <NavBar @toggle-left-nav="toggleLeftNav" />
          <router-view />
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
      store.dispatch('setSupportStructures', response.supportStructures)
      store.dispatch('setSupportTypes', response.supportTypes)
      store.dispatch('setAdhesionTypes', response.adhesionTypes)
      store.dispatch('setPrinters', response.printers)
    }
    function handleFailure(error) {
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
