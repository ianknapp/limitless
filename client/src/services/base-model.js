import { z } from 'zod'
import { readonly } from '@thinknimble/tn-models'

export const baseModelShape = {
  pk: z.string().uuid(),
  created: readonly(z.string().datetime().optional()),
  lastEdited: readonly(z.string().datetime().optional()),
}
