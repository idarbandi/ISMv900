// Translation configuration for the application
export const translations = {
  // Status translations
  status: {
    'DELIVERED': 'تحویل داده شده',
    'REGISTERED': 'ثبت شده',
    'LOADING_UNLOADING': 'در حال بارگیری/تخلیه',
    'LOADED_UNLOADED': 'بارگیری/تخلیه شده',
    'OFFICE': 'دفتر',
    'CANCELLED': 'لغو شده',
    'IN_STOCK': 'موجود',
    'SOLD': 'فروخته شده',
    'MOVED': 'انتقال یافته'
  },

  // Shipment type translations
  shipmentType: {
    'INCOMING': 'ورودی',
    'OUTGOING': 'خروجی'
  },

  // Payment status translations
  paymentStatus: {
    'PAID': 'پرداخت شده',
    'TERMS': 'نسیه',
    'CANCELLED': 'لغو شده'
  },

  // Invoice status translations
  invoiceStatus: {
    'RECEIVED': 'دریافت شده',
    'NA': 'نامشخص',
    'SENT': 'ارسال شده'
  },

  // Location translations
  location: {
    'DELIVERED': 'تحویل داده شده',
    'ANBAR_MUHVATEH_KARDAN': 'انبار محوطه کردن',
    'ANBAR_AKHAL': 'انبار آخال',
    'ANBAR_KHAMIR_GHADIM': 'انبار خمیر قدیم',
    'ANBAR_KHAMIR_KORDAN': 'انبار خمیر کردن',
    'ANBAR_KOOCHAK': 'انبار کوچک',
    'ANBAR_PARVANDEH': 'انبار پرونده'
  },

  // Unload location translations
  unloadLocation: {
    'ANBAR_MUHVATEH_KARDAN': 'انبار محوطه کردن',
    'ANBAR_AKHAL': 'انبار آخال',
    'ANBAR_KHAMIR_GHADIM': 'انبار خمیر قدیم',
    'ANBAR_KHAMIR_KORDAN': 'انبار خمیر کردن',
    'ANBAR_KOOCHAK': 'انبار کوچک',
    'ANBAR_PARVANDEH': 'انبار پرونده',
    'FACTORY': 'کارخانه',
    'CUSTOMER': 'مشتری',
    'OTHER': 'سایر'
  },

  // Table headers translations
  tableHeaders: {
    'date': 'تاریخ',
    'status': 'وضعیت',
    'location': 'موقعیت',
    'receiveDate': 'تاریخ دریافت',
    'entryTime': 'زمان ورود',
    'weight1Time': 'زمان وزن اول',
    'weight2Time': 'زمان وزن دوم',
    'exitTime': 'زمان خروج',
    'shipmentType': 'نوع ارسال',
    'licenseNumber': 'شماره پلاک',
    'customerName': 'نام مشتری',
    'supplierName': 'نام تامین کننده',
    'weight1': 'وزن اول',
    'unloadLocation': 'موقعیت تخلیه',
    'unit': 'واحد',
    'quantity': 'تعداد',
    'quality': 'کیفیت',
    'penalty': 'جریمه',
    'weight2': 'وزن دوم',
    'netWeight': 'وزن خالص',
    'listOfReels': 'لیست رول‌ها',
    'profileName': 'نام پروفایل',
    'width': 'عرض',
    'salesId': 'کد فروش',
    'pricePerKg': 'قیمت هر کیلو',
    'totalPrice': 'قیمت کل',
    'extraCost': 'هزینه اضافی',
    'materialType': 'نوع مواد',
    'materialName': 'نام مواد',
    'vat': 'مالیات بر ارزش افزوده',
    'invoiceStatus': 'وضعیت فاکتور',
    'paymentStatus': 'وضعیت پرداخت',
    'documentInfo': 'اطلاعات سند',
    'comments': 'توضیحات',
    'cancellationReason': 'دلیل لغو',
    'username': 'نام کاربری',
    'logs': 'گزارش‌ها'
  }
}

// Helper function to translate a value based on its category
export const translate = (category, value) => {
  if (!value) return value
  return translations[category]?.[value] || value
}

// Helper function to translate table headers
export const translateHeader = (header) => {
  return translations.tableHeaders[header] || header
}

// Helper function to translate an entire object
export const translateObject = (obj, category) => {
  const translated = {}
  for (const [key, value] of Object.entries(obj)) {
    if (translations[category]?.[value]) {
      translated[key] = translations[category][value]
    } else {
      translated[key] = value
    }
  }
  return translated
}

// Helper function to translate multiple fields in an object
export const translateFields = (obj, fieldMappings) => {
  const translated = { ...obj }
  for (const [field, category] of Object.entries(fieldMappings)) {
    if (obj[field]) {
      translated[field] = translate(category, obj[field])
    }
  }
  return translated
}

// Helper function to translate table data
export const translateTableData = (data, fieldMappings) => {
  return data.map(item => translateFields(item, fieldMappings))
}

// Helper function to get translation options for select fields
export const getTranslationOptions = (category, includeEmpty = true) => {
  if (!translations[category]) {
    console.warn(`Translation category "${category}" not found`)
    return includeEmpty ? [{ value: '', label: 'همه' }] : []
  }

  const options = []
  if (includeEmpty) {
    options.push({ value: '', label: 'همه' })
  }
  
  for (const [value, label] of Object.entries(translations[category])) {
    options.push({ value, label })
  }
  
  return options
} 