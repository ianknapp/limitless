<template>
  <div class="pt-8 text-left xl:max-w-2xl h-full">
    <h1 class="pt-2 pl-6 pt-12 text-4xl font-bold">Create a new Project</h1>
    <div class="mt-8 mb-2 pt-4 grid grid-cols-1 gap-6 pl-6 content-end pb-12">
      <span>
        <label class="mx-2 font-sans capitalize">Title</label>
        <InputField
          v-model:value="form.title.value"
          :errors="form.title.errors"
          @blur="form.title.validate()"
          placeholder="Model Name"
        />
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Description</label>
        <InputField
          v-model:value="form.description.value"
          :errors="form.description.errors"
          @blur="form.description.validate()"
          placeholder="Model Description"
        />
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Images</label>
        <FileField
          @update:assets="onMultipleImagesChange"
          :assets="imagesToUpload"
          :asset-types="assetTypeMap.image"
          multiple
          class="flex-grow flex flex-col overflow-y-auto"
          container-class="flex-grow overflow-y-auto"
        />
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Model File</label>
        <FileField
          @update:asset="onModelChange"
          :asset="modelToUpload"
          :asset-types="assetTypeMap.model"
          class="flex-grow flex flex-col overflow-y-auto"
          container-class="flex-grow overflow-y-auto"
        />
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Recommended Filament</label>
        <v-select
          class="w-96"
          :options="filamentChoices"
          v-model="filament"
          label="label"
          placeholder="select your default..."
        ></v-select>
      </span>
      <div class="w-24">
        <button class="btn--primary bg-zinc-900" @click.prevent="save()">Save</button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount, h } from 'vue'
import { useStore } from 'vuex'
import InputField from '@/components/inputs/InputField.vue'
import vSelect from 'vue-select'
import { ProjectForm, ProjectApi } from '@/services/projects'
import FileField from '@/components/inputs/FileField.vue'
import { assetTypeMap } from '@/constants/files'

export default {
  name: 'CreateProject',
  components: {
    FileField,
    InputField,
    vSelect,
  },
  setup() {
    const store = useStore()
    const form = ref(new ProjectForm())
    const filamentChoices = ref([])
    const filament = ref()
    const user = computed(() => {
      return store.getters.user
    })
    const imagesToUpload = ref([])
    const onMultipleImagesChange = (eventFiles) => {
      imagesToUpload.value = eventFiles
    }
    const modelToUpload = ref()
    const onModelChange = (eventFile) => {
      modelToUpload.value = eventFile
    }

    onBeforeMount(async () => {
      filamentChoices.value = store.getters.filaments
      filament.value = filamentChoices.value.find((el) => el.value === user.value.profile.filament)
    })

    function save() {
      const unwrappedForm = form.value
      unwrappedForm.recommendedFilament.value = filament.value?.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return
      const fileData = {
        model: modelToUpload.value,
        primaryImage: imagesToUpload.value[0],
        secondaryImage: imagesToUpload.value[1],
      }
      ProjectApi.csc
        .createProject(Object.assign({}, unwrappedForm.value, fileData))
        .then(handleSuccess)
        .catch(handleFailure)
    }
    function handleSuccess(response) {
      console.log('Saved!')
    }
    function handleFailure(error) {
      console.log(error)
    }

    return {
      assetTypeMap,
      filament,
      filamentChoices,
      form,
      save,
      imagesToUpload,
      onMultipleImagesChange,
      modelToUpload,
      onModelChange,
    }
  },
}
</script>

<style></style>
