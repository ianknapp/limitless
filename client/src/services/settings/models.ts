import { z } from 'zod'

export const nameValueShape = {
  name: z.string(),
  value: z.string(),
}

export const nameIdShape = {
  name: z.string(),
  id: z.string().uuid(),
}

export const settingsShape = {
  supportStructures: z.array(z.object(nameValueShape)),
  supportTypes: z.array(z.object(nameValueShape)),
  adhesionTypes: z.array(z.object(nameValueShape)),
  printers: z.array(z.object(nameIdShape)),
}
