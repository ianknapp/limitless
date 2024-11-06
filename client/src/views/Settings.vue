<template>
  <div class="w-fit grid grid-cols-1 justify-center flex-wrap-reverse lg:flex-nowrap font-sans">
    <SettingsSection />
    <CreateProject />
  </div>
</template>

<script>
import SettingsSection from '@/components/SettingsSection.vue'
import CreateProject from '@/components/CreateProject.vue'

export default {
  name: 'Settings',
  components: {
    CreateProject,
    SettingsSection,
  },
  setup() {
    return {}
  },
}
</script>

<style></style>
