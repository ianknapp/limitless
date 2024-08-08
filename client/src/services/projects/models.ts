import { z } from 'zod'
import { baseModelShape } from '../base-model'

export const projectShape = {
  ...baseModelShape,
  title: z.string(),
  description: z.string().optional(),
  image: z.string().optional(),
}

export const printShape = {
  pk: z.string(),
  supportStructure: z.string(),
  supportType: z.string(),
  adhesionType: z.string(),
  printer: z.string(),
}
