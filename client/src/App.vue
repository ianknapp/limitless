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
import { reactive, ref, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { AlertAlert } from '@thinknimble/vue3-alert-alert'
import NavBar from '@/components/NavBar.vue'
import { printerCollection } from '@/services/printers'

export default {
  name: 'App',
  components: {
    NavBar,
    AlertAlert,
  },
  setup() {
    const store = useStore()
    const printers = ref([])

    onBeforeMount(async () => {
      await printerCollection.refresh()
      printers.value = printerCollection.list.map((i) => {
        return { label: i.name, value: i.id }
      })
      await store.dispatch('setPrinters', printers)
    })
    return {}
  },
}
</script>
