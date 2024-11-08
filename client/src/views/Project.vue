<template>
  <div class="flex flex-row justify-center flex-wrap-reverse lg:flex-nowrap font-sans flex-grow">
    <div class="w-full flex flex-col items-center justify-center flex-grow">
      <div class="px-6 flex items-center justify-center flex-grow">
        <img
          v-if="currentImageSrc !== project.model"
          class="rounded-lg pointer-events-none object-contain sm:h-[300px] sm:w-[300px] md:h-[400px] md:w-[400px] lg:h-[500px] lg:w-[500px] xl:h-[600px] xl:w-[600px] 3xl:h-[1000px] 3xl:w-[1000px]"
          :src="currentImageSrc"
        />
        <vue3dLoader
          v-if="currentImageSrc === project.model"
          :enableAxesHelper="true"
          :enableGridHelper="true"
          backgroundColor="#042642"
          :filePath="currentImageSrc"
          fileType="stl"
          :rotation="rotation"
          :cameraPosition="cameraPosition"
          :scale="scale"
          class="sm:h-[300px] sm:w-[300px] md:h-[400px] md:w-[400px] lg:h-[450px] lg:w-[450px] 3xl:h-[1000px] 3xl:w-[1000px]"
        ></vue3dLoader>
      </div>
      <div class="px-6 pt-4 grid grid-cols-2 xl:grid-cols-4 gap-4 pb-4 content-start">
        <div class="flex flex-shrink-0 items-center">
          <button
            type="button"
            @click="currentImageSrc = project.primaryImage"
            :class="`rounded-lg flex bg-zinc-900 p-2 justify-self-center ${
              currentImageSrc === project.primaryImage ? 'border-2 border-accent-amber-600' : ''
            }`"
          >
            <img class="rounded-lg flex-shrink pointer-events-none" :src="project.primaryImage" />
          </button>
        </div>
        <div class="flex flex-shrink-0 items-center">
          <button
            type="button"
            @click="currentImageSrc = project.secondaryImage"
            :class="`rounded-lg flex bg-zinc-900 p-2 justify-self-center ${
              currentImageSrc === project.secondaryImage ? 'border-2 border-accent-amber-600' : ''
            }`"
          >
            <img class="rounded-lg flex-shrink pointer-events-none" :src="project.secondaryImage" />
          </button>
        </div>
        <div class="flex flex-shrink-0 items-center">
          <button
            type="button"
            @click="currentImageSrc = project.model"
            :class="`rounded-lg bg-zinc-900 p-2 flex flex-col items-center justify-center justify-self-center w-full h-full ${
              currentImageSrc === project.model ? 'border-2 border-accent-amber-600' : ''
            }`"
          >
            <p className="text-xl">Model</p>
            <Square3Stack3DIcon class="h-6 w-6 text-white" />
          </button>
        </div>
      </div>
    </div>
    <div class="pt-2 text-left xl:max-w-2xl min-w-[300px]">
      <h1 class="pt-2 text-3xl font-bold">
        {{ project.title }}
      </h1>
      <div v-if="project.description" class="font-sans pt-4 opacity-50">
        <div>
          {{ project.description }}
        </div>
      </div>
      <div class="flex flex-col gap-2 content-end pt-3">
        <h2 class="text-base font-semibold">Suggested Model Settings</h2>
        <div class="">
          <span>
            <input
              class="rounded-full checked:accent-amber-600"
              :id="minimizeSupports"
              type="checkbox"
              v-model="minimizeSupports"
            />
            <label class="px-2 font-sans capitalize">Minimize Supports</label>
          </span>
        </div>
        <section class="flex flex-col gap-1">
          <label class="px-2 font-sans capitalize">Adhesion</label>
          <v-select
            :options="adhesionChoices"
            v-model="adhesion"
            label="label"
            :searchable="false"
          ></v-select>
        </section>
        <section class="flex flex-col gap-1">
          <label class="px-2 font-sans capitalize">Support Structure</label>
          <v-select
            :options="supportStructureChoices"
            v-model="supportStructure"
            label="label"
            :searchable="false"
          ></v-select>
        </section>
        <section class="flex flex-col gap-1">
          <label class="px-2 font-sans capitalize">Support Type</label>
          <v-select
            :options="supportTypeChoices"
            v-model="supportType"
            label="label"
            :searchable="false"
          ></v-select>
        </section>
        <section class="flex flex-col gap-1">
          <label class="px-2 font-sans capitalize">Filament</label>
          <v-select :options="filamentChoices" v-model="filament" label="label"></v-select>
        </section>
        <section class="flex flex-col gap-1">
          <label class="px-2 font-sans capitalize">Printer</label>
          <v-select :options="printerChoices" v-model="printer" label="label"></v-select>
        </section>
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
import { PrintForm, ProjectApi } from '@/services/projects'
import Advertisement from '@/components/Advertisement.vue'
import { Square3Stack3DIcon } from '@heroicons/vue/24/solid'

export default {
  name: 'Project',
  components: {
    Advertisement,
    vSelect,
    vue3dLoader,
    Square3Stack3DIcon,
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
    const filamentChoices = ref([])
    const filament = ref()
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
      const projectServer = await ProjectApi.retrieve(route.params.id)
      project.value = projectServer
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
      ProjectApi.csc
        .print({
          pk: route.params.id,
          filament: filament.value.value,
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
      currentImageSrc.value = project.value.primaryImage
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
      filamentChoices.value = store.getters.filaments
      filament.value = filamentChoices.value.find((el) => el.value === user.value.profile.filament)
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

    const currentImageSrc = ref('')

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
      filament,
      filamentChoices,
      printer,
      printerChoices,
      rotation,
      cameraPosition,
      scale,
      minimizeSupports,
      showAd,
      currentImageSrc,
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
