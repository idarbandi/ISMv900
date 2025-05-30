// Validation rules for all filter components
export const filterValidations = {
  // Common validations for all filters
  common: {
    startDate: {
      type: 'string',
      message: 'تاریخ شروع نامعتبر است',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (typeof value !== 'string') return 'تاریخ شروع باید متن باشد'
        return true
      }
    },
    endDate: {
      type: 'string',
      message: 'تاریخ پایان نامعتبر است',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (typeof value !== 'string') return 'تاریخ پایان باید متن باشد'
        return true
      }
    }
  },

  // Product filter validations
  product: {
    productReelNumber: {
      type: 'string',
      message: 'شماره رول باید متن باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (typeof value !== 'string') return 'شماره رول باید متن باشد'
        return true
      }
    },
    productWidth: {
      type: 'array',
      message: 'عرض باید از لیست انتخاب شود',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (!Array.isArray(value)) return 'عرض باید از لیست انتخاب شود'
        const validWidths = ['210', '220', '230', '240', '250']
        const invalidWidths = value.filter(width => !validWidths.includes(width))
        if (invalidWidths.length > 0) {
          return 'عرض انتخاب شده نامعتبر است'
        }
        return true
      }
    },
    productGsm: {
      type: 'number',
      message: 'GSM باید عدد باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const num = Number(value)
        if (isNaN(num)) return 'GSM باید عدد باشد'
        if (num < 0 || num > 1000) {
          return 'GSM باید بین 0 تا 1000 باشد'
        }
        return true
      }
    },
    productLength: {
      type: 'number',
      message: 'طول باید عدد باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const num = Number(value)
        if (isNaN(num)) return 'طول باید عدد باشد'
        if (num < 0 || num > 100000) {
          return 'طول باید بین 0 تا 100000 باشد'
        }
        return true
      }
    },
    productStatus: {
      type: 'string',
      enum: ['', 'In-stock', 'Sold', 'Moved', 'Delivered'],
      message: 'وضعیت نامعتبر است',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const validStatuses = ['', 'In-stock', 'Sold', 'Moved', 'Delivered']
        if (!validStatuses.includes(value)) return 'وضعیت نامعتبر است'
        return true
      }
    },
    productBreaks: {
      type: 'number',
      message: 'شکستگی باید عدد باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const num = Number(value)
        if (isNaN(num)) return 'شکستگی باید عدد باشد'
        if (num < 0) {
          return 'شکستگی نمی‌تواند منفی باشد'
        }
        return true
      }
    }
  },

  // Purchase filter validations
  purchase: {
    status: {
      type: 'string',
      enum: ['', 'Paid', 'Terms', 'Cancelled'],
      message: 'وضعیت نامعتبر است',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const validStatuses = ['', 'Paid', 'Terms', 'Cancelled']
        if (!validStatuses.includes(value)) return 'وضعیت نامعتبر است'
        return true
      }
    },
    invoiceStatus: {
      type: 'string',
      enum: ['', 'Received', 'NA'],
      message: 'وضعیت فاکتور نامعتبر است',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const validStatuses = ['', 'Received', 'NA']
        if (!validStatuses.includes(value)) return 'وضعیت فاکتور نامعتبر است'
        return true
      }
    },
    supplierName: {
      type: 'string',
      message: 'نام تامین کننده باید متن باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (typeof value !== 'string') return 'نام تامین کننده باید متن باشد'
        return true
      }
    },
    materialType: {
      type: 'string',
      message: 'نوع مواد باید متن باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (typeof value !== 'string') return 'نوع مواد باید متن باشد'
        return true
      }
    },
    materialName: {
      type: 'string',
      message: 'نام مواد باید متن باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        if (typeof value !== 'string') return 'نام مواد باید متن باشد'
        return true
      }
    },
    pricePerKg: {
      type: 'number',
      message: 'قیمت هر کیلو باید عدد باشد',
      validate: (value) => {
        if (!value) return true // Allow empty/null values
        const num = Number(value)
        if (isNaN(num)) return 'قیمت هر کیلو باید عدد باشد'
        if (num < 0) {
          return 'قیمت هر کیلو نمی‌تواند منفی باشد'
        }
        return true
      }
    }
  }
}

// Helper function to clean string values
const cleanStringValue = (value) => {
  if (!value) return value // Return null/undefined/empty as is
  if (typeof value === 'string') {
    return value.trim()
  }
  return value
}

// Helper function to handle empty object responses
export const handleEmptyResponse = (data) => {
  if (!data) return []
  if (Array.isArray(data)) {
    return data.filter(item => item && typeof item === 'object' && Object.keys(item).length > 0)
  }
  if (typeof data === 'object' && Object.keys(data).length === 0) {
    return []
  }
  return data
}

// Validation helper functions
export const validateField = (value, field, type) => {
  if (!value) return null // Allow empty/null values

  switch (field) {
    case 'status':
      if (type === 'purchase') {
        if (!['', 'Paid', 'Terms', 'Cancelled'].includes(value)) {
          return 'وضعیت نامعتبر است'
        }
      } else if (!['', 'DELIVERED', 'IN_TRANSIT', 'PENDING', 'CANCELLED'].includes(value)) {
        return 'وضعیت نامعتبر است'
      }
      return null
    case 'shipmentStatus':
      if (!['', 'DELIVERED', 'IN_TRANSIT', 'PENDING', 'CANCELLED'].includes(value)) {
        return 'وضعیت نامعتبر است'
      }
      return null
    case 'shipmentLocation':
      if (!['', 'DELIVERED', 'IN_TRANSIT', 'PENDING', 'CANCELLED'].includes(value)) {
        return 'موقعیت نامعتبر است'
      }
      return null
    case 'unloadLocation':
      if (!['', 'Anbar_Muhvateh_Kardan', 'Anbar_Asli', 'Anbar_Farangi'].includes(value)) {
        return 'محل تخلیه نامعتبر است'
      }
      return null
    case 'invoiceStatus':
      if (!['', 'NA', 'SENT', 'RECEIVED'].includes(value)) {
        return 'وضعیت فاکتور نامعتبر است'
      }
      return null
    case 'paymentStatus':
      if (!['', 'TERMS', 'PAID'].includes(value)) {
        return 'وضعیت پرداخت نامعتبر است'
      }
      return null
    case 'productStatus':
      if (!['', 'IN_STOCK', 'SOLD', 'MOVED', 'DELIVERED'].includes(value)) {
        return 'وضعیت نامعتبر است'
      }
      return null
    case 'productWidth':
      if (value && value.length > 0) {
        const validWidths = ['210', '220', '230', '240', '250']
        const invalidWidths = value.filter(width => !validWidths.includes(width))
        if (invalidWidths.length > 0) {
          return 'عرض انتخاب شده نامعتبر است'
        }
      }
      return null
    case 'productLength':
    case 'productGsm':
    case 'productBreaks':
    case 'pricePerKg':
      const num = Number(value)
      if (isNaN(num)) {
        return 'مقدار باید عدد باشد'
      }
      return null
    default:
      return null
  }
}

export const validateForm = (form, type) => {
  if (!form || typeof form !== 'object') {
    return { isValid: false, errors: { form: 'فرم نامعتبر است' } }
  }

  const errors = {}
  const validations = {
    ...filterValidations.common,
    ...filterValidations[type]
  }

  // Only validate fields that have values
  Object.keys(form).forEach(field => {
    if (form[field] !== '' && form[field] !== null && form[field] !== undefined) {
      const rules = validations[field]
      if (rules) {
        if (rules.validate) {
          const result = rules.validate(form[field])
          if (result !== true) {
            errors[field] = result
          }
        } else {
          const error = validateField(form[field], field, type)
          if (error !== null) {
            errors[field] = error
          }
        }
      }
    }
  })

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

// Helper function to clean form data
export const cleanFormData = (form) => {
  if (!form || typeof form !== 'object') {
    return {}
  }

  const cleaned = Object.entries(form).reduce((acc, [key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      // Clean string values before adding to cleaned form
      acc[key] = typeof value === 'string' ? value.trim() : value
    }
    return acc
  }, {})
  
  // Handle empty object responses
  return handleEmptyResponse(cleaned)
} 