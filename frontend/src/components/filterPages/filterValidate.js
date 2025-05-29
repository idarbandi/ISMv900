// Validation rules for all filter components
export const filterValidations = {
  // Common validations for all filters
  common: {
    startDate: {
      type: 'string',
      message: 'تاریخ شروع نامعتبر است'
    },
    endDate: {
      type: 'string',
      message: 'تاریخ پایان نامعتبر است'
    }
  },

  // Product filter validations
  product: {
    productReelNumber: {
      type: 'string',
      message: 'شماره رول باید متن باشد'
    },
    productWidth: {
      type: 'array',
      message: 'عرض باید از لیست انتخاب شود',
      validate: (value) => {
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
        if (value && (value < 0 || value > 1000)) {
          return 'GSM باید بین 0 تا 1000 باشد'
        }
        return true
      }
    },
    productLength: {
      type: 'number',
      message: 'طول باید عدد باشد',
      validate: (value) => {
        if (value && (value < 0 || value > 100000)) {
          return 'طول باید بین 0 تا 100000 باشد'
        }
        return true
      }
    },
    productStatus: {
      type: 'string',
      enum: ['', 'In-stock', 'Sold', 'Moved', 'Delivered'],
      message: 'وضعیت نامعتبر است'
    },
    productBreaks: {
      type: 'number',
      message: 'شکستگی باید عدد باشد',
      validate: (value) => {
        if (value && value < 0) {
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
      message: 'وضعیت نامعتبر است'
    },
    invoiceStatus: {
      type: 'string',
      enum: ['', 'Received', 'NA'],
      message: 'وضعیت فاکتور نامعتبر است'
    },
    supplierName: {
      type: 'string',
      message: 'نام تامین کننده باید متن باشد'
    },
    materialType: {
      type: 'string',
      message: 'نوع مواد باید متن باشد'
    },
    materialName: {
      type: 'string',
      message: 'نام مواد باید متن باشد'
    },
    pricePerKg: {
      type: 'number',
      message: 'قیمت هر کیلو باید عدد باشد',
      validate: (value) => {
        if (value && value < 0) {
          return 'قیمت هر کیلو نمی‌تواند منفی باشد'
        }
        return true
      }
    }
  }
}

// Helper function to clean string values
const cleanStringValue = (value) => {
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
  switch (field) {
    case 'status':
      if (type === 'purchase') {
        if (value && !['Paid', 'Terms', 'Cancelled'].includes(value)) {
          return 'وضعیت نامعتبر است'
        }
      } else if (value && !['DELIVERED', 'IN_TRANSIT', 'PENDING', 'CANCELLED'].includes(value)) {
        return 'وضعیت نامعتبر است'
      }
      return null
    case 'shipmentStatus':
      if (value && !['DELIVERED', 'IN_TRANSIT', 'PENDING', 'CANCELLED'].includes(value)) {
        return 'وضعیت نامعتبر است'
      }
      return null
    case 'shipmentLocation':
      if (value && !['DELIVERED', 'IN_TRANSIT', 'PENDING', 'CANCELLED'].includes(value)) {
        return 'موقعیت نامعتبر است'
      }
      return null
    case 'unloadLocation':
      if (value && !['Anbar_Muhvateh_Kardan', 'Anbar_Asli', 'Anbar_Farangi'].includes(value)) {
        return 'محل تخلیه نامعتبر است'
      }
      return null
    case 'invoiceStatus':
      if (value && !['NA', 'SENT', 'RECEIVED'].includes(value)) {
        return 'وضعیت فاکتور نامعتبر است'
      }
      return null
    case 'paymentStatus':
      if (value && !['TERMS', 'PAID'].includes(value)) {
        return 'وضعیت پرداخت نامعتبر است'
      }
      return null
    case 'productStatus':
      if (value && !['IN_STOCK', 'SOLD', 'MOVED', 'DELIVERED'].includes(value)) {
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
      if (value && isNaN(Number(value))) {
        return 'مقدار باید عدد باشد'
      }
      return null
    default:
      return null
  }
}

export const validateForm = (form, type) => {
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
        const error = validateField(form[field], field, type)
        if (error !== null) {
          errors[field] = error
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