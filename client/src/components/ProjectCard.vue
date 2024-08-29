<template>
  <div class="text-left font-sans w-48 h-36">
    <router-link
      :to="{ name: 'Project', params: { id: project.id } }"
      class="flex flex-shrink-0 items-center"
    >
      <div
        class="rounded-lg w-48 h-36 bg-zinc-900 bg-contain bg-center"
        :style="{ 'background-image': `url(${project.image})` }"
      ></div>
    </router-link>
    <div class="pt-2 font-semibold text-sm">
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
