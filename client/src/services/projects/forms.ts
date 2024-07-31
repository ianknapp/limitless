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
