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
        <label class="block text-sm font-medium text-gray-700">تاریخ شروع <span class="text-red-500">*</span></label>
        <input 
          type="date" 
          v-model="filters.startDate"
          required
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.startDate ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.startDate" class="mt-1 text-sm text-red-600">{{ fieldErrors.startDate }}</p>
      </div>
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">تاریخ پایان <span class="text-red-500">*</span></label>
        <input 
          type="date" 
          v-model="filters.endDate"
          required
          :class="[
            'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            fieldErrors.endDate ? 'border-red-500' : ''
          ]"
        >
        <p v-if="fieldErrors.endDate" class="mt-1 text-sm text-red-600">{{ fieldErrors.endDate }}</p>
      </div>

      <!-- Status and Location -->
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


      <!-- Price -->
      <div class="col-span-1">
        <label class="block text-sm font-medium text-gray-700">قیمت هر کیلو</label>
        <input 
          type="number" 
          v-model="filters.pricePerKg"
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
        shipmentLocation: '',
        unloadLocation: '',
        licenseNumber: '',
        customerName: '',
        materialName: '',
        pricePerKg: '',
        invoiceStatus: '',
        paymentStatus: ''
      },
      statusOptions: [
        { value: '', label: 'همه' },
        { value: 'Registered', label: 'ثبت شده' },
        { value: 'Loading', label: 'در حال بارگیری' },
        { value: 'Loaded', label: 'بارگیری شده' },
        { value: 'Office', label: 'دفتر' },
        { value: 'Delivered', label: 'تحویل داده شده' },
        { value: 'Cancelled', label: 'لغو شده' }
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
        { value: 'ANBAR_MUHVATEH_KARDAN', label: 'انبار محوطه کردان' },
        { value: 'Anbar_Sangin', label: 'انبار محوطه سنگین' },
        { value: 'Anbar_Khamir_Kordan', label: 'انبار خمیر کردان' },
        { value: 'Anbar_Muhavateh_Homayoun', label: 'انبار محوطه همایون' },
        { value: 'Anbar_Khamir_Ghadim', label: 'انبار خمیر قدیم' },
        { value: 'Anbar_Salon_Tolid', label: 'انبار سالن تولید' },
        { value: 'ANBAR_ASLI', label: 'انبار اصلی' },
        { value: 'Anbar_PAK', label: 'انبار پاک' },
        { value: 'ANBAR_FARANGI', label: 'انبار فرنگی' }
      ],
      invoiceStatusOptions: getTranslationOptions('invoiceStatus'),
      paymentStatusOptions: [
        { value: '', label: 'همه' },
        { value: 'Paid', label: 'پرداخت شده' },
        { value: 'Terms', label: 'نسیه' }
      ],
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

      const upperValue = value?.toUpperCase()
      const translationMap = translations[type] || {}
      const translatedValue = Object.entries(translationMap).find(([key]) => 
        key.toUpperCase() === upperValue
      )?.[1]

      return translatedValue || value
    },
    async loadShipments() {
      this.loading = true
      try {
        const { data } = await apolloClient.query({
          query: gql`
            query GetAllShipments {
              filteredData(filterInput: { 
                shipmentType: "Outgoing",
                shipmentStatus: null,
                shipmentLocation: null,
                licenseNumber: null,
                customerName: null,
                supplierName: null,
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
                  weight1
                  weight2
                  exitTime
                  licenseNumber
                  customerName
                  supplierName
                  unloadLocation
                  unit
                  quantity
                  quality
                  penalty
                  listOfReels
                  profileName
                  width
                  salesId
                  pricePerKg
                  materialName
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
        
        if (!data?.filteredData) {
          console.log('No data received')
          this.shipments = []
          this.filteredShipments = []
          this.$emit('filter-applied', [])
          return
        }

        const validShipments = data.filteredData
          .filter(item => 
            item && 
            typeof item === 'object' && 
            Object.keys(item).length > 0 &&
            item.id &&
            item.__typename === 'ShipmentType'
          )
          .map(shipment => ({
            ...shipment,
            location: this.translateValue(shipment.location, 'location'),
            status: this.translateValue(shipment.status, 'status'),
            unloadLocation: this.translateValue(shipment.unloadLocation, 'unloadLocation')
          }))

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
        shipmentLocation: '',
        unloadLocation: '',
        licenseNumber: '',
        customerName: '',
        materialName: '',
        pricePerKg: '',
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
        // Validate dates first
        if (!this.filters.startDate) {
          this.fieldErrors.startDate = 'تاریخ شروع الزامی است'
          this.error = 'لطفا تاریخ شروع را وارد کنید'
          return
        }
        if (!this.filters.endDate) {
          this.fieldErrors.endDate = 'تاریخ پایان الزامی است'
          this.error = 'لطفا تاریخ پایان را وارد کنید'
          return
        }

        const startDate = new Date(this.filters.startDate)
        const endDate = new Date(this.filters.endDate)

        if (startDate > endDate) {
          this.fieldErrors.endDate = 'تاریخ پایان باید بعد از تاریخ شروع باشد'
          this.error = 'تاریخ پایان باید بعد از تاریخ شروع باشد'
          return
        }

        const { isValid, errors } = validateForm(this.filters, 'shipment')
        
        if (!isValid) {
          this.fieldErrors = errors
          this.error = 'لطفا خطاهای فرم را برطرف کنید'
          return
        }

        const cleanFilters = cleanFormData(this.filters)
        cleanFilters.shipmentType = 'Outgoing'

        // If status is CANCELLED, use the cancelled shipments query
        if (cleanFilters.shipmentStatus === 'CANCELLED') {
          const { data } = await apolloClient.query({
            query: gql`
              query GetCancelledShipments {
                shipments(filter: { status: "CANCELLED" }) {
                  id
                  date
                  status
                  location
                  receiveDate
                  entryTime
                  weight1Time
                  weight2Time
                  weight1
                  weight2
                  exitTime
                  licenseNumber
                  customerName
                  supplierName
                  unloadLocation
                  unit
                  quantity
                  quality
                  penalty
                  listOfReels
                  profileName
                  width
                  salesId
                  pricePerKg
                  materialName
                  invoiceStatus
                  paymentStatus
                  documentInfo
                  comments
                  cancellationReason
                  username
                  logs
                }
              }
            `
          })
          
          if (!data?.shipments) {
            console.log('No data received')
            this.filteredShipments = []
            this.$emit('filter-applied', [])
            return
          }

          const validShipments = data.shipments
            .filter(item => 
              item && 
              typeof item === 'object' && 
              Object.keys(item).length > 0 &&
              item.id
            )
            .map(shipment => ({
              ...shipment,
              location: this.translateValue(shipment.location, 'location'),
              status: this.translateValue(shipment.status, 'status'),
              unloadLocation: this.translateValue(shipment.unloadLocation, 'unloadLocation')
            }))

          this.filteredShipments = validShipments
          this.$emit('filter-applied', validShipments)
          return
        }
        
        // Construct filter input for filteredData query
        const filterInput = {
          shipmentType: 'Outgoing',
          startDate: cleanFilters.startDate || null,
          endDate: cleanFilters.endDate || null,
          shipmentStatus: cleanFilters.shipmentStatus || null,
          shipmentLocation: cleanFilters.shipmentLocation || null,
          unloadLocation: cleanFilters.unloadLocation || null, // Add unloadLocation filter
          licenseNumber: cleanFilters.licenseNumber || null,
          customerName: cleanFilters.customerName || null,
          materialName: cleanFilters.materialName || null,
          pricePerKg: cleanFilters.pricePerKg ? Number(cleanFilters.pricePerKg) : null,
          invoiceStatus: cleanFilters.invoiceStatus || null,
          paymentStatus: cleanFilters.paymentStatus || null
          // Add other filter fields as needed
        }

        // Remove null or empty string values from filterInput
        Object.keys(filterInput).forEach(key => {
          if (filterInput[key] === null || filterInput[key] === '') {
            delete filterInput[key];
          }
        });

        // Use the filteredData query for other filters
        const { data } = await apolloClient.query({
          query: gql`
            query FilterShipments($filterInput: FilterInput) {
              filteredData(filterInput: $filterInput) {
                ... on ShipmentType {
                  id
                  date
                  status
                  location
                  receiveDate
                  entryTime
                  weight1Time
                  weight2Time
                  weight1
                  weight2
                  exitTime
                  licenseNumber
                  customerName
                  supplierName
                  unloadLocation
                  unit
                  quantity
                  quality
                  penalty
                  listOfReels
                  profileName
                  width
                  salesId
                  pricePerKg
                  materialName
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
          `,
          variables: {
            filterInput: filterInput
          }
        })

        // Handle potential null/empty response from the query
        const validShipments = handleEmptyResponse(data?.filteredData, 'ShipmentType')

        // Apply date range filter client-side as it's not consistently applied backend for filteredData
        const finalFilteredShipments = validShipments.filter(shipment => {
           const shipmentDate = new Date(shipment.date);
           const startDateObj = cleanFilters.startDate ? new Date(cleanFilters.startDate) : null;
           const endDateObj = cleanFilters.endDate ? new Date(cleanFilters.endDate) : null;

           if (startDateObj && shipmentDate < startDateObj) return false;
           if (endDateObj && shipmentDate > endDateObj) return false;

           return true;
        });

        this.filteredShipments = finalFilteredShipments;
        this.$emit('filter-applied', finalFilteredShipments);

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