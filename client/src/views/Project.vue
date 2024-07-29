<template>
  <div class="pl-8 pb-4 pt-4 text-left">
    <router-link :to="{ name: 'Projects' }">
      <span class="pt-1 font-semibold">&lt; Back</span>
    </router-link>
  </div>
  <div class="flex flex-row justify-center flex-wrap-reverse lg:flex-nowrap">
    <div class="pt-2 text-left">
      <h1 class="pt-2 pl-6 text-6xl font-bold">
        {{ project.title }}
      </h1>
      <div v-if="project.description" class="font-sans pl-8 pt-4">
        <div>
          {{ project.description }}
        </div>
      </div>
      <div class="mt-8 mb-2 flex flex-wrap justify-left pl-6">
        <hr class="h-0.5 bg-primary mt-8 mb-6" />
        <div class="flex flex-shrink-0 items-center pb-4">
          <v-select
            class="w-1/2"
            :options="printerChoices"
            v-model="printer"
            label="label"
          ></v-select>
          <button
            class="w-1/2 ml-4 btn--primary"
            @click.prevent="print()"
          >
            Print
          </button>
        </div>
      </div>
    </div>
    <div class="lg:max-w-lg xl:max-w-2xl">
      <div class="mb-auto px-6 pt-4">
        <img class="rounded-lg pointer-events-none" :src="project.primaryImage" />
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
    const printer = ref(0)
    const form = ref(new PrintForm())
    const printSuccess = ref(false)

    const getProjectData = async () => {
      project.value = await projectApi.retrieve(route.params.pk)
    }

    vSelect.props.components.default = () => ({
      Deselect: {
        render: () => h('span', ''),
      },
    })

    onBeforeMount(async () => {
      await getProjectData()
      printer.value = { label: project.value.printers + ' printers', value: project.value.printers }
      printerChoices.value = [...Array(project.value.printers + 30).keys()].map((i) => {
        return { label: i + 1 + ' printers', value: i + 1 }
      })
    })

    function print() {
      console.log('printing')
      //projectApi.csc
      //  .print({ pk: route.params.pk, printer: printer.value.value })
      //  .then(handleSuccess)
      //  .catch(handleFailure)
    }
    function handleSuccess() {
      // projectA.csc.foo().then(handleUpdateSuccess).catch(handleFailure)
      console.log('print success')
    }
    function handleUpdateSuccess(response) {
      store.dispatch(
        'setFoo',
        response.map((element) => element.project.id),
      )
    }
    function handleFailure(error) {
      console.log(error)
    }

    return {
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
