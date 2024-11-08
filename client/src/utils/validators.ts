import { Validator } from '@thinknimble/tn-forms'

export class FileIsOfTypeValidator extends Validator<File> {
  types: string[]
  constructor(options: {
    message: string
    code: string
    isRequired?: boolean
    /**
     * The extensions to validate against
     */
    types: string[]
  }) {
    super(options)
    this.message = options.message
    this.isRequired = options.isRequired ?? false
    this.code = options.code
    this.types = options.types
  }
  call(value: File | File[]) {
    if (!value && !this.isRequired) return
    if (
      !(value instanceof File || (Array.isArray(value) && value.every((v) => v instanceof File)))
    ) {
      throw new Error(JSON.stringify({ code: this.code, message: this.message }))
    }
    const getFileExtension = (filename: string) => {
      return filename.split('.').pop()
    }
    const arrayValue = Array.isArray(value) ? value : [value]
    arrayValue.forEach((file) => {
      const extension = getFileExtension(file.name)
      if (!extension) throw new Error(JSON.stringify({ code: this.code, message: this.message }))
      if (!this.types.includes(extension)) {
        throw new Error(JSON.stringify({ code: this.code, message: this.message }))
      }
    })
  }
}
