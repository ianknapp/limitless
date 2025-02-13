<template>
  <div>
    <h2>History</h2>
    <!-- Display saved and downloaded projects -->
    <ul>
      <li v-for="project in savedProjects" :key="project.id">
        {{ project.title }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HistorySettings',
  data() {
    return {
      savedProjects: [], // Fetch from API or store
    }
  },
  mounted() {
    // Fetch saved projects
  },
}
</script> 