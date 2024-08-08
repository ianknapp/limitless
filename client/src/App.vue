<template>
  <div
    class="flex min-h-screen flex-col text-center font-serif text-primary antialiased pt-16 bg-slate-200"
  >
    <AlertAlert />
    <NavBar />
    <div class="w-full mx-auto max-w-7xl flex min-h-full flex-2 flex-col bg-white">
      <router-view />
    </div>
  </div>
</template>

<script>
import { ref, onBeforeMount } from 'vue'
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
    const store = useStore()
    const printers = ref([])
    const supportStructures = ref([])
    const supportTypes = ref([])
    const adhesionTypes = ref([])

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
    return {}
  },
}
</script>
