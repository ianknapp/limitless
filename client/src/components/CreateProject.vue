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
        <label class="mx-2 font-sans capitalize">Primary Image</label>
        <InputField
          v-model:value="form.primaryImage.value"
          :errors="form.primaryImage.errors"
          @blur="form.primaryImage.validate()"
          placeholder="Image URL"
        />
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Secondary Image</label>
        <InputField
          v-model:value="form.secondaryImage.value"
          :errors="form.secondaryImage.errors"
          @blur="form.secondaryImage.validate()"
          placeholder="Image URL"
        />
      </span>
      <span>
        <label class="mx-2 font-sans capitalize">Model File</label>
        <InputField
          v-model:value="form.model.value"
          :errors="form.model.errors"
          @blur="form.model.validate()"
          placeholder="(.stl, etc)"
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

export default {
  name: 'CreateProject',
  components: {
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

    onBeforeMount(async () => {
      filamentChoices.value = store.getters.filaments
      filament.value = filamentChoices.value.find((el) => el.value === user.value.profile.filament)
    })

    function save() {
      const unwrappedForm = form.value
      unwrappedForm.recommendedFilament.value = filament.value.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return
      ProjectApi.create(unwrappedForm.value).then(handleSuccess).catch(handleFailure)
    }
    function handleSuccess(response) {
      console.log('Saved!')
    }
    function handleFailure(error) {
      console.log(error)
    }

    return {
      filament,
      filamentChoices,
      form,
      save,
    }
  },
}
</script>

<style></style>
