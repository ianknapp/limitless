import { z } from 'zod'
import { baseModelShape } from '../base-model'

export const printerShape = {
  ...baseModelShape,
  name: z.string(),
}
