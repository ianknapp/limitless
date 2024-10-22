<template>
  <div class="z-20 w-full fixed left-0 top-0 h-full backdrop-blur-sm p-4 flex items-center justify-center">
    <div class="bg-primaryLight rounded p-5 w-full h-full md:h-fit md:w-1/2 max-h-full flex flex-col items-center justify-evenly md:justify-between">
      <img
        src="@/assets/icons/x-mark.svg"
        alt="Close"
        class="self-end block h-6 w-6 cursor-pointer text-primary"
        @click="closeModal"
      />
      <header class="flex flex-col h-48 items-center md:w-1/2">
        <h2 class="text-primary lg:text-lg mb-3 m-0 font-bold">Ad Coming Soon</h2>
      </header>
      <main class="overflow-y-scroll">
        <slot></slot>
      </main>
      <footer class="flex gap-2 py-2">

        <button
          :disabled="loading"
          @click="submit"
          class="btn--primary bg-zinc-900"
        >
          Finish Advertisement
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Advertisement',
  emits: ['closeModal'],
  props: {
    loading: {
      type: Boolean,
    },
  },
  setup(props, context) {
    function closeModal() {
      context.emit('closeModal')
    }
    const submit = () => {
      // context.emit('submit')
      context.emit('closeModal')
    }
    return {
      closeModal,
      submit,
    }
  },
}
</script>
<style scoped></style>
