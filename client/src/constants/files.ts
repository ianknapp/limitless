export const assetTypeMap = {
  image: 'image/*',
  video: 'video/*',
  audio: 'audio/*',
  model: 'model/*',
  document: '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx',
}

const documentExtensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif']
const videoExtensions = ['.mp4', '.avi', '.mov']
const audioExtensions = ['.mp3', '.wav', '.flac']
const modelExtensions = ['.stl']

const documentEntries = documentExtensions.map((ext) => [ext, 'document'] as const)
const imageEntries = imageExtensions.map((ext) => [ext, 'image'] as const)
const videoEntries = videoExtensions.map((ext) => [ext, 'video'] as const)
const audioEntries = audioExtensions.map((ext) => [ext, 'audio'] as const)
const modelEntries = modelExtensions.map((ext) => [ext, 'model'] as const)

export const extensionResolveMap = new Map(
  [documentEntries, imageEntries, videoEntries, audioEntries, modelEntries].flat(),
)
