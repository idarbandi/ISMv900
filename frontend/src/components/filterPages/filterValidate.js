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
      type: 'number',
      message: 'عرض باید عدد باشد',
      validate: (value) => {
        if (value && (value < 0 || value > 10000)) {
          return 'عرض باید بین 0 تا 10000 باشد'
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
    minQuantity: {
      type: 'number',
      message: 'حداقل تعداد باید عدد باشد',
      validate: (value, form) => {
        if (value && form.maxQuantity && value > form.maxQuantity) {
          return 'حداقل تعداد نمی‌تواند بیشتر از حداکثر باشد'
        }
        return true
      }
    },
    maxQuantity: {
      type: 'number',
      message: 'حداکثر تعداد باید عدد باشد',
      validate: (value, form) => {
        if (value && form.minQuantity && value < form.minQuantity) {
          return 'حداکثر تعداد نمی‌تواند کمتر از حداقل باشد'
        }
        return true
      }
    },
    minWeight: {
      type: 'number',
      message: 'حداقل وزن باید عدد باشد',
      validate: (value, form) => {
        if (value && form.maxWeight && value > form.maxWeight) {
          return 'حداقل وزن نمی‌تواند بیشتر از حداکثر باشد'
        }
        return true
      }
    },
    maxWeight: {
      type: 'number',
      message: 'حداکثر وزن باید عدد باشد',
      validate: (value, form) => {
        if (value && form.minWeight && value < form.minWeight) {
          return 'حداکثر وزن نمی‌تواند کمتر از حداقل باشد'
        }
        return true
      }
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
    },
    totalPrice: {
      type: 'number',
      message: 'قیمت کل باید عدد باشد',
      validate: (value) => {
        if (value && value < 0) {
          return 'قیمت کل نمی‌تواند منفی باشد'
        }
        return true
      }
    },
    extraCost: {
      type: 'number',
      message: 'هزینه اضافی باید عدد باشد',
      validate: (value) => {
        if (value && value < 0) {
          return 'هزینه اضافی نمی‌تواند منفی باشد'
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
export const validateField = (value, rules) => {
  if (!rules) return true

  // Clean string values before validation
  const cleanedValue = cleanStringValue(value)

  // Check type
  if (rules.type && typeof cleanedValue !== rules.type) {
    return rules.message
  }

  // Check enum
  if (rules.enum && !rules.enum.includes(cleanedValue)) {
    return rules.message
  }

  // Run custom validation
  if (rules.validate) {
    const result = rules.validate(cleanedValue)
    if (result !== true) {
      return result
    }
  }

  return true
}

export const validateForm = (form, type) => {
  const errors = {}
  const validations = {
    ...filterValidations.common,
    ...filterValidations[type]
  }

  Object.keys(form).forEach(field => {
    const rules = validations[field]
    if (rules) {
      const error = validateField(form[field], rules)
      if (error !== true) {
        errors[field] = error
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