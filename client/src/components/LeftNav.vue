<template>
  <div v-if="expandLeftNav" id="leftNav" class="flex-initial shadow hidden sm:inline-block">
    <div class="mx-auto px-8">
      <div class="flex flex-col h-16 justify-between">
        <div class="flex flex-row gap-4 font-sans w-fit mr-12 py-12 px-8">
          <img class="mx-auto w-8" src="@/assets/icons/glyph.png" alt="Limitless" />
          <div
            class="text-center self-center text-4xl w-fit font-semibold leading-9 tracking-tight text-primary"
          >
            Limitless
          </div>
        </div>
        <router-link :to="{ name: 'Home' }" class="router" active-class="active">
          <img class="pr-4" src="@/assets/icons/home.png" alt="Home" />
          Home
        </router-link>
        <div class="flex flex-col gap-4 justify-start pt-16 font-semibold w-72">
          <div class="font-sans text-left">Recently Viewed</div>
          <ProjectMiniCard v-for="project in projects.list" :project="project" :key="project.id" />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="hidden sm:inline-block pt-8">
    <div class="mx-auto max-w-7xl pl-8">
      <div class="justify-between">
        <div class="w-6 pt-6">
          <img class="mx-auto" src="@/assets/icons/glyph.png" alt="Limitless" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onBeforeMount, triggerRef } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import ProjectMiniCard from '@/components/ProjectMiniCard.vue'
import { projectFunctions } from '@/services/projects'
import { userApi } from '@/services/users'

export default {
  name: 'LeftNav',
  components: {
    ProjectMiniCard,
  },
  props: {
    expandLeftNav: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const { projectCollection, projectFilters } = projectFunctions()
    const projects = ref(projectCollection)
    let mobileMenuOpen = ref(false)
    let profileMenuOpen = ref(false)

    const getProjects = async () => {
      projectFilters.recentlyViewed = 'true'
      await projects.value.refresh()
      triggerRef(projects)
      store.dispatch('setProjects', projects.value.list)
    }
    async function logout() {
      try {
        await userApi.csc.logout()
      } catch (error) {
        if (error.response && error.response.status === 401) {
          console.error('User is not logged in')
        }
        console.log(error)
      } finally {
        profileMenuOpen.value = false
        mobileMenuOpen.value = false
        store.dispatch('setUser', null)
        router.push({ name: 'Home' })
      }
    }
    onBeforeMount(async () => {
      await getProjects()
    })

    return {
      logout,
      isLoggedIn: computed(() => store.getters.isLoggedIn),
      user: computed(() => store.getters.user),
      mobileMenuOpen,
      profileMenuOpen,
      projects,
    }
  },
}
</script>
<style scoped>
.mobile-link {
  @apply block cursor-pointer border-l-4 px-4 py-2 text-base font-medium hover:bg-gray-100 hover:text-gray-800;
}

.mobile-link--main {
  @apply block border-l-4 py-2 pl-3 pr-4 text-base font-medium hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700;
}
</style>
