import Form, { FormField, IFormField } from '@thinknimble/tn-forms'

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
