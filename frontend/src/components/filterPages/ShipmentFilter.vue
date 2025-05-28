<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold mb-6">فیلتر بارنامه</h2>
    
    <!-- Error Message -->
    <div v-if="error" class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="mb-4 p-4 bg-blue-100 border border-blue-400 text-blue-700 rounded">
      Loading...
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Date Range -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ شروع</label>
        <input 
          type="date" 
          v-model="filters.startDate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ پایان</label>
        <input 
          type="date" 
          v-model="filters.endDate"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Status and Type -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت</label>
        <select 
          v-model="filters.shipmentStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option v-for="option in statusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نوع بارنامه</label>
        <select 
          v-model="filters.shipmentType"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option v-for="option in shipmentTypeOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Location -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">موقعیت</label>
        <select 
          v-model="filters.shipmentLocation"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option v-for="option in locationOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Unload Location -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">محل تخلیه</label>
        <select 
          v-model="filters.unloadLocation"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option v-for="option in unloadLocationOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Vehicle and Customer -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">شماره پلاک</label>
        <input 
          type="text" 
          v-model="filters.licenseNumber"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام مشتری</label>
        <input 
          type="text" 
          v-model="filters.customerName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Supplier and Material -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام تامین کننده</label>
        <input 
          type="text" 
          v-model="filters.supplierName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نوع مواد</label>
        <input 
          type="text" 
          v-model="filters.materialType"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">نام مواد</label>
        <input 
          type="text" 
          v-model="filters.materialName"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Weights -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وزن اول</label>
          <input 
            type="number" 
          v-model="filters.weight1"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وزن دوم</label>
          <input 
            type="number" 
          v-model="filters.weight2"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وزن خالص</label>
          <input 
          type="text" 
          v-model="filters.netWeight"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
      </div>

      <!-- Prices -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت هر کیلو</label>
          <input 
            type="number" 
          v-model="filters.pricePerKg"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت کل</label>
          <input 
            type="number" 
          v-model="filters.totalPrice"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">هزینه اضافی</label>
          <input 
            type="number" 
          v-model="filters.extraCost"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
        </div>

      <!-- Status -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت فاکتور</label>
        <select 
          v-model="filters.invoiceStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option v-for="option in invoiceStatusOptions" :value="option.value" :key="option.value">{{ option.label }}</option>
        </select>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">وضعیت پرداخت</label>
        <select 
          v-model="filters.paymentStatus"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option v-for="option in paymentStatusOptions" :value="option.value" :key="option.value">{{ option.label }}</option>
        </select>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="mt-6 flex justify-end space-x-4">
      <button 
        @click="resetFilters"
        class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loading"
      >
        پاک کردن
      </button>
      <button 
        @click="applyFilters"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loading"
      >
        {{ loading ? 'Loading...' : 'اعمال فیلتر' }}
      </button>
    </div>
  </div>
</template>

<script>
import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo'
import { validateForm, cleanFormData, handleEmptyResponse } from './filterValidate'
import { translate, getTranslationOptions } from '@/config/translations'

export default {
  name: 'ShipmentFilter',
  data() {
    return {
      filters: {
        startDate: '',
        endDate: '',
        shipmentStatus: '',
        shipmentType: '',
        shipmentLocation: '',
        unloadLocation: '',
        licenseNumber: '',
        customerName: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        weight1: '',
        weight2: '',
        netWeight: '',
        pricePerKg: '',
        totalPrice: '',
        extraCost: '',
        invoiceStatus: '',
        paymentStatus: ''
      },
      statusOptions: [
        { value: '', label: 'همه' },
        { value: 'DELIVERED', label: 'تحویل داده شده' },
        { value: 'IN_TRANSIT', label: 'در حال انتقال' },
        { value: 'PENDING', label: 'در انتظار' },
        { value: 'CANCELLED', label: 'لغو شده' }
      ],
      shipmentTypeOptions: [
        { value: '', label: 'همه' },
        { value: 'INCOMING', label: 'ورودی' },
        { value: 'OUTGOING', label: 'خروجی' }
      ],
      locationOptions: [
        { value: '', label: 'همه' },
        { value: 'DELIVERED', label: 'تحویل داده شده' },
        { value: 'IN_TRANSIT', label: 'در حال انتقال' },
        { value: 'PENDING', label: 'در انتظار' },
        { value: 'CANCELLED', label: 'لغو شده' }
      ],
      unloadLocationOptions: [
        { value: '', label: 'همه' },
        { value: 'Anbar_Muhvateh_Kardan', label: 'انبار محوطه کردان' },
        { value: 'Anbar_Asli', label: 'انبار اصلی' },
        { value: 'Anbar_Farangi', label: 'انبار فرنگی' }
      ],
      invoiceStatusOptions: getTranslationOptions('invoiceStatus'),
      paymentStatusOptions: getTranslationOptions('paymentStatus'),
      loading: false,
      error: null,
      fieldErrors: {},
      shipments: [],
      filteredShipments: []
    }
  },
  async created() {
    await this.loadShipments()
  },
  methods: {
    translateValue(value, type) {
      const translations = {
        location: {
          'DELIVERED': 'تحویل داده شده',
          'IN_TRANSIT': 'در حال انتقال',
          'PENDING': 'در انتظار',
          'CANCELLED': 'لغو شده'
        },
        shipmentType: {
          'INCOMING': 'ورودی',
          'OUTGOING': 'خروجی'
        },
        status: {
          'DELIVERED': 'تحویل داده شده',
          'IN_TRANSIT': 'در حال انتقال',
          'PENDING': 'در انتظار',
          'CANCELLED': 'لغو شده'
        },
        unloadLocation: {
          'ANBAR_MUHVATEH_KARDAN': 'انبار محوطه کردان',
          'Anbar_Sangin': 'انبار محوطه سنگین',
          "Anbar_Khamir_Kordan": "انبار خمیر کردان",
          "Anbar_Muhavateh_Homayoun": "انبار محوطه همایون",
          "Anbar_Khamir_Ghadim": "انبار خمیر قدیم",
          "Anbar_Salon_Tolid": "انبار سالن تولید",
          'ANBAR_ASLI': 'انبار اصلی',
          "Anbar_PAK": "انبار پاک",
          'ANBAR_FARANGI': 'انبار فرنگی'
        }
      }

      // Convert both the input value and the translation keys to uppercase for comparison
      const upperValue = value?.toUpperCase()
      const translationMap = translations[type] || {}
      const translatedValue = Object.entries(translationMap).find(([key]) => 
        key.toUpperCase() === upperValue
      )?.[1]

      console.log(`Translating ${type}: ${value} -> ${translatedValue || value}`)
      return translatedValue || value
    },
    async loadShipments() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query GetAllShipments {
              filteredData(filterInput: { 
                shipmentStatus: null,
                shipmentType: null,
                shipmentLocation: null,
                licenseNumber: null,
                customerName: null,
                supplierName: null,
                materialType: null,
                materialName: null,
                invoiceStatus: null,
                paymentStatus: null,
                startDate: null,
                endDate: null
              }) {
                ... on ShipmentType {
                  id
                  date
                  status
                  location
                  receiveDate
                  entryTime
                  weight1Time
                  weight2Time
                  exitTime
                  shipmentType
                  licenseNumber
                  customerName
                  supplierName
                  weight1
                  unloadLocation
                  unit
                  quantity
                  quality
                  penalty
                  weight2
                  netWeight
                  listOfReels
                  profileName
                  width
                  salesId
                  pricePerKg
                  totalPrice
                  extraCost
                  materialType
                  materialName
                  vat
                  invoiceStatus
                  paymentStatus
                  documentInfo
                  comments
                  cancellationReason
                  username
                  logs
                }
              }
            }
          `
        })
        
        console.log('Raw data from server:', data?.filteredData)
        
        if (!data?.filteredData) {
          console.log('No data received')
          this.shipments = []
          this.filteredShipments = []
          this.$emit('filter-applied', [])
          return
        }

        // Filter out empty objects and translate values
        const validShipments = data.filteredData
          .filter(item => 
            item && 
            typeof item === 'object' && 
            Object.keys(item).length > 0 &&
            item.id &&
            item.__typename === 'ShipmentType'
          )
          .map(shipment => {
            console.log('Processing shipment:', shipment)
            const translated = {
              ...shipment,
              location: this.translateValue(shipment.location, 'location'),
              shipmentType: this.translateValue(shipment.shipmentType, 'shipmentType'),
              status: this.translateValue(shipment.status, 'status'),
              unloadLocation: this.translateValue(shipment.unloadLocation, 'unloadLocation')
            }
            console.log('Translated shipment:', translated)
            return translated
          })

        console.log('Final translated shipments:', validShipments)
        this.shipments = validShipments
        this.filteredShipments = validShipments
        this.$emit('filter-applied', validShipments)
      } catch (err) {
        this.error = 'خطا در بارگذاری بارنامه‌ها'
        console.error('Error loading shipments:', err)
        this.shipments = []
        this.filteredShipments = []
        this.$emit('filter-applied', [])
      } finally {
        this.loading = false
      }
    },
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        shipmentStatus: '',
        shipmentType: '',
        shipmentLocation: '',
        unloadLocation: '',
        licenseNumber: '',
        customerName: '',
        supplierName: '',
        materialType: '',
        materialName: '',
        weight1: '',
        weight2: '',
        netWeight: '',
        pricePerKg: '',
        totalPrice: '',
        extraCost: '',
        invoiceStatus: '',
        paymentStatus: ''
      }
      this.fieldErrors = {}
      this.error = null
      this.filteredShipments = this.shipments
      this.$emit('filter-reset', this.shipments)
    },
    async applyFilters() {
      this.loading = true
      this.error = null
      this.fieldErrors = {}
      
      try {
        const { isValid, errors } = validateForm(this.filters, 'shipment')
        
        if (!isValid) {
          this.fieldErrors = errors
          this.error = 'لطفا خطاهای فرم را برطرف کنید'
          return
        }

        const cleanFilters = cleanFormData(this.filters)
        
        this.filteredShipments = this.shipments.filter(shipment => {
          if (Object.keys(cleanFilters).length === 0) return true

          if (cleanFilters.shipmentStatus && shipment.status !== cleanFilters.shipmentStatus) return false
          if (cleanFilters.shipmentType && shipment.shipmentType !== cleanFilters.shipmentType) return false
          if (cleanFilters.shipmentLocation && !shipment.location.includes(cleanFilters.shipmentLocation)) return false
          if (cleanFilters.unloadLocation && shipment.unloadLocation !== cleanFilters.unloadLocation) return false
          if (cleanFilters.licenseNumber && !shipment.licenseNumber.includes(cleanFilters.licenseNumber)) return false
          if (cleanFilters.customerName && !shipment.customerName.includes(cleanFilters.customerName)) return false
          if (cleanFilters.supplierName && !shipment.supplierName.includes(cleanFilters.supplierName)) return false
          if (cleanFilters.materialType && !shipment.materialType.includes(cleanFilters.materialType)) return false
          if (cleanFilters.materialName && !shipment.materialName.includes(cleanFilters.materialName)) return false
          if (cleanFilters.invoiceStatus && shipment.invoiceStatus !== cleanFilters.invoiceStatus) return false
          if (cleanFilters.paymentStatus && shipment.paymentStatus !== cleanFilters.paymentStatus) return false

          if (cleanFilters.weight1 && shipment.weight1 !== Number(cleanFilters.weight1)) return false
          if (cleanFilters.weight2 && shipment.weight2 !== Number(cleanFilters.weight2)) return false
          if (cleanFilters.netWeight && shipment.netWeight !== Number(cleanFilters.netWeight)) return false
          if (cleanFilters.pricePerKg && shipment.pricePerKg !== Number(cleanFilters.pricePerKg)) return false
          if (cleanFilters.totalPrice && shipment.totalPrice !== Number(cleanFilters.totalPrice)) return false
          if (cleanFilters.extraCost && shipment.extraCost !== Number(cleanFilters.extraCost)) return false

          if (cleanFilters.startDate) {
            const startDate = new Date(cleanFilters.startDate)
            const shipmentDate = new Date(shipment.date)
            if (shipmentDate < startDate) return false
          }
          if (cleanFilters.endDate) {
            const endDate = new Date(cleanFilters.endDate)
            const shipmentDate = new Date(shipment.date)
            if (shipmentDate > endDate) return false
          }

          return true
        })

        this.$emit('filter-applied', this.filteredShipments)
      } catch (err) {
        this.error = err.message
        console.error('Filter error:', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 