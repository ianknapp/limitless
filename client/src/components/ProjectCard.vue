<template>
  <div class="text-left font-sans">
    <router-link
      :to="{ name: 'Project', params: { id: project.id } }"
      class="flex flex-shrink-0 items-center"
    >
      <div class="rounded-lg bg-zinc-900/30">
        <div class="mb-auto flex w-48 h-36 justify-center">
          <img class="rounded-lg flex-shrink max-h-full pointer-events-none" :src="project.image" />
        </div>
      </div>
    </router-link>
    <div class="pt-2 font-semibold text-sm text-center">
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
