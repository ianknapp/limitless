<template>
  <div class="min-h-screen bg-black" style="background-image: url('/src/assets/icons/hex.png')">
    <div v-if="skipNav">
      <router-view />
    </div>
    <div
      v-else
      class="flex min-h-screen flex-col text-center font-serif text-primary antialiased pt-16 bg-slate-200"
    >
      <AlertAlert />
      <NavBar />

        <router-view />
      </div>
  </div>
</template>

<script>
import { computed, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { AlertAlert } from '@thinknimble/vue3-alert-alert'
import NavBar from '@/components/NavBar.vue'
import { settingsApi } from '@/services/settings'

export default {
  name: 'App',
  components: {
    NavBar,
    AlertAlert,
  },
  setup() {
    const router = useRouter()
    const store = useStore()

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
