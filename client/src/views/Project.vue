<template>
  <div class="pl-8 pb-4 pt-4 text-left">
    <router-link :to="{ name: 'Projects' }">
      <span class="pt-1 font-semibold">&lt; Back</span>
    </router-link>
  </div>
  <div class="flex flex-row justify-center flex-wrap-reverse lg:flex-nowrap">
    <div class="pt-2 text-left w-1/2 h-full">
      <h1 class="pt-2 pl-6 text-6xl font-bold">
        {{ project.title }}
      </h1>
      <div v-if="project.description" class="font-sans pl-8 pt-4">
        <div>
          {{ project.description }}
        </div>
      </div>
      <div class="mt-8 mb-2 grid grid-cols-1 gap-4 pl-6 content-end h-96">
        <hr class="h-0.5 bg-primary mt-2 mb-2" />
        <v-select class="w-96" :options="printerChoices" v-model="printer" label="label"></v-select>
        <div class="w-24">
          <button class="btn--primary bg-primary" @click.prevent="print()">Print</button>
        </div>
      </div>
    </div>
    <div class="lg:max-w-lg xl:max-w-2xl">
      <div class="mb-auto px-6 pt-4">
        <img
          class="rounded-lg pointer-events-none"
          src="https://1.bp.blogspot.com/-dHN4KiD3dsU/XRxU5JRV7DI/AAAAAAAAAz4/u1ynpCMIuKwZMA642dHEoXFVKuHQbJvwgCEwYBhgL/s1600/qr-code.png"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount, h } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import vSelect from 'vue-select'
import { PrintForm, projectApi } from '@/services/projects'

export default {
  name: 'Project',
  components: {
    vSelect,
  },
  setup() {
    const store = useStore()
    const project = ref({})
    const route = useRoute()
    const printerChoices = ref([])
    const printer = ref()
    const form = ref(new PrintForm())
    const printSuccess = ref(false)

    const getProjectData = async () => {
      project.value = await projectApi.retrieve(route.params.id)
    }
    const snakeCase = (value) => {
      return value
        .split(' ')
        .map((word) => word.toLowerCase())
        .join('_')
    }

    vSelect.props.components.default = () => ({
      Deselect: {
        render: () => h('span', ''),
      },
    })

    onBeforeMount(async () => {
      await getProjectData()
      printerChoices.value = store.getters.printers
      printer.value = printerChoices.value[0]
    })

    function print() {
      projectApi.csc
        .print({ pk: route.params.id, printer: printer.value.value })
        .then(handleGcodeSuccess)
        .catch(handleFailure)
    }
    function handleGcodeSuccess(response) {
      const title = project.value.title
      const link = document.createElement('a')
      link.href = URL.createObjectURL(new Blob([response], { type: 'application/gcode' }))
      let d = new Date()
      const fileElements = [snakeCase(title), d.getMonth() + 1, d.getDate(), d.getFullYear()]
      link.download = fileElements.join('_') + '.gcode'
      link.click()
    }
    function handleFailure(error) {
      console.log(error)
    }

    return {
      printers: computed(() => store.getters.printers),
      project,
      print,
      printSuccess,
      form,
      printer,
      printerChoices,
    }
  },
}
</script>

<style>
@import 'vue-select/dist/vue-select.css';

.vs__dropdown-toggle {
  height: 3.25rem;
  font-weight: 600;
  padding-left: 1rem;
  border-width: 0.12rem;
  border-color: #003851;
  border-radius: 0.5rem;
}
.vs__dropdown-menu {
  height: 12rem;
  font-weight: 600;
}
</style>
