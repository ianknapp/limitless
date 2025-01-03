<template>
  <section v-if="!inCreateMode">
    <button type="button" @click="inCreateMode = true" class="btn--primary bg-zinc-900">
      Create a new Project
    </button>
  </section>
  <div v-else class="pt-8 text-left xl:max-w-2xl h-full">
    <section class="flex justify-between">
      <h1 class="pt-2 pl-6 text-4xl font-bold">Create a new Project</h1>
      <button type="button" @click="inCreateMode = false" class="text-purple text-lg">
        Cancel
      </button>
    </section>
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
          :assets="form.imagesToUpload.value"
          :asset-types="assetTypeMap.image"
          multiple
          class="flex-grow flex flex-col overflow-y-auto"
          container-class="flex-grow overflow-y-auto"
        />
        <ul v-if="form.imagesToUpload.errors.length">
          <li
            v-for="(error, index) in form.imagesToUpload.errors"
            :key="index"
            v-text="error.message"
            class="input--error"
          />
        </ul>
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Model File</label>
        <FileField
          @update:asset="onModelChange"
          :asset="form.modelToUpload.value"
          :asset-types="assetTypeMap.model"
          class="flex-grow flex flex-col overflow-y-auto"
          container-class="flex-grow overflow-y-auto"
        />
        <ul v-if="form.modelToUpload.errors.length">
          <li
            v-for="(error, index) in form.modelToUpload.errors"
            :key="index"
            v-text="error.message"
            class="input--error"
          />
        </ul>
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
        <button class="btn--primary bg-zinc-900" @click.prevent="save()" :disabled="isCreating">
          Save
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import InputField from '@/components/inputs/InputField.vue'
import vSelect from 'vue-select'
import { ProjectForm, ProjectApi, projectQueries } from '@/services/projects'
import FileField from '@/components/inputs/FileField.vue'
import { assetTypeMap } from '@/constants/files'
import { useMutation, useQueryClient } from '@tanstack/vue-query'

export default {
  name: 'CreateProject',
  components: {
    FileField,
    InputField,
    vSelect,
  },
  setup() {
    const inCreateMode = ref(false)
    const store = useStore()
    const form = ref(new ProjectForm())
    const filamentChoices = ref([])
    const filament = ref()
    const user = computed(() => {
      return store.getters.user
    })
    const onMultipleImagesChange = (eventFiles) => {
      form.value.imagesToUpload.value = eventFiles
    }
    const onModelChange = (eventFile) => {
      form.value.modelToUpload.value = eventFile
    }

    onBeforeMount(async () => {
      filamentChoices.value = store.getters.filaments
      filament.value = filamentChoices.value.find((el) => el.value === user.value.profile.filament)
    })

    const queryClient = useQueryClient()

    const { mutate: createProject, isPending: isCreating } = useMutation({
      mutationFn: ProjectApi.csc.createProject,
    })

    function save() {
      const unwrappedForm = form.value
      unwrappedForm.recommendedFilament.value = filament.value?.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) {
        console.error(unwrappedForm.errors)
        return
      }
      const fileData = {
        model: form.value.modelToUpload.value,
        primaryImage: form.value.imagesToUpload.value[0],
        secondaryImage: form.value.imagesToUpload.value[1],
      }
      createProject(Object.assign({}, unwrappedForm.value, fileData), {
        onSuccess: () => {
          queryClient.invalidateQueries(projectQueries.all())
          console.log('Saved!')
          form.value = new ProjectForm()
        },
        onError: (error) => {
          console.error(error)
        },
      })
    }

    return {
      assetTypeMap,
      filament,
      filamentChoices,
      form,
      save,
      onMultipleImagesChange,
      onModelChange,
      isCreating,
      inCreateMode,
    }
  },
}
</script>

<style></style>
