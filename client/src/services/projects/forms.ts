import Form, { FormField, IFormField, RequiredValidator } from '@thinknimble/tn-forms'

export type PrintFormInputs = {
  printer: IFormField<string>
}
export type TPrintForm = PrintFormInputs & PrintForm

export class PrintForm extends Form<PrintFormInputs> {
  static printer = new FormField({
    placeholder: 'Printer',
    type: 'text',
    validators: [],
  })
}

export type SearchFormInputs = {
  query: IFormField<string>
}
export type TSearchForm = SearchFormInputs & SearchForm

export class SearchForm extends Form<SearchFormInputs> {
  static query = new FormField({
    placeholder: 'Search Models',
    type: 'text',
    validators: [],
  })
}

export type ProjectFormInputs = {
  title: IFormField<string>
  description: IFormField<string>
  primaryImage: IFormField<string>
  secondaryImage: IFormField<string>
  model: IFormField<string>
  recommendedFilament: IFormField<string>
}

export class ProjectForm extends Form<ProjectFormInputs> {
  static title = FormField.create({
    label: 'Title',
    placeholder: 'Title',
    type: 'text',
    validators: [new RequiredValidator({ message: 'Please enter a title' })],
    value: '',
  })

  static description = FormField.create({
    label: 'Description',
    placeholder: 'Description',
    type: 'text',
    validators: [new RequiredValidator({ message: 'Please enter a description' })],
    value: '',
  })

  static primaryImage = FormField.create({
    label: 'Primary Image',
    placeholder: 'Primary Image',
    type: 'text',
    validators: [new RequiredValidator({ message: 'Please enter a primary image' })],
    value: '',
  })

  static secondaryImage = FormField.create({
    label: 'Secondary Image',
    placeholder: 'Secondary Image',
    type: 'text',
    validators: [new RequiredValidator({ message: 'Please enter a secondary image' })],
    value: '',
  })

  static model = FormField.create({
    label: 'Model',
    placeholder: 'Model',
    type: 'text',
    validators: [new RequiredValidator({ message: 'Please enter a model' })],
    value: '',
  })

  static recommendedFilament = FormField.create({
    label: 'Recommended Filament',
    placeholder: 'Recommended Filament',
    type: 'text',
    validators: [new RequiredValidator({ message: 'Please enter a recommended filament' })],
    value: '',
  })
}
export type TProjectForm = ProjectForm & ProjectFormInputs
