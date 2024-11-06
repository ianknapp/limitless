<template>
  <div class="w-fit grid grid-cols-1 justify-center flex-wrap-reverse lg:flex-nowrap font-sans">
    <SettingsSection />
    <MyProjects />
    <CreateProject />
  </div>
</template>

<script>
import MyProjects from '@/components/MyProjects.vue'
import SettingsSection from '@/components/SettingsSection.vue'
import CreateProject from '@/components/CreateProject.vue'

export default {
  name: 'Settings',
  components: {
    CreateProject,
    MyProjects,
    SettingsSection,
  },
  setup() {
    return {}
  },
}
</script>

<style></style>
