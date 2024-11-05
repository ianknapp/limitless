import { z } from 'zod'
import { baseModelShape } from '../base-model'

export const projectShape = {
  ...baseModelShape,
  title: z.string(),
  description: z.string().optional(),
  primaryImage: z.any().optional(),
  secondaryImage: z.any().optional(),
  model: z.any().optional(),
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
