<template>
  <div class="col-span-full relative">
    <div
      :class="`flex justify-center items-center rounded-lg border border-dashed border-black/25 px-6 py-10 relative ${props.containerClass}`"
    >
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          class="h-full sm:h-16 sm:w-16 relative"
          v-for="(assetItem, index) in assetsAsList"
          :key="index"
        >
          <div
            class="group aspect-h-1 aspect-w-2 overflow-hidden rounded-lg sm:aspect-none sm:relative sm:h-full"
          >
            <img
              v-if="assetItem.type.startsWith('image')"
              :src="assetItem.preview"
              class="object-cover object-center group-hover:opacity-75 sm:absolute sm:inset-0 sm:h-full sm:w-full"
            />
            <video
              v-else-if="assetItem.type.startsWith('video')"
              :src="assetItem.preview"
              class="object-cover object-center group-hover:opacity-75 sm:absolute sm:inset-0 sm:h-full sm:w-full"
            />
            <audio
              v-else-if="assetItem.type.startsWith('audio')"
              :src="assetItem.preview"
              controls
              class="object-cover object-center group-hover:opacity-75 sm:absolute sm:inset-0 sm:h-full sm:w-full"
            />
            <DocumentIcon
              v-else
              class="h-12 w-12 text-gray-500 group-hover:opacity-75 sm:absolute sm:inset-0 sm:h-full sm:w-full"
              aria-hidden="true"
            />

            <div
              aria-hidden="true"
              class="absolute inset-0 bg-gradient-to-b from-transparent to-black opacity-50 flex items-end p-2"
            >
              <span @click="onClearFileInput(index)">
                <XCircleIcon class="h-6 w-6 text-gray-500" aria-hidden="true" />
              </span>
            </div>
          </div>
        </div>
      </div>

      <button
        type="button"
        class="absolute top-1/2 -translate-x-1/2 -translate-y-1/2 left-1/2"
        v-if="!assetsAsList?.length"
        @click="onFileInputClick"
      >
        <div class="flex flex-col items-center">
          <DocumentPlusIcon class="h-12 w-12 text-gray-500" aria-hidden="true" />
          <p class="text-slate-400 text-sm text-center">Choose a File</p>
        </div>
      </button>
    </div>
    <section className="absolute top-2 right-6">
      <button
        type="button"
        v-if="assetsAsList?.length"
        class="sticky top-0"
        @click="onClearFileInput(null)"
      >
        <XCircleIcon class="h-10 w-10 text-gray-500" aria-hidden="true" />
      </button>
    </section>
    <div class="mt-4 flex text-sm leading-6 text-gray-400">
      <label
        for="file-upload"
        class="relative cursor-pointer rounded-md bg-gray-900 font-semibold text-white focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 focus-within:ring-offset-gray-900 hover:text-indigo-500"
      >
        <input
          ref="fileInput"
          id="file-upload"
          name="file-upload"
          type="file"
          class="sr-only"
          :accept="assetTypes"
          @change="handleFileChange"
        />
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FileUploadEmitDefinition, useFileUploadComponent } from '@/composables/FileUpload'
import { assetTypeMap } from '@/constants/files'
import { DocumentIcon, DocumentPlusIcon, XCircleIcon } from '@heroicons/vue/24/solid'
import { InputHTMLAttributes, useAttrs } from 'vue'

interface FileUploadInputProps extends /* @vue-ignore */ InputHTMLAttributes {
  assets?: File[]
  asset?: File | null
  assetTypes?: string
  containerClass?: string
}

const props = withDefaults(defineProps<FileUploadInputProps>(), {
  assets: () => [] as File[],
  asset: null,
  assetTypes: Object.values(assetTypeMap).join(', '),
  containerClass: '',
})

const attrs = useAttrs()
const emits = defineEmits<FileUploadEmitDefinition>()

const { handleFileChange, fileInput, onFileInputClick, onClearFileInput, assetsAsList } =
  useFileUploadComponent(props, emits, attrs)
</script>
