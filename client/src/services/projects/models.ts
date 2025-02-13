import { z } from 'zod'
import { baseModelShape } from '../base-model'

export const projectShape = {
  ...baseModelShape,
  title: z.string(),
  description: z.string().optional(),
  recommendedFilament: z.string().optional(),
  primaryImage: z.string(),
  secondaryImage: z.string(),
  model: z.string(),
  recentlyViewed: z.boolean().optional(),
}

export const simplifiedProjectShape = {
  id: projectShape.id,
  title: projectShape.title,
  image: projectShape.primaryImage,
  recentlyViewed: projectShape.recentlyViewed,
}

export const printShape = {
  pk: z.string(),
  supportStructure: z.string(),
  supportType: z.string(),
  adhesionType: z.string(),
  filament: z.string(),
  printer: z.string(),
  minimizeSupports: z.boolean().optional(),
  layerHeight: z.number().min(0.001).max(0.8),
  initialLayerHeight: z.number().min(0.001).max(0.8),
}

export const projectFiltersShape = {
  search: z.string(),
  recentlyViewed: z.string(),
}
