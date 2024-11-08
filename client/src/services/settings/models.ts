import { GetInferredFromRaw } from '@thinknimble/tn-models'
import { z } from 'zod'

export const nameValueShape = {
  label: z.string(),
  value: z.string(),
}

export type NameValueShape = GetInferredFromRaw<typeof nameValueShape>

export const nameIdShape = {
  name: z.string(),
  id: z.string().uuid(),
}

export type NameIdShape = GetInferredFromRaw<typeof nameIdShape>

export const settingsShape = {
  filaments: z.array(z.object(nameValueShape)),
  supportStructures: z.array(z.object(nameValueShape)),
  supportTypes: z.array(z.object(nameValueShape)),
  adhesionTypes: z.array(z.object(nameValueShape)),
  printers: z.array(z.object(nameValueShape)),
}

export type SettingsShape = GetInferredFromRaw<typeof settingsShape>
