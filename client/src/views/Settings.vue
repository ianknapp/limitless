<template>
  <div class="w-fit flex flex-row justify-center flex-wrap-reverse lg:flex-nowrap font-sans">
    <div class="pt-8 text-left xl:max-w-2xl h-full">
      <h1 class="pt-2 pl-6 pt-12 text-4xl font-bold">Print Settings</h1>
      <div class="mt-8 mb-2 pt-4 grid grid-cols-1 gap-6 pl-6 content-end pb-12">
        <span>
          <label class="mx-2 font-sans capitalize">Your Default Printer</label>
          <v-select
            class="w-96"
            :options="printerChoices"
            v-model="printer"
            label="label"
            placeholder="select your default..."
          ></v-select>
        </span>
        <span>
          <label class="mx-2 font-sans capitalize">Your Default Filament</label>
          <v-select
            class="w-96"
            :options="filamentChoices"
            v-model="filament"
            label="label"
            placeholder="select your default..."
          ></v-select>
        </span>
        <span>
          <input
            class="rounded-full checked:accent-amber-600"
            :id="minimizeSupports"
            type="checkbox"
            v-model="minimizeSupports"
          />
          <label class="mx-2 font-sans capitalize">Minimize Supports</label>
        </span>
        <div class="w-24">
          <button class="btn--primary bg-zinc-900" @click.prevent="save()">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount, h } from 'vue'
import { useStore } from 'vuex'
import vSelect from 'vue-select'
import { vue3dLoader } from 'vue-3d-loader'
import { userApi } from '@/services/users'

export default {
  name: 'Settings',
  components: {
    vSelect,
    vue3dLoader,
  },
  setup() {
    const store = useStore()
    const filamentChoices = ref([])
    const filament = ref()
    const printerChoices = ref([])
    const printer = ref()
    const minimizeSupports = ref(false)
    const user = computed(() => {
      return store.getters.user
    })

    vSelect.props.components.default = () => ({
      Deselect: {
        render: () => h('span', ''),
      },
    })

    onBeforeMount(async () => {
      minimizeSupports.value = user.value.profile.minimize_supports
      filamentChoices.value = store.getters.filaments
      filament.value = filamentChoices.value.find((el) => el.value === user.value.profile.filament)
      printerChoices.value = store.getters.printers
      printer.value = printerChoices.value.find((el) => el.value === user.value.profile.printer)
    })

    function save() {
      userApi.csc
        .saveSettings({
          filament: filament.value?.value,
          printer: printer.value?.value,
          minimizeSupports: minimizeSupports.value,
        })
        .then(handleSuccess)
        .catch(handleFailure)
    }
    function handleSuccess(response) {
      store.dispatch('setUser', response)
      console.log('Saved!')
    }
    function handleFailure(error) {
      console.log(error)
    }

    return {
      filament,
      filamentChoices,
      printer,
      printerChoices,
      minimizeSupports,
      save,
      user: computed(() => store.getters.user),
    }
  },
}
</script>

<style>
@import 'vue-select/dist/vue-select.css';

.vs__selected {
  color: #ffffff;
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
