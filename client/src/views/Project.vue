<template>
  <div class="flex flex-row justify-center flex-wrap-reverse lg:flex-nowrap font-sans pt-12">
    <div class="w-full">
      <div class="mb-auto px-6 pt-4 flex justify-center">
        <img class="rounded-lg w-full pointer-events-none" :src="project.primaryImage" />
      </div>
      <div class="mb-auto px-6 pt-4 grid grid-cols-2 xl:grid-cols-4 gap-4 pb-4 content-start">
        <div class="flex flex-shrink-0 items-center">
          <div class="rounded-lg flex bg-zinc-900 p-2 h-full w-full justify-self-center">
            <img class="rounded-lg flex-shrink pointer-events-none" :src="project.primaryImage" />
          </div>
        </div>
        <div class="flex flex-shrink-0 items-center">
          <div class="rounded-lg flex bg-zinc-900 p-2 justify-self-center">
            <img class="rounded-lg flex-shrink pointer-events-none" :src="project.secondaryImage" />
          </div>
        </div>
        <div class="flex flex-shrink-0 items-center">
          <div class="rounded-lg bg-zinc-900 p-2 justify-self-center">
            <vue3dLoader
              :enableAxesHelper="true"
              :enableGridHelper="true"
              :height="115"
              :width="115"
              backgroundColor="#042642"
              :filePath="project.model"
              fileType="stl"
              :rotation="rotation"
              :cameraPosition="cameraPosition"
              :scale="scale"
            ></vue3dLoader>
          </div>
        </div>
      </div>
    </div>
    <div class="pt-2 text-left xl:max-w-2xl h-full w-96">
      <h1 class="pt-2 text-3xl font-bold">
        {{ project.title }}
      </h1>
      <div v-if="project.description" class="font-sans pt-4 opacity-50">
        <div>
          {{ project.description }}
        </div>
      </div>
      <div class="mb-2 grid grid-cols-1 gap-4 mt-24 content-end h-96">
        <h2 class="text-base font-semibold">Suggested Model Settings</h2>
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
          :options="adhesionChoices"
          v-model="adhesion"
          label="label"
          :searchable="false"
        ></v-select>
        <v-select
          :options="supportStructureChoices"
          v-model="supportStructure"
          label="label"
          :searchable="false"
        ></v-select>
        <v-select
          :options="supportTypeChoices"
          v-model="supportType"
          label="label"
          :searchable="false"
        ></v-select>
        <v-select :options="printerChoices" v-model="printer" label="label"></v-select>
        <div class="w-full">
          <button class="btn--primary bg-zinc-900" @click.prevent="print()">Download Files</button>
        </div>
      </div>
      <Advertisement v-if="showAd" @close-modal="closeModal" />
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount, h } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import vSelect from 'vue-select'
import { vue3dLoader } from 'vue-3d-loader'
import { PrintForm, projectApi } from '@/services/projects'
import Advertisement from '@/components/Advertisement.vue'

export default {
  name: 'Project',
  components: {
    Advertisement,
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
    let showAd = ref(false)
    const link = ref()
    const user = computed(() => {
      return store.getters.user
    })

    const getProjectData = async () => {
      project.value = await projectApi.retrieve(route.params.id)
    }
    const snakeCase = (value) => {
      return value
        .split(' ')
        .map((word) => word.toLowerCase())
        .join('_')
    }

    function closeModal() {
      showAd.value = false
      link.value.click()
    }

    function print() {
      showAd.value = true
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
      link.value = document.createElement('a')
      link.value.href = URL.createObjectURL(new Blob([response], { type: 'application/gcode' }))
      let d = new Date()
      const fileElements = [snakeCase(title), d.getMonth() + 1, d.getDate(), d.getFullYear()]
      link.value.download = fileElements.join('_') + '.gcode'
    }
    function handleFailure(error) {
      console.log(error)
    }

    vSelect.props.components.default = () => ({
      Deselect: {
        render: () => h('span', ''),
      },
    })

    onBeforeMount(async () => {
      await getProjectData()
      adhesionChoices.value = store.getters.adhesionTypes
      adhesion.value = adhesionChoices.value.find(
        (el) => el.value === project.value.settings?.adhesionType,
      )
      supportStructureChoices.value = store.getters.supportStructures
      supportStructure.value = supportStructureChoices.value.find(
        (el) => el.value === project.value.settings?.supportStructure,
      )
      supportTypeChoices.value = store.getters.supportTypes
      supportType.value = supportTypeChoices.value.find(
        (el) => el.value === project.value.settings?.supportType,
      )
      printerChoices.value = store.getters.printers
      printer.value = printerChoices.value.find((el) => el.value === user.value.profile.printer)
      minimizeSupports.value = user.value.profile.minimize_supports
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

    return {
      adhesion,
      adhesionChoices,
      closeModal,
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
      showAd,
    }
  },
}
</script>

<style>
@import 'vue-select/dist/vue-select.css';

.vs__selected {
  color: #ffffff;
  opacity: 0.5;
}

.vs__dropdown-toggle {
  height: 3.25rem;
  font-weight: 600;
  padding-left: 1rem;
  border-width: 0.12rem;
  border-radius: 0.5rem;
  background-color: #18181b;
}
.vs__dropdown-menu {
  max-height: 12rem;
  font-weight: 600;
  background-color: #18181b;
}
</style>
