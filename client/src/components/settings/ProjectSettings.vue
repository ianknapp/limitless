<template>
  <div>
    <h2>My Projects</h2>
    <!-- Display user's projects -->
    <ul>
      <li v-for="project in userProjects" :key="project.id">
        {{ project.title }}
      </li>
    </ul>
    <button @click="createNewProject">Create New Project</button>
  </div>
</template>

<script>
export default {
  name: 'ProjectSettings',
  data() {
    return {
      userProjects: [], // Fetch from API or store
    }
  },
  methods: {
    createNewProject() {
      // Navigate to project creation page
      this.$router.push({ name: 'CreateProject' })
    },
  },
  mounted() {
    // Fetch user's projects
  },
}
</script> 