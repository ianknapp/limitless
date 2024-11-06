import { Ref, computed, onMounted, ref, toRefs } from 'vue'

type PendingFileUpload = File & {
  preview: string
}

type Data = Record<string, unknown>
type Attrs = Data

interface Props {
  assets?: File[] | null
  asset?: File | null
  assetTypes?: string
}

export type FileUploadEmitDefinition = {
  'files-ready': []
  'update:assets': [files: File[]]
  'update:asset': [file: File | null]
}

//! This would be the ideal  but doesn't work
// type FileUploadEmits = ReturnType<typeof defineEmits<FileUploadEmitDefinition>>
//TODO: We could probably do some type helper here. The typescript definition for `defineEmits` is a bit broken so we cannot infer from it's TS definition return type. Here we're just hardcoding the result. If any other event is going to be emitted, then we would have to update this.
type FileUploadEmits = ((evt: 'update:assets', files: File[]) => void) &
  ((evt: 'update:asset', file: File | null) => void) &
  ((evt: 'files-ready') => void)

export function useFileUploadComponent(
  props: Props,
  emit: FileUploadEmits,
  attrs: Attrs | null = null,
) {
  const isSingleFile = attrs?.multiple === undefined
  const fileInput: Ref<HTMLInputElement | null> = ref(null)

  const { assets, asset, assetTypes } = toRefs(props)

  const assetsAsList = computed(() => {
    if (!isSingleFile) {
      return (assets?.value ? assets.value : []) as PendingFileUpload[]
    }
    return (asset?.value ? [asset.value] : []) as PendingFileUpload[]
  })

  onMounted(() => {
    if (!isSingleFile) {
      fileInput?.value?.setAttribute('multiple', '')
    }
  })

  const updateAssets = (value: File | File[] | null) => {
    Array.isArray(value) ? emit('update:assets', value) : emit('update:asset', value)
  }

  const onFileInputClick = () => {
    fileInput.value?.click()
  }

  const onClearFileInput = (index: number | null = null) => {
    // if no file passed clear all
    if (index == null || index == undefined) {
      updateAssets(isSingleFile ? null : [])
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    } else {
      if (!isSingleFile && Array.isArray(assetsAsList.value)) {
        const updatedAssets = [...assetsAsList.value]
        updatedAssets.splice(index, 1)
        updateAssets(updatedAssets)
      } else if (isSingleFile) {
        updateAssets(null)
      }
    }
  }

  const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    const f = target.files

    if (f) {
      const files: File[] = []
      Object.values(f).forEach((file: File) => {
        const pendingFile = file as PendingFileUpload
        pendingFile['preview'] = URL.createObjectURL(file)
        files.push(file)
      })
      updateAssets(isSingleFile ? files[0] : files)
    }
  }

  return {
    assets,
    asset,
    assetTypes,
    fileInput,
    onFileInputClick,
    onClearFileInput,
    handleFileChange,
    updateAssets,
    assetsAsList,
    isSingleFile,
  }
}
