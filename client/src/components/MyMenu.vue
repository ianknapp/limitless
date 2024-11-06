<template>
  <div class="h-50 mx-2 mb-12 flex flex-col p-4 text-left">
    <div class="flex flex-shrink-0 py-12 items-center justify-between">
      <h1 class="pt-2 pl-6 text-2xl font-bold">My Menu</h1>
      <button class="w-48 btn--primary bg-primary" @click.prevent="downloadPDF()">
        <span class="pt-1 font-semibold">Download Menu</span>
        <span>
          <img class="pl-6" src="@/assets/icons/download.png" />
        </span>
      </button>
    </div>
    <div
      class="flex gap-x-2 justify-between"
      v-for="scaled_recipe in recipes"
      :key="scaled_recipe.recipe.id"
    >
      <div class="my-2 py-2 pl-4 border rounded-lg flex justify-between">
        <div class="w-1/6 p-2 flex">
          <img
            class="m-auto rounded-lg pointer-events-none"
            :src="scaled_recipe.recipe.secondary_image"
          />
        </div>
        <div class="w-3/4 pr-12">
          <div class="pt-2 pl-2 mt-4 font-normal text-lg font-sans flex flex-wrap justify-left">
            {{ scaled_recipe.recipe.title }}
          </div>
          <div class="mt-4 mb-4 flex flex-wrap justify-left">
            <RecipeTag
              v-for="tag in scaled_recipe.recipe.mtm_tags"
              :tag="tag.name"
              :key="tag.name"
            />
            <RecipeTag
              v-for="tag in scaled_recipe.recipe.edamam_tags"
              :tag="tag.name"
              :key="tag.name"
            />
          </div>
        </div>
        <div class="w-28 pr-4 flex-none self-center">
          Servings:
          <span class="font-bold">{{ scaled_recipe.scale }}</span>
        </div>
      </div>
      <div class="border my-2 py-2 flex flex-none rounded-lg w-16">
        <button class="self-center pl-6" @click.prevent="removeRecipe(scaled_recipe.recipe)">
          <img src="@/assets/icons/trash_can.png" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { onBeforeMount, ref } from 'vue'
import { useStore } from 'vuex'
import RecipeTag from '@/components/RecipeTag.vue'
import { RecipeAPI } from '@/services/recipes'

export default {
  name: 'MyMenu',
  components: {
    RecipeTag,
  },
  setup() {
    const store = useStore()
    const recipes = ref()

    onBeforeMount(async () => {
      await getRecipes()
    })

    const getRecipes = async () => {
      await RecipeAPI.csc.myMenu().then(handleUpdateMenuSuccess).catch(handleFailure)
    }

    function removeRecipe(recipe) {
      RecipeAPI.csc
        .removeFromMenu({ pk: recipe.id })
        .then(handleRemovalSuccess)
        .catch(handleFailure)
    }
    function handleRemovalSuccess() {
      RecipeAPI.csc.myMenu().then(handleUpdateMenuSuccess).catch(handleFailure)
    }
    function handleUpdateMenuSuccess(response) {
      recipes.value = response
      store.dispatch(
        'setMyMenu',
        response.map((recipe) => recipe.id),
      )
    }

    function downloadPDF() {
      RecipeAPI.csc.downloadPDF().then(handlePdfSuccess).catch(handleFailure)
    }
    function handlePdfSuccess(response) {
      const link = document.createElement('a')
      link.href = URL.createObjectURL(new Blob([response], { type: 'application/pdf' }))
      let d = new Date()
      link.download = d.getMonth() + 1 + '_' + d.getDate() + '_' + d.getFullYear() + '_menu'
      link.click()
    }
    function handleFailure(error) {
      console.log(error)
    }

    return {
      downloadPDF,
      recipes,
      removeRecipe,
    }
  },
}
</script>
