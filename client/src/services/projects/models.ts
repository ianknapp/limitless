import { z } from 'zod'
import { baseModelShape } from '../base-model'

export const projectShape = {
  ...baseModelShape,
  title: z.string(),
  image: z.string().optional(),
}
