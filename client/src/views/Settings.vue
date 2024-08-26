<template>
  <div class="flex flex-row justify-center flex-wrap-reverse lg:flex-nowrap">
    <div class="pt-2 text-left xl:max-w-2xl h-full">
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

        <div class="">
          <span>
            <input
              class="rounded-full checked:accent-amber-600"
              :id="minimizeSupports"
              type="checkbox"
              v-model="minimizeSupports"
            />
            <label class="mx-2 font-sans capitalize">Minimize Supports</label>
          </span>
        </div>
        <v-select
          class="w-96"
          :options="adhesionChoices"
          v-model="adhesion"
          label="label"
          :searchable="false"
        ></v-select>
        <v-select
          class="w-96"
          :options="supportStructureChoices"
          v-model="supportStructure"
          label="label"
          :searchable="false"
        ></v-select>
        <v-select
          class="w-96"
          :options="supportTypeChoices"
          v-model="supportType"
          label="label"
          :searchable="false"
        ></v-select>
        <v-select class="w-96" :options="printerChoices" v-model="printer" label="label"></v-select>
        <div class="w-24">
          <button class="btn--primary bg-primary" @click.prevent="print()">Print</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onBeforeMount, h } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import vSelect from 'vue-select'
import { vue3dLoader } from 'vue-3d-loader'
import { PrintForm, projectApi } from '@/services/projects'

export default {
  name: 'Settings',
  components: {
    vSelect,
    vue3dLoader,
  },
  setup() {
    const store = useStore()
    const project = ref({})
    const route = useRoute()
    const adhesionChoices = ref([])
    const adhesion = ref()
    const supportStructureChoices = ref([])
    const supportStructure = ref()
    const supportTypeChoices = ref([])
    const supportType = ref()
    const printerChoices = ref([])
    const printer = ref()
    const form = ref(new PrintForm())
    const printSuccess = ref(false)
    const rotation = ref()
    const cameraPosition = ref()
    const scale = ref()
    const minimizeSupports = ref(false)

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
      adhesionChoices.value = store.getters.adhesionTypes
      adhesion.value = adhesionChoices.value[0]
      supportStructureChoices.value = store.getters.supportStructures
      supportStructure.value = supportStructureChoices.value[0]
      supportTypeChoices.value = store.getters.supportTypes
      supportType.value = supportTypeChoices.value[0]
      printerChoices.value = store.getters.printers
      printer.value = printerChoices.value[0]
      rotation.value = {
        x: Math.PI / 2,
        y: Math.PI,
        z: Math.PI - 30,
      }
      cameraPosition.value = {
        x: -Math.PI / 2 + 100,
        y: 250,
        z: -300,
      }
      scale.value = { x: 1.5, y: 1.5, z: 1.5 }
    })

    function print() {
      projectApi.csc
        .print({
          pk: route.params.id,
          printer: printer.value.value,
          supportStructure: supportStructure.value.value,
          supportType: supportType.value.value,
          adhesionType: adhesion.value.value,
          minimizeSupports: minimizeSupports.value,
        })
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
      adhesion,
      adhesionChoices,
      supportStructureChoices,
      supportStructure,
      supportTypeChoices,
      supportType,
      project,
      print,
      printSuccess,
      form,
      printer,
      printerChoices,
      rotation,
      cameraPosition,
      scale,
      minimizeSupports,
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
