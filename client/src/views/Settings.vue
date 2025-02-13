<template>
  <div class="settings-page">
    <nav class="settings-nav">
      <button @click="activeTab = 'settings'">Settings</button>
      <button @click="activeTab = 'projects'">My Projects</button>
      <button @click="activeTab = 'createProject'">Create Project</button>
      <button @click="activeTab = 'history'">History</button>
    </nav>
    <div class="settings-content">
      <component :is="activeTabComponent" />
    </div>
  </div>
</template>

<script>
import SettingsSection from '@/components/settings/SettingsSection.vue'
import CreateProject from '@/components/CreateProject.vue'
import HistorySettings from '@/components/settings/HistorySettings.vue'

export default {
  name: 'Settings',
  components: {
    SettingsSection,
    CreateProject,
    HistorySettings,
  },
  data() {
    return {
      activeTab: 'settings', // Default tab
    }
  },
  computed: {
    activeTabComponent() {
      switch (this.activeTab) {
        case 'settings':
          return 'SettingsSection'
        case 'projects':
          return 'ProjectSettings'
        case 'createProject':
          return 'CreateProject'
        case 'history':
          return 'HistorySettings'
        default:
          return 'SettingsSection'
      }
    },
  },
}
</script>

<style>
.settings-page {
  display: flex;
  flex-direction: column;
}
.settings-nav {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}
.settings-content {
  flex-grow: 1;
}
</style>

