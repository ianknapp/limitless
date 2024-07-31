<template>
  <div class="text-left">
    <router-link
      :to="{ name: 'Project', params: { id: project.id } }"
      class="flex flex-shrink-0 items-center"
    >
      <div class="rounded-lg bg-gray-100">
        <div class="mb-auto p-2">
          <img class="rounded-lg pointer-events-none" :src="project.image" />
        </div>
      </div>
    </router-link>
    <div class="pt-2 font-bold">
      {{ project.title }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectCard',
  components: {},
  computed: {},
  methods: {},
  props: {
    project: {
      type: Object,
      required: true,
    },
  },
}
</script>
