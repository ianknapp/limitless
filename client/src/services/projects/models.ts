import { z } from 'zod'
import { baseModelShape } from '../base-model'

export const projectShape = {
  ...baseModelShape,
  title: z.string(),
  description: z.string().optional(),
  primaryImage: z.string().optional(),
  secondaryImage: z.string().optional(),
  model: z.string().optional(),
  recentlyViewed: z.boolean().optional(),
}

export const printShape = {
  pk: z.string(),
  supportStructure: z.string(),
  supportType: z.string(),
  adhesionType: z.string(),
  filament: z.string(),
  printer: z.string(),
  minimizeSupports: z.boolean().optional(),
}

export const projectFiltersShape = {
  search: z.string(),
  recentlyViewed: z.string(),
}
