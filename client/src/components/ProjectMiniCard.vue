<template>
  <div class="text-left font-sans pb-4">
    <router-link
      :to="{ name: 'Project', params: { id: project.id } }"
      class="flex flex-shrink-0 items-center"
    >
      <div class="rounded-lg hover:bg-zinc-900/30 flex flex-row items-center">
        <div class="flex w-24 flex-none">
          <img class="rounded-lg pointer-events-none" :src="project.image" />
        </div>
        <div class="w-48 pl-6 font-semibold text-md flex-initial">
          {{ project.title }}
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'ProjectMiniCard',
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
